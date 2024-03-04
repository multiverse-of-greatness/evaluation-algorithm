from dotenv import load_dotenv

from src.analysis import evaluate_story, get_criterion_objs


def print_result(result: dict) -> None:
    for criterion, score in result.items():
        print(f"{criterion}: {score['avg']} ± {score['sd']}")


def main():
    story_id = '488395e4-d625-11ee-9079-9a01b5b45ca5'
    criterion_objs = get_criterion_objs()
    result = evaluate_story(story_id, criterion_objs)
    print(f"Results for story {story_id}:")
    print_result(result)


if __name__ == "__main__":
    load_dotenv()
    main()
