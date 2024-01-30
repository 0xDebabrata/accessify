import uvicorn

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

from sGPT import generate_caption
from config import get_config
from src import ElementType
from src import connectGPT
from utils import download_image


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


@app.post("/process-elements")
async def read_root(req: ProcessElementsBody):
    accessible_anchors: List[str] = []
    accessible_images: List[str] = []
    accessible_buttons: List[str] = []

    if req.anchors is not None:
        anchor_output: str = await connectGPT(req.anchors, ElementType.ANCHOR)
        accessible_anchors = anchor_output.split("\n")

    if req.buttons is not None:
        button_output: str = await connectGPT(req.buttons, ElementType.BUTTON)
        accessible_buttons = button_output.split("\n")

    if req.images is not None:
        for image_url in req.images:
            image_path = download_image(image_url)
            caption: str = generate_caption(image_path)
            accessible_images.append(caption)

    server_response = {
        "anchors": accessible_anchors,
        "images": accessible_images,
        "buttons": accessible_buttons,
    }

    print(server_response)
    return server_response


if __name__ == "__main__":
    uvicorn.run(app, port=configuration.SERVER_PORT)
