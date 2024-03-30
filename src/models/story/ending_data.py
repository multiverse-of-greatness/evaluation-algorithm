class EndingData:
    def __init__(self, id: int, ending: str):
        self.id = id
        self.ending = ending

    @staticmethod
    def from_json(json_obj: dict):
        return EndingData(json_obj['id'], json_obj['ending'])

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'ending': self.ending
        }

    def __str__(self):
        return f'EndingData(id={self.id}, ending={self.ending})'
