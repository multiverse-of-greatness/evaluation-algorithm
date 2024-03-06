from base64 import b64decode
from typing import Annotated

import typer
from dotenv import load_dotenv

from src.config import OUTPUT_DIR_PATH
from src.databases import Neo4J
from src.repositories.story_data import StoryDataRepository


def write_image(b64image: str, path: str):
    if b64image is None:
        return
    image = b64decode(b64image)
    with open(path, "wb") as file:
        file.write(image)


def main(
    story_id: Annotated[
        str, typer.Option(help="The story id to evaluate")
    ]
):
    db = Neo4J()
    story_data_repository = StoryDataRepository(db)
    story = story_data_repository.get(story_id)
    output_path = OUTPUT_DIR_PATH / story_id / "images"
    output_path.mkdir(parents=True, exist_ok=True)
    for scene in story.main_scenes:
        write_image(scene.image, output_path / f"scene_{scene.id}.png")
    for character in story.main_characters:
        write_image(character.image, output_path / f"character_{character.id}.png")


if __name__ == "__main__":
    load_dotenv()
    typer.run(main)
