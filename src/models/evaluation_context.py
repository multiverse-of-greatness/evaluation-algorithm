import json
import re
from json import JSONDecodeError
from pathlib import Path

from loguru import logger

from src.config import OUTPUT_DIR_PATH
from src.generative_models.llm import LLM
from src.models.criterion import Criterion
from src.models.story_chunk import StoryChunk


class EvaluationContext:
    def __init__(self, story_id: str, trial_id: str, generative_model: LLM, criterion_objs: list[Criterion]):
        self.story_id = story_id
        self.trial_id = trial_id
        self.generative_model = generative_model
        self.criterion_objs = criterion_objs

    def get_output_dir(self, story_chunk: StoryChunk = None) -> Path:
        dir_name = "story-data" if not story_chunk else f"story-chunk-{story_chunk.id}"
        return OUTPUT_DIR_PATH / self.story_id / self.trial_id / dir_name

    def is_data_already_evaluated(self, criterion: Criterion, story_chunk: StoryChunk = None) -> bool:
        return (self.get_output_dir(story_chunk) / f"{criterion.name}.json").exists()

    def save_raw_output_to_file(self, raw_output: str, story: str, criterion: Criterion, story_chunk: StoryChunk = None):
        output_dir = self.get_output_dir(story_chunk)
        output_dir.mkdir(parents=True, exist_ok=True)

        try:
            parsed_output = raw_output
            if "```json" in parsed_output:
                parsed_output = re.search(r"```json(.*)```", parsed_output, re.DOTALL).group(1).strip()
            parsed_output = re.search(r"\{.*}", parsed_output, re.DOTALL).group(0).strip()
            parsed_output = json.loads(parsed_output, strict=False)
        except JSONDecodeError as e:
            logger.error(f"Failed to parse output: {e}")
            parsed_output = {"error": str(e)}

        json_obj = {
            "id": self.story_id,
            "story": story,
            "trial_id": self.trial_id,
            "model": self.generative_model.model_name,
            "criterion": criterion.criterion,
            "raw_output": raw_output,
            "parsed_output": parsed_output,
        }

        with open(output_dir / f"{criterion.name}.json", "w") as file:
            json.dump(json_obj, file, indent=2)
            logger.info(f"Saved raw output to {str(output_dir / f'{criterion.name}.json')}")

    def __str__(self):
        return f"EvaluationContext(story_data={self.story_id}, trial_id={self.trial_id}, generative_model={self.generative_model.model_name})"
    