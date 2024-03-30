import json

from loguru import logger

from src.databases import Neo4J
from src.models.story.chapter_synopsis import ChapterSynopsis
from src.models.story.character_data import CharacterData
from src.models.story.ending_data import EndingData
from src.models.story.scene_data import SceneData
from src.models.story_chunk import StoryChunk
from src.models.story_data import StoryData


class StoryDataRepository:
    _instance = None

    @classmethod
    def __new__(cls):
        if cls._instance is None:
            logger.info("Creating new StoryDataRepository instance")
            cls._instance = super(StoryDataRepository, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.database = Neo4J()

    def get(self, story_id: str) -> StoryData:
        with self.database.driver.session() as session:
            result = session.run("MATCH (storyData:StoryData {id: $story_id})-[:STARTED_AT]->(storyChunk:StoryChunk) RETURN storyData, storyChunk", story_id=story_id)
            record = result.single()

            if record is None:
                raise Exception("Story not found")
            
            data = record.data()
            story_data_obj = data["storyData"]
            story_chunk_obj = data["storyChunk"]
            return StoryData(
                id=story_data_obj["id"],
                title=story_data_obj["title"],
                genre=story_data_obj["genre"],
                themes=story_data_obj["themes"],
                main_scenes=[SceneData.from_json(s) for s in json.loads(story_data_obj["main_scenes"])],
                main_characters=[CharacterData.from_json(c) for c in json.loads(story_data_obj["main_characters"])],
                synopsis=story_data_obj["synopsis"],
                chapter_synopses=[ChapterSynopsis.from_json(s) for s in json.loads(story_data_obj["chapter_synopses"])],
                beginning=story_data_obj["beginning"],
                endings=[EndingData.from_json(e) for e in json.loads(story_data_obj["endings"])],
                start_chunk=StoryChunk.from_json(story_chunk_obj),
            )
