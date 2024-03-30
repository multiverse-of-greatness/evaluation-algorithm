import json
import os
import re
from base64 import b64decode
from json.decoder import JSONDecodeError

from loguru import logger

from src.config import CRITERIA_DIR_PATH, OUTPUT_DIR_PATH
from src.models.criterion import Criterion
from src.models.story_chunk import StoryChunk
from src.models.story_data import StoryData


def write_image(b64image: str, path: str):
    if b64image is None:
        return
    image = b64decode(b64image)
    with open(path, "wb") as file:
        file.write(image)


def get_criterion_objs() -> list[Criterion]:
    criteria = [criterion for criterion in os.listdir(CRITERIA_DIR_PATH) if criterion.endswith(".txt")]
    criterion_objs = []
    for criterion in criteria:
        with open(CRITERIA_DIR_PATH / criterion, "r") as file:
            criterion_text = file.read()
        criterion_name = criterion.split(".")[0]
        criterion_obj = Criterion(criterion_name, criterion_text)
        criterion_objs.append(criterion_obj)
    return criterion_objs


def save_raw_output_to_file(
        raw_output: str, model: str, temperature: float, criterion: Criterion, 
        story_data: StoryData, story_chunk: StoryChunk = None):
    if story_chunk:
        id = story_chunk.id
        story = story_chunk.get_narratives()
        output_path = OUTPUT_DIR_PATH / story_chunk.story_id / "chunks" / story_chunk.id / criterion.name
    else:
        id = story_data.id
        story = story_data.get_text()
        output_path = OUTPUT_DIR_PATH / story_data.id / "main" / criterion.name
    output_path.mkdir(parents=True, exist_ok=True)

    last_trial_num = 0
    for file in os.listdir(output_path):
        if file.endswith(".json"):
            last_trial_num += 1

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
        "id": id,
        "story": story,
        "trial_num": last_trial_num + 1,
        "model": model,
        "temperature": temperature,
        "criterion": criterion.criterion,
        "raw_output": raw_output,
        "parsed_output": parsed_output,
    }

    file_name = f"{last_trial_num + 1}.json"
    with open(output_path / file_name, "w") as f:
        json.dump(json_obj, f, indent=2)
        logger.info(f"Saved raw output to {str(output_path / file_name)}")
