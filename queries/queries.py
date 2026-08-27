# ============================================================
# PathGraph AI - Cypher Queries
# ============================================================


# ------------------------------------------------------------
# 1. CAREER MATCH QUERY
# ------------------------------------------------------------

CAREER_MATCH_QUERY = """
MATCH (role:JobRole)-[:REQUIRES]->(required:Skill)

WITH
    role,
    collect(required.name) AS required_skills

WITH
    role,
    required_skills,
    [
        skill IN required_skills
        WHERE skill IN $user_skills
    ] AS matched_skills

RETURN
    role.name AS role,
    required_skills,
    matched_skills,
    size(required_skills) AS total_required,
    size(matched_skills) AS total_matched,
    round(
        100.0 * size(matched_skills) /
        size(required_skills)
    ) AS match_percentage

ORDER BY
    match_percentage DESC,
    role ASC
"""


# ------------------------------------------------------------
# 2. CAREER ROUTE QUERY
# ------------------------------------------------------------

CAREER_ROUTE_QUERY = """
MATCH path =
    (start:Skill {name: $start_skill})
    -[:PREREQUISITE_OF*1..4]->
    (target:Skill)

RETURN
    [node IN nodes(path) | node.name] AS route,
    target.name AS target_skill,
    length(path) AS hops

ORDER BY
    hops ASC,
    target_skill ASC

LIMIT 20
"""


# ------------------------------------------------------------
# 3. ROLE SKILL GAP QUERY
# ------------------------------------------------------------

ROLE_SKILL_GAP_QUERY = """
MATCH
    (role:JobRole {name: $role_name})
    -[:REQUIRES]->
    (skill:Skill)

WITH
    collect(skill.name) AS required_skills

RETURN
    required_skills,

    [
        skill IN required_skills
        WHERE skill IN $user_skills
    ] AS matched_skills,

    [
        skill IN required_skills
        WHERE NOT skill IN $user_skills
    ] AS missing_skills
"""


# ------------------------------------------------------------
# 4. GRAPH EXPLORER QUERY
# ------------------------------------------------------------

GRAPH_EXPLORER_QUERY = """
MATCH (source)-[rel]->(target)

WHERE
    (
        source:Skill
        OR source:JobRole
        OR source:Project
        OR source:CareerDomain
    )
    AND
    (
        target:Skill
        OR target:JobRole
        OR target:Project
        OR target:CareerDomain
    )

RETURN
    labels(source)[0] AS source_type,
    source.name AS source_name,
    type(rel) AS relationship,
    labels(target)[0] AS target_type,
    target.name AS target_name

ORDER BY
    source_type,
    source_name,
    relationship,
    target_name

LIMIT 200
"""


# ------------------------------------------------------------
# 5. PROJECT FINDER QUERY
# ------------------------------------------------------------

PROJECT_FINDER_QUERY = """
MATCH (project:Project)-[:USES]->(skill:Skill)

WITH
    project,
    collect(skill.name) AS project_skills

WITH
    project,
    project_skills,
    [
        skill IN project_skills
        WHERE skill IN $user_skills
    ] AS matched_skills

RETURN
    project.name AS project,
    project_skills,
    matched_skills,

    [
        skill IN project_skills
        WHERE NOT skill IN $user_skills
    ] AS missing_skills,

    size(project_skills) AS total_skills,
    size(matched_skills) AS matched_count,

    round(
        100.0 * size(matched_skills) /
        size(project_skills)
    ) AS match_percentage

ORDER BY
    match_percentage DESC,
    project ASC
"""


# ------------------------------------------------------------
# 6. DASHBOARD METRICS QUERY
# ------------------------------------------------------------

DASHBOARD_METRICS_QUERY = """
CALL {
    MATCH (s:Skill)
    RETURN count(s) AS skill_count
}

CALL {
    MATCH (r:JobRole)
    RETURN count(r) AS role_count
}

CALL {
    MATCH (d:CareerDomain)
    RETURN count(d) AS domain_count
}

CALL {
    MATCH (p:Project)
    RETURN count(p) AS project_count
}

RETURN
    skill_count,
    role_count,
    domain_count,
    project_count
"""