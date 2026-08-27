from config.database import db

from queries.queries import (
    CAREER_ROUTE_QUERY,
    ROLE_SKILL_GAP_QUERY,
    GRAPH_EXPLORER_QUERY,
    PROJECT_FINDER_QUERY,
    DASHBOARD_METRICS_QUERY,
)


# ============================================================
# CAREER ROUTE SERVICE
# ============================================================

def get_career_routes(start_skill):
    if not start_skill:
        return []

    try:
        driver = db.connect()

        with driver.session() as session:
            result = session.run(
                CAREER_ROUTE_QUERY,
                start_skill=start_skill,
            )

            routes = []

            for record in result:
                routes.append(
                    {
                        "route": list(record["route"] or []),
                        "target_skill": record["target_skill"],
                        "hops": record["hops"],
                    }
                )

            return routes

    except Exception as error:
        print(f"Career route error: {error}")
        return []


# ============================================================
# SKILL GAP SERVICE
# ============================================================

def get_role_skill_gap(role_name, user_skills):
    if not role_name:
        return None

    if user_skills is None:
        user_skills = []

    try:
        driver = db.connect()

        with driver.session() as session:
            result = session.run(
                ROLE_SKILL_GAP_QUERY,
                role_name=role_name,
                user_skills=user_skills,
            )

            record = result.single()

            if not record:
                return None

            required_skills = list(
                record["required_skills"] or []
            )

            matched_skills = list(
                record["matched_skills"] or []
            )

            missing_skills = list(
                record["missing_skills"] or []
            )

            total_required = len(required_skills)
            total_matched = len(matched_skills)

            if total_required > 0:
                readiness = int(
                    (total_matched * 100 / total_required) + 0.5
                )
            else:
                readiness = 0

            return {
                "role": role_name,
                "required_skills": required_skills,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "total_required": total_required,
                "total_matched": total_matched,
                "readiness": readiness,
            }

    except Exception as error:
        print(f"Skill gap error: {error}")
        return None


# ============================================================
# GRAPH EXPLORER SERVICE
# ============================================================

def get_graph_data():
    try:
        driver = db.connect()

        with driver.session() as session:
            result = session.run(
                GRAPH_EXPLORER_QUERY
            )

            nodes = {}
            edges = []

            for record in result:
                source_name = record["source_name"]
                source_type = record["source_type"]

                target_name = record["target_name"]
                target_type = record["target_type"]

                relationship = record["relationship"]

                if not source_name or not target_name:
                    continue

                source_id = f"{source_type}:{source_name}"
                target_id = f"{target_type}:{target_name}"

                if source_id not in nodes:
                    nodes[source_id] = {
                        "id": source_id,
                        "label": source_name,
                        "type": source_type,
                    }

                if target_id not in nodes:
                    nodes[target_id] = {
                        "id": target_id,
                        "label": target_name,
                        "type": target_type,
                    }

                edges.append(
                    {
                        "source": source_id,
                        "target": target_id,
                        "relationship": relationship,
                    }
                )

            return {
                "nodes": list(nodes.values()),
                "edges": edges,
            }

    except Exception as error:
        print(f"Graph explorer error: {error}")

        return {
            "nodes": [],
            "edges": [],
        }


# ============================================================
# PROJECT FINDER SERVICE
# ============================================================

def get_project_recommendations(user_skills):
    if not user_skills:
        return []

    try:
        driver = db.connect()

        with driver.session() as session:
            result = session.run(
                PROJECT_FINDER_QUERY,
                user_skills=user_skills,
            )

            projects = []

            for record in result:
                projects.append(
                    {
                        "project": record["project"],
                        "project_skills": list(
                            record["project_skills"] or []
                        ),
                        "matched_skills": list(
                            record["matched_skills"] or []
                        ),
                        "missing_skills": list(
                            record["missing_skills"] or []
                        ),
                        "total_skills": record["total_skills"],
                        "matched_count": record["matched_count"],
                        "match_percentage": int(
                            record["match_percentage"]
                        ),
                    }
                )

            return projects

    except Exception as error:
        print(f"Project finder error: {error}")
        return []


# ============================================================
# DASHBOARD METRICS SERVICE
# ============================================================

def get_dashboard_metrics():
    """
    Return live node counts from CognoDB.
    """

    try:
        driver = db.connect()

        with driver.session() as session:
            result = session.run(
                DASHBOARD_METRICS_QUERY
            )

            record = result.single()

            if not record:
                return {
                    "skills": 0,
                    "roles": 0,
                    "domains": 0,
                    "projects": 0,
                }

            return {
                "skills": record["skill_count"],
                "roles": record["role_count"],
                "domains": record["domain_count"],
                "projects": record["project_count"],
            }

    except Exception as error:
        print(f"Dashboard metrics error: {error}")

        return {
            "skills": 0,
            "roles": 0,
            "domains": 0,
            "projects": 0,
        }