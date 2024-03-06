from typing import Annotated

import typer
from dotenv import load_dotenv

from src.analysis import evaluate_story, get_criterion_objs


def print_result(result: dict) -> None:
    for criterion, score in result.items():
        print(f"{criterion}: {score['avg']} ± {score['sd']}")


def main(
    story_id: Annotated[
        str, typer.Option(help="The story id to evaluate")
    ]
):
    criterion_objs = get_criterion_objs()
    result = evaluate_story(story_id, criterion_objs)
    print(f"Results for story {story_id}:")
    print_result(result)


if __name__ == "__main__":
    load_dotenv()
    typer.run(main)
