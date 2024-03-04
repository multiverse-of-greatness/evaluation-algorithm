from ..databases import Neo4J
from ..structs.story_chunk import StoryChunk
from ..structs.story_choice import StoryChoice


class StoryChunkRepository:
    def __init__(self, db: Neo4J) -> None:
        self.db = db

    def get(self, chunk_id: str) -> StoryChunk:
        with self.db.driver.session() as session:
            result = session.run("MATCH (chunk:StoryChunk {id: $chunk_id}) RETURN chunk", chunk_id=chunk_id)
            record = result.single()

            if record is None:
                raise Exception("Chunk not found")
            
            data = record.data()
            chunk_obj = data["chunk"]
            return StoryChunk.from_json(chunk_obj)
        
    def get_branched_chunks(self, chunk_id: str) -> list[StoryChunk]:
        chunks = []
        with self.db.driver.session() as session:
            results = session.run("MATCH (StoryChunk {id: $chunk_id})-[:BRANCHED_TO]->(target:StoryChunk) RETURN target", chunk_id=chunk_id)

            for record in results:
                chunk_obj = record["target"]
                chunks.append(StoryChunk.from_json(chunk_obj))

        return chunks
    
    def list_choices(self, chunk_id: str) -> list[StoryChoice]:
        choices = []
        with self.db.driver.session() as session:
            query = "MATCH (StoryChunk {id: $chunk_id})-[b:BRANCHED_TO]->() RETURN PROPERTIES(b)"
            results = session.run(query, chunk_id=chunk_id)

            for record in results:
                choice_obj = record["PROPERTIES(b)"]
                if not bool(choice_obj):
                    raise Exception("No choices found")
                
                choices.append(StoryChoice.from_json(choice_obj))

        return choices

    def find_next(self, chunk_id: str, choice_id: int = None) -> StoryChunk:
        with self.db.driver.session() as session:
            if choice_id:
                query = "MATCH (StoryChunk {id: $chunk_id})-[b:BRANCHED_TO]->(target:StoryChunk) WHERE PROPERTIES(b).id = $choice_id RETURN target"
                parameters = {'chunk_id': chunk_id, 'choice_id': choice_id}
            else:
                query = "MATCH (StoryChunk {id: $chunk_id})-[b:BRANCHED_TO]->(target:StoryChunk) RETURN target"
                parameters = {'chunk_id': chunk_id}

            results = session.run(query, **parameters)
            records = results.data()

            if not records:
                raise Exception("No choice found with given choice_id" if choice_id else "No choices found")
            if not choice_id and len(records) > 1:
                raise Exception("Multiple choices found, please specify choice_id")

            chunk_obj = records[0]["target"]
            return StoryChunk.from_json(chunk_obj)
