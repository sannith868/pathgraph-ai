import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()


class Database:
    def __init__(self):
        self.uri = os.getenv("COGNODB_URI")
        self.user = os.getenv("COGNODB_USER")
        self.password = os.getenv("COGNODB_PASSWORD")
        self.driver = None

    def connect(self):
        if not self.uri or not self.user or not self.password:
            raise ValueError(
                "CognoDB credentials are missing. Check your .env file."
            )

        self.driver = GraphDatabase.driver(
            self.uri,
            auth=(self.user, self.password),
        )

        self.driver.verify_connectivity()

        return self.driver

    def test_connection(self):
        try:
            driver = self.connect()

            with driver.session() as session:
                result = session.run(
                    "RETURN 'PathGraph AI connected successfully!' AS message"
                )

                record = result.single()

                return {
                    "success": True,
                    "message": record["message"],
                }

        except Exception as error:
            return {
                "success": False,
                "message": str(error),
            }

    def close(self):
        if self.driver:
            self.driver.close()


db = Database()