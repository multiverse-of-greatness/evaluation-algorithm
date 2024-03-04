class SceneData:
    def __init__(self, id: int, title: str, location: str, description: str):
        self.id = id
        self.title = title
        self.location = location
        self.description = description

    @staticmethod
    def from_json(json_obj: dict):
        return SceneData(json_obj['id'], json_obj['title'], json_obj['location'], json_obj['description'])

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'location': self.location,
            'description': self.description
        }

    def __str__(self):
        return f'SceneData(id={self.id}, title={self.title}, location={self.location}, description={self.description})'
