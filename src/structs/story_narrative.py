class StoryNarrative:
    def __init__(self, id: int, speaker: str, text: str):
        self.id = id
        self.speaker = speaker
        self.text = text

    @staticmethod
    def from_json(json_obj: dict):
        return StoryNarrative(json_obj['id'], json_obj['speaker'], json_obj['text'])

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'speaker': self.speaker,
            'text': self.text
        }

    def __str__(self):
        return f'StoryNarrative(id={self.id}, speaker={self.speaker}, text={self.text})'
