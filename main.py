from pathlib import Path
from typing import Annotated, Optional

import typer
from dotenv import load_dotenv
from loguru import logger

from src.analysis import run_analysis
from src.evaluation import run_evaluation
from src.models.analysis_context import AnalysisContext
from src.models.evaluation_context import EvaluationContext
from src.repositories.criterion import CriterionRepository
from src.repositories.story_data import StoryDataRepository
from src.utils.generative_models import get_generation_model

app = typer.Typer()


@app.command()
def batch_run_evaluation_with(
        story_ids_list_path: Annotated[Path, typer.Option(
            help="Path of a text file containing a list of story ids to evaluate. Story ids should be separated by new "
                 "lines")],
        trial_id: Annotated[str, typer.Option(help="The trial id to save")],
        model_name: Annotated[Optional[str], typer.Option(help="The generative model to use")] = "gpt-3.5-turbo-0125"):
    with open(story_ids_list_path, "r") as f:
        story_ids = f.read().splitlines()
        logger.info(f"Running evaluation for {len(story_ids)} stories")
        for story_id in story_ids:
            logger.info(f"Running evaluation for story {story_id}")
            run_evaluation_with(story_id=story_id, trial_id=trial_id, model_name=model_name)
            logger.info(f"Finished evaluation for story {story_id}")


@app.command()
def run_evaluation_with(
        story_id: Annotated[str, typer.Option(help="The story id to evaluate")],
        trial_id: Annotated[str, typer.Option(help="The trial id to save")],
        model_name: Annotated[Optional[str], typer.Option(help="The generative model to use")] = "gpt-3.5-turbo-0125"):
    context = EvaluationContext(
        story_id=story_id,
        trial_id=trial_id,
        generative_model=get_generation_model(model_name),
        criterion_objs=CriterionRepository().list_criterion()
    )
    logger.info(f"Running evaluation with context: {context}")
    story_data = StoryDataRepository().get(story_id)
    logger.info(f"Story data loaded")
    run_evaluation(context, story_data)


@app.command()
def run_analysis_with(
        story_id: Annotated[str, typer.Option(help="The story id to analyze")],
        trial_id: Annotated[str, typer.Option(help="The trial id to analyze")]):
    context = AnalysisContext(
        story_id=story_id,
        trial_id=trial_id,
        criterion_objs=CriterionRepository().list_criterion()
    )
    logger.info(f"Running analysis with context: {context}")
    analysis_result = run_analysis(context)
    print(f"Results for story {story_id}:")
    for criterion, score in analysis_result.items():
        print(f"{criterion}: {score['mean']:.4f} ± {score['sd']:.4f}")


if __name__ == "__main__":
    load_dotenv()
    app()
