from src.config import OUTPUT_DIR_PATH
from src.repositories.story_data import StoryDataRepository
from src.utils.file_io import write_image


def convert_b64image_to_png(story_id: str):
    story_data_repository = StoryDataRepository()
    story = story_data_repository.get(story_id)
    output_path = OUTPUT_DIR_PATH / story_id / "images"
    output_path.mkdir(parents=True, exist_ok=True)
    for scene in story.main_scenes:
        write_image(scene.image, output_path / f"scene_{scene.id}.png")
    for character in story.main_characters:
        write_image(character.image, output_path / f"character_{character.id}.png")
