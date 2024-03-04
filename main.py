import os
from pathlib import Path
from time import sleep

import google.generativeai as genai
from dotenv import load_dotenv
from loguru import logger

from src.config import CRITERIA_DIR_PATH, MODEL, TEMPERATURE
from src.databases import Neo4J
from src.models import GoogleGenerativeAI
from src.prompts import (story_chunk_evaluation_prompt,
                         story_data_evaluation_prompt)
from src.repositories.story_chunk import StoryChunkRepository
from src.repositories.story_data import StoryDataRepository
from src.structs.criterion import Criterion
from src.utils import save_raw_output_to_file


def main():
    database = Neo4J()
    story_chunk_repository = StoryChunkRepository(database)
    story_data_repository = StoryDataRepository(database)
    model = GoogleGenerativeAI()
    logger.info("=== Evaluating ===")
    logger.info(f"Model: {MODEL}, Temperature: {TEMPERATURE}")
    criteria = [criterion for criterion in os.listdir(CRITERIA_DIR_PATH) if criterion.endswith(".txt")]
    current_count = 0
    for criterion in criteria:
        logger.info(f"--- Progress: {current_count+1}/{len(criteria)} ---")
        story_id = "488395e4-d625-11ee-9079-9a01b5b45ca5"
        story_data = story_data_repository.get(story_id)
        with open(CRITERIA_DIR_PATH / criterion, "r") as file:
            criterion_text = file.read()
        criterion_name = criterion.split(".")[0]
        criterion_obj = Criterion(criterion_name, criterion_text)
        prompt = story_data_evaluation_prompt(story_data, criterion_obj)
        response = model.generate(prompt, temperature=TEMPERATURE)
        save_raw_output_to_file(response, MODEL, TEMPERATURE, criterion_obj, story_data)

        story_chunk = story_data.start_chunk
        prompt = story_chunk_evaluation_prompt(story_chunk, story_data, criterion_obj)
        response = model.generate(prompt, temperature=TEMPERATURE)
        save_raw_output_to_file(response, MODEL, TEMPERATURE, criterion_obj, story_data, story_chunk)

        current_count += 1
        sleep(3)
    logger.info("Finished evaluating game stories.")


if __name__ == "__main__":
    load_dotenv()
    Path("logs").mkdir(exist_ok=True)
    logger.add("logs/{time}.log")
    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)
    main()
