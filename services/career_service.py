from config.database import db
from queries.queries import CAREER_MATCH_QUERY


def get_career_matches(user_skills):
    if not user_skills:
        return []

    try:
        driver = db.connect()

        with driver.session() as session:
            result = session.run(
                CAREER_MATCH_QUERY,
                user_skills=user_skills
            )

            careers = []

            for record in result:
                required = record["required_skills"]
                matched = record["matched_skills"]

                missing = [
                    skill
                    for skill in required
                    if skill not in matched
                ]

                careers.append({
                    "role": record["role"],
                    "match_percentage": int(
                        record["match_percentage"]
                    ),
                    "matched_skills": matched,
                    "missing_skills": missing,
                    "total_required": record["total_required"],
                    "total_matched": record["total_matched"],
                })

            return careers

    except Exception as error:
        print(f"Career matching error: {error}")
        return []