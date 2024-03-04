class ChapterSynopsis:
    def __init__(self, chapter: int, synopsis: str):
        self.chapter = chapter
        self.synopsis = synopsis

    @staticmethod
    def from_json(json_obj: dict):
        return ChapterSynopsis(json_obj['chapter'], json_obj['synopsis'])

    def to_json(self) -> dict:
        return {
            'chapter': self.chapter,
            'synopsis': self.synopsis
        }

    def __str__(self):
        return f"ChapterSynopsis(chapter={self.chapter}, synopsis={self.synopsis})"
