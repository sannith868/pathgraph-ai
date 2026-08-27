import json
from pathlib import Path

from config.database import db


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "seed_data.json"


def load_seed_data():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def seed_database():
    data = load_seed_data()
    driver = db.connect()

    with driver.session() as session:

        # ----------------------------
        # Skills
        # ----------------------------
        for skill in data["skills"]:
            session.run(
                """
                MERGE (s:Skill {name: $name})
                """,
                name=skill,
            )

        # ----------------------------
        # Career domains
        # ----------------------------
        for domain in data["career_domains"]:
            session.run(
                """
                MERGE (d:CareerDomain {name: $name})
                """,
                name=domain,
            )

        # ----------------------------
        # Job roles
        # ----------------------------
        for role in data["job_roles"]:

            session.run(
                """
                MERGE (r:JobRole {name: $role_name})
                """,
                role_name=role["name"],
            )

            session.run(
                """
                MATCH (r:JobRole {name: $role_name})
                MATCH (d:CareerDomain {name: $domain})
                MERGE (r)-[:BELONGS_TO]->(d)
                """,
                role_name=role["name"],
                domain=role["domain"],
            )

            for skill in role["required_skills"]:
                session.run(
                    """
                    MATCH (r:JobRole {name: $role_name})
                    MATCH (s:Skill {name: $skill_name})
                    MERGE (r)-[:REQUIRES]->(s)
                    """,
                    role_name=role["name"],
                    skill_name=skill,
                )

        # ----------------------------
        # Projects
        # ----------------------------
        for project in data["projects"]:

            session.run(
                """
                MERGE (p:Project {name: $name})
                """,
                name=project["name"],
            )

            for skill in project["skills"]:
                session.run(
                    """
                    MATCH (p:Project {name: $project_name})
                    MATCH (s:Skill {name: $skill_name})
                    MERGE (p)-[:USES]->(s)
                    """,
                    project_name=project["name"],
                    skill_name=skill,
                )

        # ----------------------------
        # Skill prerequisites
        # ----------------------------
        for source_skill, target_skill in data["skill_prerequisites"]:

            session.run(
                """
                MATCH (source:Skill {name: $source})
                MATCH (target:Skill {name: $target})
                MERGE (source)-[:PREREQUISITE_OF]->(target)
                """,
                source=source_skill,
                target=target_skill,
            )

    print("✅ PathGraph AI seed data loaded successfully!")


if __name__ == "__main__":
    seed_database()