import json

from .story_narrative import StoryNarrative


class StoryChunk:
    def __init__(self, id: str, story_id: str, chapter: int, story_so_far: str, story: list[StoryNarrative]):
        self.id = id
        self.story_id = story_id
        self.chapter = chapter
        self.story_so_far = story_so_far
        self.story = story

    @staticmethod
    def from_json(json_obj: dict):
        return StoryChunk(
            id=json_obj["id"],
            story_id=json_obj["story_id"],
            chapter=json_obj["chapter"],
            story_so_far=json_obj["story_so_far"],
            story=[StoryNarrative.from_json(n) for n in json.loads(json_obj["story"])],
        )

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "story_id": self.story_id,
            "chapter": self.chapter,
            "story_so_far": self.story_so_far,
            "story": [narrative.to_json() for narrative in self.story],
        }
    
    def get_narratives(self) -> str:
        return '\n'.join([f"{narrative.speaker}: {narrative.text}" for narrative in self.story])

    def __str__(self):
        return f"StoryChunk(id={self.id}, story_id={self.story_id}, chapter={self.chapter}, story_so_far={self.story_so_far}, story={[str(n) for n in self.story]}, choices={[str(c) for c in self.choices]})"
