from threading import Thread
import uvicorn

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

from sGPT import generate_caption
from config import get_config
from src import ElementType
from src import connectGPT
from utils import download_image, delete_image
from config import get_redis


configuration = get_config()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
        "http://localhost",
        "http://localhost:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def test_home() -> dict[str, str]:
    return {"Message": "Hello From FastAPI Server"}


class ProcessElementsBody(BaseModel):
    anchors: Optional[List[str]]
    images: Optional[List[str]]
    buttons: Optional[List[str]]


def populate_captions(image_index: int, image_url: str, captions: List[str]):
    """
    This function is not thread safe if two threads have same image_index.
    Use with extreme caution.
    """
    image_path = download_image(image_url)
    caption: str = generate_caption(image_path)
    captions[image_index] = caption
    deleted = delete_image(image_path)


@app.post("/process-elements")
async def read_root(req: ProcessElementsBody):
    print(req.images)
    accessible_anchors: List[str] = []
    accessible_buttons: List[str] = []

    images_url_list = req.images if req.images is not None else []
    images_url_count = len(images_url_list)
    accessible_images: List[str] = [""] * images_url_count
    image_processing_threads: List[Thread | None] = [None] * images_url_count

    if req.anchors is not None:
        anchor_output: str = await connectGPT(req.anchors, ElementType.ANCHOR)
        accessible_anchors = anchor_output.split("\n")

    if req.buttons is not None:
        button_output: str = await connectGPT(req.buttons, ElementType.BUTTON)
        accessible_buttons = button_output.split("\n")

    redis_conn = get_redis()

    for image_index, image_url in enumerate(images_url_list):
        caption_cnt = redis_conn.exists(image_url)
        print(caption_cnt)
        if caption_cnt > 0:
            existing_caption = redis_conn.get(name=image_url)
            accessible_images[image_index] = existing_caption
            print(
                "existing caption for url ", image_url, " is ", existing_caption
            )
            continue

        th = Thread(
            target=populate_captions,
            args=(
                image_index,
                image_url,
                accessible_images,
            ),
        )
        th.start()
        image_processing_threads[image_index] = th

    redis_conn.close()

    for thread_idx, th in enumerate(image_processing_threads):
        if th is not None:
            th.join()
            redis_conn.set(
                name=images_url_list[thread_idx],
                value=accessible_images[thread_idx],
            )

    server_response = {
        "anchors": accessible_anchors,
        "images": accessible_images,
        "buttons": accessible_buttons,
    }

    # print(server_response)
    return server_response


# if __name__ == "__main__":
#     uvicorn.run(app, port=configuration.SERVER_PORT)
