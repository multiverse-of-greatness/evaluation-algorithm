from typing import Annotated

import typer
from dotenv import load_dotenv
from loguru import logger

from src.analysis import evaluate_story
from src.config import OUTPUT_DIR_PATH
from src.evaluation import evaluate_story_chunks, evaluate_story_data
from src.repositories.story_data import StoryDataRepository
from src.utils.file_io import write_image
from src.utils.generative_models import get_generation_model

app = typer.Typer()


@app.command()
def run_evaluation(
        story_id: Annotated[str, typer.Option(help="The story id to evaluate")],
        model_name: Annotated[str, typer.Option(help="The generative model to use")]):
    logger.info(f"Running evaluation for story {story_id}")
    generative_model = get_generation_model(model_name)
    logger.info(f"Using model {model_name}")
    evaluate_story_data(story_id, generative_model)
    evaluate_story_chunks(story_id, generative_model)


@app.command()
def run_analysis(
        story_id: Annotated[str, typer.Option(help="The story id to evaluate")]):
    logger.info(f"Running analysis for story {story_id}")
    result = evaluate_story(story_id)
    print(f"Results for story {story_id}:")
    for criterion, score in result.items():
        print(f"{criterion}: {score['mean']} ± {score['sd']}")


@app.command()
def generate_image(
        story_id: Annotated[str, typer.Option(help="The story id to evaluate")]):
    story_data_repository = StoryDataRepository()
    story = story_data_repository.get(story_id)
    output_path = OUTPUT_DIR_PATH / story_id / "images"
    output_path.mkdir(parents=True, exist_ok=True)
    for scene in story.main_scenes:
        write_image(scene.image, output_path / f"scene_{scene.id}.png")
    for character in story.main_characters:
        write_image(character.image, output_path / f"character_{character.id}.png")


if __name__ == "__main__":
    load_dotenv()
    app()