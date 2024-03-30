import os
from neo4j import GraphDatabase


class Neo4J:
    def __init__(self):
        uri = os.getenv("NEO4J_URI")
        username, password = os.getenv("NEO4J_AUTH").split("/")
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def close(self):
        self.driver.close()
