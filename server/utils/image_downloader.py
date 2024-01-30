import urllib.request
import uuid
import os


def download_image(url: str) -> str:
    """
    Given the publicly available URL of an image, this function will
    download the image into local machine and return the path of the
    downloaded file stored in the file system.
    """

    # check whether temp directory already exists or not
    # and if it doesn't, create temp directory
    os.makedirs("./temp/", exist_ok=True)

    image_name = f"{str(uuid.uuid4())}_image.jpg"
    image_path = os.path.abspath(f"./temp/{image_name}")

    path, message = urllib.request.urlretrieve(url, image_path)

    return path
