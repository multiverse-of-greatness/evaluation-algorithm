from loguru import logger

from src.models.evaluation_context import EvaluationContext
from src.models.story_chunk import StoryChunk
from src.models.story_data import StoryData
from src.prompts import (story_chunk_evaluation_prompt,
                         story_data_evaluation_prompt)
from src.repositories.story_chunk import StoryChunkRepository
from src.utils.openai_ai import append_openai_message


def run_evaluation(context: EvaluationContext, story_data: StoryData):
    logger.info(f"Evaluating story {context.story_id}")
    evaluate_story_data(context, story_data)
    evaluate_story_chunks(context, story_data)
    logger.info(f"Finished evaluation for story {context.story_id}")


def evaluate_story_data(context: EvaluationContext, story_data: StoryData):
    for criterion in context.criterion_objs:
        logger.info(f"Evaluating {criterion.name}")
        if context.is_data_already_evaluated(criterion):
            logger.info(f"Skipping {criterion.name} as it is already evaluated")
            continue
        prompt = story_data_evaluation_prompt(story_data, criterion)
        response = context.generative_model.generate_content(append_openai_message(prompt))
        context.save_raw_output_to_file(response, story_data.get_text(), criterion)


def evaluate_story_chunks(context: EvaluationContext, story_data: StoryData):
    frontiers = [story_data.start_chunk]
    story_chunk_repository = StoryChunkRepository()
    while frontiers:
        current_chunk = frontiers.pop(0)
        evaluate_story_chunk(context, story_data, current_chunk)
        branched_chunks = story_chunk_repository.get_branched_chunks(current_chunk.id)
        frontiers.extend(branched_chunks)
        logger.info(f"Data added to frontiers: +{len(branched_chunks)}, Total: {len(frontiers)}")


def evaluate_story_chunk(context: EvaluationContext, story_data: StoryData, story_chunk: StoryChunk):
    logger.info(f"Evaluating chunk {story_chunk.id}")
    for criterion in context.criterion_objs:
        if context.is_data_already_evaluated(criterion, story_chunk):
            logger.info(f"Skipping {criterion.name} as it is already evaluated")
            continue
        logger.info(f"Evaluating {criterion.name}")
        prompt = story_chunk_evaluation_prompt(story_chunk, story_data, criterion)
        response = context.generative_model.generate_content(append_openai_message(prompt))
        context.save_raw_output_to_file(response, story_chunk.get_narratives(), criterion, story_chunk)
    logger.info(f"Finished evaluating chunk {story_chunk.id}")
