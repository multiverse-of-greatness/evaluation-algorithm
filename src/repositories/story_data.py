import json

from ..databases import Neo4J
from ..structs.chapter_synopsis import ChapterSynopsis
from ..structs.character_data import CharacterData
from ..structs.ending_data import EndingData
from ..structs.scene_data import SceneData
from ..structs.story_chunk import StoryChunk
from ..structs.story_data import StoryData


class StoryDataRepository:
    def __init__(self, database: Neo4J) -> None:
        self.database = database

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
