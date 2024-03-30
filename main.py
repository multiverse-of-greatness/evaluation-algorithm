from typing import Annotated

import typer
from dotenv import load_dotenv
from loguru import logger

from src.evaluation import evaluate_story_chunks, evaluate_story_data
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


if __name__ == "__main__":
    load_dotenv()
    app()