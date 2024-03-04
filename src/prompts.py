from .structs.story_data import StoryData
from .structs.story_chunk import StoryChunk
from .structs.criterion import Criterion


def story_chunk_evaluation_prompt(chunk: StoryChunk, story: StoryData, criterion: Criterion) -> str:
    theme_text = ", ".join([theme for theme in story.themes])
    concepts = f"\n\nConcepts:\n{theme_text}" if criterion.name == "inspiration" else ""

    return f"""Evaluate the following visual novel game story according to the specified criteria and assign a score with a total of 10 for each criterion, where 10 is the best and 0 is the worst. Provide reasons for your scores. Make sure to output it in a MarkDown code block, i.e., between ```json and ```.

Output format:
```json
{{
"chunk_id": "{chunk.id}",
"{criterion.name}": [{{ "factor_name": <factor>, "score": <int score out of 10>, "reason": <reason for the given score> }}]
}}
```

Criterion description:
{criterion.criterion}{concepts}

Story:
{chunk.get_narratives()}"""


def story_data_evaluation_prompt(story: StoryData, criterion: Criterion) -> str:
    theme_text = ", ".join([theme for theme in story.themes])
    concepts = f"\n\nConcepts:\n{theme_text}" if criterion.name == "inspiration" else ""

    return f"""Evaluate the following visual novel game story according to the specified criteria and assign a score with a total of 10 for each criterion, where 10 is the best and 0 is the worst. Provide reasons for your scores. Make sure to output it in a MarkDown code block, i.e., between ```json and ```.

Output format:
```json
{{
"story_id": "{story.id}",
"{criterion.name}": [{{ "factor_name": <factor>, "score": <int score out of 10>, "reason": <reason for the given score> }}]
}}
```

Criterion description:
{criterion.criterion}{concepts}

Story:
{story.get_text()}"""