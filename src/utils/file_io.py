from base64 import b64decode


def write_image(b64image: str, path: str):
    if b64image is None:
        return
    image = b64decode(b64image)
    with open(path, "wb") as file:
        file.write(image)
