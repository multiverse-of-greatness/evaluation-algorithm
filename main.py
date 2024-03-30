from typing import Annotated

import typer
from dotenv import load_dotenv
from loguru import logger

from src.analysis import evaluate_story
from src.evaluation import evaluate_story_chunks, evaluate_story_data
from src.image import convert_b64image_to_png
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
        story_id: Annotated[str, typer.Option(help="The story id to analyze")]):
    logger.info(f"Running analysis for story {story_id}")
    result = evaluate_story(story_id)
    print(f"Results for story {story_id}:")
    for criterion, score in result.items():
        print(f"{criterion}: {score['mean']} ± {score['sd']}")


@app.command()
def run_image_conversion(
        story_id: Annotated[str, typer.Option(help="The story id to convert images for")]):
    logger.info(f"Converting images for story {story_id}")
    convert_b64image_to_png(story_id)


if __name__ == "__main__":
    load_dotenv()
    app()