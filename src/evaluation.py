from time import sleep

from loguru import logger

from src.generative_models.llm import LLM
from src.prompts import (story_chunk_evaluation_prompt,
                         story_data_evaluation_prompt)
from src.repositories.story_chunk import StoryChunkRepository
from src.repositories.story_data import StoryDataRepository
from src.utils.file_io import get_criterion_objs, save_raw_output_to_file
from src.utils.openai_ai import append_openai_message


def evaluate_story_data(story_id: str, generative_model: LLM):
    logger.info(f"Evaluating story {story_id}")
    story_data_repository = StoryDataRepository()
    story_data = story_data_repository.get(story_id)
    logger.info(f"Story data loaded")
    criterion_objs = get_criterion_objs()
    logger.info(f"Criteria loaded")
    for criterion in criterion_objs:
        logger.info(f"Evaluating {criterion.name}")
        prompt = story_data_evaluation_prompt(story_data, criterion)
        response = generative_model.generate_content(append_openai_message(prompt))
        save_raw_output_to_file(response, generative_model.model_name, 0, criterion, story_data)
    logger.info(f"Finished evaluating story {story_data.id}")
    sleep(3)


def evaluate_story_chunks(story_id: str, generative_model: LLM):
    logger.info(f"Evaluating story {story_id}")
    story_data_repository = StoryDataRepository()
    story_chunk_repository = StoryChunkRepository()
    story_data = story_data_repository.get(story_id)
    frontiers = [story_data.start_chunk]
    logger.info(f"Story data loaded")
    criterion_objs = get_criterion_objs()
    logger.info(f"Criteria loaded")
    while frontiers:
        current_chunk = frontiers.pop(0)
        logger.info(f"Evaluating chunk {current_chunk.id}")
        for criterion in criterion_objs:
            logger.info(f"Evaluating {criterion.name}")
            prompt = story_chunk_evaluation_prompt(current_chunk, story_data, criterion)
            response = generative_model.generate_content(append_openai_message(prompt))
            save_raw_output_to_file(response, generative_model.model_name, 0, criterion, story_data, current_chunk)
        logger.info(f"Finished evaluating chunk {current_chunk.id}")
        branched_chunks = story_chunk_repository.get_branched_chunks(current_chunk.id)
        frontiers.extend(branched_chunks)
        logger.info(f"Data added to frontiers: +{len(branched_chunks)}, Total: {len(frontiers)}")
        sleep(3)
