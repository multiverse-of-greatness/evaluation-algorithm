from .chapter_synopsis import ChapterSynopsis
from .character_data import CharacterData
from .ending_data import EndingData
from .scene_data import SceneData
from .story_chunk import StoryChunk


class StoryData:
    def __init__(self, id: str, title: str, genre: str, themes: list[str], main_scenes: list[SceneData],
                 main_characters: list[CharacterData], synopsis: str, chapter_synopses: list[ChapterSynopsis],
                 beginning: str, endings: list[EndingData], start_chunk: StoryChunk):
        self.id = id
        self.title = title
        self.genre = genre
        self.themes = themes
        self.main_scenes = main_scenes
        self.main_characters = main_characters
        self.synopsis = synopsis
        self.chapter_synopses = chapter_synopses
        self.beginning = beginning
        self.endings = endings
        self.start_chunk = start_chunk

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'genre': self.genre,
            'themes': self.themes,
            'main_scenes': [scene.to_json() for scene in self.main_scenes],
            'main_characters': [character.to_json() for character in self.main_characters],
            'synopsis': self.synopsis,
            'chapter_synopses': [chapter_synopsis.to_json() for chapter_synopsis in self.chapter_synopses],
            'beginning': self.beginning,
            'endings': [ending.to_json() for ending in self.endings],
            'start_chunk': self.start_chunk.to_json()
        }
    
    def get_text(self) -> str:
        ending_text = "\n".join([f"{i+1}. {e.ending}" for i, e in enumerate(self.endings)])
        return f"Synopsis:\n{self.synopsis}\nEndings:\n{ending_text}"

    def __str__(self):
        return f"""StoryData(id={self.id}, title={self.title}, genre={self.genre}, themes={self.themes}, main_scenes={[str(s) for s in self.main_scenes]}, main_characters={[str(c) for c in self.main_characters]}, synopsis={self.synopsis}, chapter_synopses={[str(cs) for cs in self.chapter_synopses]}, beginning={self.beginning}, endings={[str(e) for e in self.endings]})"""