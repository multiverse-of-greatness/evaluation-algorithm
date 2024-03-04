import json
import os

import numpy as np

from .config import CRITERIA_DIR_PATH, OUTPUT_DIR_PATH
from .structs.criterion import Criterion


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


def calc_mean_sd(criterion_scores: list[float]) -> tuple[float, float]:
    if len(criterion_scores) == 0:
        return 0, 0
    return np.mean(criterion_scores), np.std(criterion_scores)


def evaluate_story(story_id: str, criterion_objs: list[Criterion]) -> dict:
    criterion_scores = {criterion.name: [] for criterion in criterion_objs}
    evaluation_obj = {criterion.name: {} for criterion in criterion_objs}
    # Evaluate main story data
    story_data_path = OUTPUT_DIR_PATH / story_id / "main"
    for criterion in criterion_objs:
        files = [file for file in os.listdir(story_data_path / criterion.name) if not file.startswith('.')]
        for file in files:
            with open(story_data_path / criterion.name / file, 'r') as file:
                data = json.load(file)
            if "error" in data["parsed_output"]:
                continue
            factor_scores = data["parsed_output"][criterion.name]
            score_avg, _ = calc_mean_sd([factor["score"] for factor in factor_scores])
            if score_avg > 0:
                criterion_scores[criterion.name].append(score_avg)
    # Evaluate chunks
    story_chunks_path = OUTPUT_DIR_PATH / story_id / "chunks"
    chunks = [chunk for chunk in os.listdir(story_chunks_path) if not chunk.startswith('.')]
    for chunk in chunks:
        for criterion in criterion_objs:
            files = [file for file in os.listdir(story_chunks_path / chunk / criterion.name) if not file.startswith('.')]
            for file in files:
                with open(story_chunks_path / chunk / criterion.name / file, 'r') as file:
                    data = json.load(file)
                if "error" in data["parsed_output"]:
                    continue
                factor_scores = data["parsed_output"][criterion.name]
                score_avg, _ = calc_mean_sd([factor["score"] for factor in factor_scores])
                if score_avg > 0:
                    criterion_scores[criterion.name].append(score_avg)
    # Calculate average and standard deviation
    for criterion in criterion_objs:
        evaluation_obj[criterion.name]["avg"] = np.mean(criterion_scores[criterion.name])
        evaluation_obj[criterion.name]["sd"] = np.std(criterion_scores[criterion.name])
    return evaluation_obj