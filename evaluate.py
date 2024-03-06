from pathlib import Path
from time import sleep
from typing import Annotated

import typer
from dotenv import load_dotenv
from loguru import logger

from src.analysis import get_criterion_objs
from src.config import CRITERIA_DIR_PATH, MODEL, TEMPERATURE
from src.databases import Neo4J
from src.models import GoogleGenerativeAI
from src.prompts import (story_chunk_evaluation_prompt,
                         story_data_evaluation_prompt)
from src.repositories.story_chunk import StoryChunkRepository
from src.repositories.story_data import StoryDataRepository
from src.structs.criterion import Criterion
from src.structs.story_data import StoryData
from src.utils import save_raw_output_to_file


def evaluate_story_data(story_data: StoryData, criterion_objs: list[Criterion], model: GoogleGenerativeAI):
    logger.info(f"Evaluating story {story_data.id}")
    for criterion in criterion_objs:
        logger.info(f"Evaluating {criterion.name}")
        prompt = story_data_evaluation_prompt(story_data, criterion)
        response = model.generate(prompt, temperature=TEMPERATURE)
        save_raw_output_to_file(response, MODEL, TEMPERATURE, criterion, story_data)
    logger.info(f"Finished evaluating story {story_data.id}")
    sleep(3)


def evaluate_story_chunks(story_data: StoryData, criterion_objs: list[Criterion], model: GoogleGenerativeAI, story_chunk_repository: StoryChunkRepository):
    frontiers = [story_data.start_chunk]
    while frontiers:
        current_chunk = frontiers.pop(0)
        logger.info(f"Evaluating chunk {current_chunk.id}")
        for criterion in criterion_objs:
            logger.info(f"Evaluating {criterion.name}")
            prompt = story_chunk_evaluation_prompt(current_chunk, story_data, criterion)
            response = model.generate(prompt, temperature=TEMPERATURE)
            save_raw_output_to_file(response, MODEL, TEMPERATURE, criterion, story_data, current_chunk)
        logger.info(f"Finished evaluating chunk {current_chunk.id}")
        branched_chunks = story_chunk_repository.get_branched_chunks(current_chunk.id)
        frontiers.extend(branched_chunks)
        logger.info(f"Data added to frontiers: +{len(branched_chunks)}, Total: {len(frontiers)}")
        sleep(3)


def main(
    story_id: Annotated[
        str, typer.Option(help="The story id to evaluate")
    ]
):
    database = Neo4J()
    story_chunk_repository = StoryChunkRepository(database)
    story_data_repository = StoryDataRepository(database)
    model = GoogleGenerativeAI()
    logger.info("=== Evaluating ===")
    logger.info(f"Model: {MODEL}, Temperature: {TEMPERATURE}")
    criterion_objs = get_criterion_objs()
    story_data = story_data_repository.get(story_id)
    evaluate_story_data(story_data, criterion_objs, model)
    evaluate_story_chunks(story_data, criterion_objs, model, story_chunk_repository)


if __name__ == "__main__":
    load_dotenv()
    Path("logs").mkdir(exist_ok=True)
    logger.add("logs/{time}.log")
    typer.run(main)
