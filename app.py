import tempfile

import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network

from config.database import db
from services.career_service import get_career_matches

from services.graph_service import (
    get_career_routes,
    get_role_skill_gap,
    get_graph_data,
    get_project_recommendations,
    get_dashboard_metrics,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="PathGraph AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

.stApp {
    background:
        radial-gradient(
            circle at 80% 10%,
            rgba(98, 72, 255, 0.12),
            transparent 25%
        ),
        linear-gradient(
            135deg,
            #080c16 0%,
            #10182a 50%,
            #090e1a 100%
        );
}

.main .block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1280px;
}

.hero {
    padding: 42px;
    border-radius: 26px;
    background:
        radial-gradient(
            circle at top right,
            rgba(112, 70, 255, 0.34),
            transparent 38%
        ),
        linear-gradient(
            135deg,
            rgba(28, 38, 67, 0.98),
            rgba(13, 18, 33, 0.98)
        );
    border: 1px solid rgba(255,255,255,0.10);
    box-shadow: 0 20px 70px rgba(0,0,0,0.38);
    margin-bottom: 28px;
}

.hero-badge {
    display: inline-block;
    padding: 7px 13px;
    border-radius: 999px;
    background: rgba(120, 95, 255, 0.14);
    border: 1px solid rgba(142, 123, 255, 0.28);
    color: #c7bcff;
    font-size: 13px;
    font-weight: 650;
    margin-bottom: 16px;
}

.hero-title {
    font-size: 48px;
    font-weight: 820;
    letter-spacing: -1.3px;
    line-height: 1.13;
    color: white;
    max-width: 900px;
}

.hero-highlight {
    background: linear-gradient(
        90deg,
        #9a85ff,
        #5fd8ff
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    font-size: 18px;
    color: #aebbd2;
    max-width: 780px;
    line-height: 1.7;
    margin-top: 17px;
}

.section-title {
    font-size: 29px;
    font-weight: 760;
    margin-top: 20px;
    margin-bottom: 5px;
}

.section-text {
    color: #98a6c0;
    font-size: 15px;
    line-height: 1.6;
    margin-bottom: 22px;
}

div[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        rgba(26,35,58,0.85),
        rgba(14,20,35,0.85)
    );
    border: 1px solid rgba(255,255,255,0.08);
    padding: 17px;
    border-radius: 18px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.20);
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(
        145deg,
        rgba(19,27,47,0.90),
        rgba(12,18,31,0.90)
    );
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 10px 32px rgba(0,0,0,0.22);
}

div.stButton > button {
    border-radius: 14px;
    min-height: 49px;
    font-weight: 700;
    font-size: 16px;
}

div[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #080d17,
        #0b111e
    );
    border-right: 1px solid rgba(255,255,255,0.07);
}

.route-box {
    padding: 20px 22px;
    border-radius: 17px;
    background: linear-gradient(
        135deg,
        rgba(77,60,170,0.15),
        rgba(29,42,69,0.50)
    );
    border: 1px solid rgba(142,123,255,0.18);
    margin-bottom: 12px;
}

.route-path {
    color: #e8e8ff;
    font-size: 17px;
    font-weight: 600;
    line-height: 1.7;
}

.route-meta {
    color: #8998b4;
    font-size: 13px;
    margin-top: 7px;
}

.skill-tag {
    display: inline-block;
    padding: 6px 10px;
    margin: 3px 4px 3px 0;
    border-radius: 999px;
    background: rgba(72,190,140,0.10);
    border: 1px solid rgba(72,190,140,0.22);
    color: #92e6bd;
    font-size: 13px;
}

.gap-tag {
    display: inline-block;
    padding: 6px 10px;
    margin: 3px 4px 3px 0;
    border-radius: 999px;
    background: rgba(255,177,70,0.10);
    border: 1px solid rgba(255,177,70,0.22);
    color: #ffc978;
    font-size: 13px;
}

.small-muted {
    color: #73829d;
    font-size: 13px;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# DATABASE STATUS
# ============================================================

status = db.test_connection()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("## 🧠 PathGraph AI")
    st.caption("Career Intelligence Platform")

    st.divider()

    st.markdown("### Navigation")
    st.markdown("🏠 **Dashboard**")
    st.markdown("🎯 Career Match")
    st.markdown("🧩 Skill Gap")
    st.markdown("🗺️ Career Routes")
    st.markdown("🌐 Graph Explorer")
    st.markdown("💼 Project Finder")

    st.divider()

    st.markdown("### System")

    if status["success"]:
        st.success("● CognoDB Connected")
    else:
        st.error("● Database Offline")

    st.caption("Graph database • Bolt protocol")


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
<div class="hero">
<div class="hero-badge">
◆ GRAPH-POWERED CAREER INTELLIGENCE
</div>

<div class="hero-title">
Navigate your career with
<span class="hero-highlight">graph intelligence.</span>
</div>

<div class="hero-subtitle">
PathGraph AI maps the relationships between your skills,
career roles, projects and learning prerequisites to reveal
the shortest path from where you are today to where you
want to be.
</div>
</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# DATABASE FAILURE
# ============================================================

if not status["success"]:
    st.error(
        "PathGraph AI cannot reach the career graph right now."
    )

    st.info(
        "Check the CognoDB instance and your connection "
        "configuration, then try again."
    )

    st.stop()


# ============================================================
# LIVE DASHBOARD METRICS
# ============================================================

metrics = get_dashboard_metrics()

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(
        "Graph Skills",
        metrics["skills"],
    )

with m2:
    st.metric(
        "Career Roles",
        metrics["roles"],
    )

with m3:
    st.metric(
        "Career Domains",
        metrics["domains"],
    )

with m4:
    st.metric(
        "Project Paths",
        metrics["projects"],
    )

st.caption(
    "Live graph counts retrieved directly from CognoDB."
)

st.markdown(
    "<br>",
    unsafe_allow_html=True,
)


# ============================================================
# AVAILABLE DATA
# ============================================================

available_skills = [
    "Python",
    "Java",
    "SQL",
    "JavaScript",
    "React",
    "Django",
    "Flask",
    "Machine Learning",
    "Deep Learning",
    "TensorFlow",
    "PyTorch",
    "OpenCV",
    "YOLO",
    "Computer Vision",
    "LLMs",
    "RAG",
    "LangChain",
    "Vector Databases",
    "AWS",
    "Docker",
    "Git",
    "REST APIs",
    "Data Structures",
]

career_roles = [
    "Computer Vision Engineer",
    "Machine Learning Engineer",
    "GenAI Engineer",
    "Backend Developer",
    "Full-Stack Developer",
    "Data Scientist",
]


# ============================================================
# CAREER MATCH
# ============================================================

st.markdown(
    """
<div class="section-title">
🎯 Career Match Intelligence
</div>

<div class="section-text">
Select your current skills and PathGraph AI will query
the career graph to discover which roles have the strongest
relationship with your existing technical profile.
</div>
""",
    unsafe_allow_html=True,
)

selected_skills = st.multiselect(
    "Your current skills",
    available_skills,
    placeholder="Select Python, Machine Learning, OpenCV...",
)

analyze = st.button(
    "✨ Analyze My Career Graph",
    type="primary",
    use_container_width=True,
)

if analyze:
    if not selected_skills:
        st.warning(
            "Select at least one skill before starting the analysis."
        )

    else:
        with st.spinner(
            "Traversing your career graph and ranking opportunities..."
        ):
            careers = get_career_matches(
                selected_skills
            )

        if not careers:
            st.info(
                "No career matches were found."
            )

        else:
            top = careers[0]

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown(
                "## ⭐ Your Strongest Career Signal"
            )

            a, b, c = st.columns([2, 1, 1])

            with a:
                st.metric(
                    "Top Career",
                    top["role"],
                )

            with b:
                st.metric(
                    "Match Score",
                    f"{top['match_percentage']}%",
                )

            with c:
                st.metric(
                    "Skills Matched",
                    f"{top['total_matched']}/{top['total_required']}",
                )

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown(
                "## Career Match Rankings"
            )

            for index, career in enumerate(
                careers[:5],
                start=1,
            ):
                with st.container(border=True):
                    left, right = st.columns([4, 1])

                    with left:
                        if index == 1:
                            badge = "🏆"
                        elif index == 2:
                            badge = "🥈"
                        elif index == 3:
                            badge = "🥉"
                        else:
                            badge = "◆"

                        st.markdown(
                            f"### {badge} {career['role']}"
                        )

                        st.progress(
                            career["match_percentage"] / 100
                        )

                        st.caption(
                            f"{career['total_matched']} of "
                            f"{career['total_required']} required "
                            f"skills matched"
                        )

                    with right:
                        st.metric(
                            "Match",
                            f"{career['match_percentage']}%",
                        )

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(
                            "#### ✅ Existing Strengths"
                        )

                        if career["matched_skills"]:
                            for skill in career["matched_skills"]:
                                st.markdown(
                                    f"✓ {skill}"
                                )

                        else:
                            st.caption(
                                "No required skills matched yet."
                            )

                    with col2:
                        st.markdown(
                            "#### ⚡ Skill Gaps"
                        )

                        if career["missing_skills"]:
                            for skill in career["missing_skills"]:
                                st.markdown(
                                    f"→ {skill}"
                                )

                        else:
                            st.success(
                                "Full skill alignment"
                            )

                    if career["missing_skills"]:
                        st.info(
                            "Recommended next focus: "
                            f"**{career['missing_skills'][0]}**"
                        )


# ============================================================
# SKILL GAP
# ============================================================

st.markdown(
    "<br><br>",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="section-title">
🧩 Skill Gap Intelligence
</div>

<div class="section-text">
Choose a target career and compare its graph-connected
requirements against your current skills.
</div>
""",
    unsafe_allow_html=True,
)

gap_col1, gap_col2 = st.columns([1, 2])

with gap_col1:
    target_role = st.selectbox(
        "Target career",
        career_roles,
    )

with gap_col2:
    gap_skills = st.multiselect(
        "Skills you currently have",
        available_skills,
        default=selected_skills,
        key="gap_skills",
    )

gap_button = st.button(
    "🧠 Analyze Skill Gap",
    use_container_width=True,
)

if gap_button:
    with st.spinner(
        "Comparing your skills with the target career graph..."
    ):
        gap = get_role_skill_gap(
            target_role,
            gap_skills,
        )

    if not gap:
        st.warning(
            "Unable to analyze this career."
        )

    else:
        readiness = gap["readiness"]

        st.markdown("<br>", unsafe_allow_html=True)

        g1, g2, g3, g4 = st.columns(4)

        with g1:
            st.metric(
                "Career Readiness",
                f"{readiness}%",
            )

        with g2:
            st.metric(
                "Skills Matched",
                gap["total_matched"],
            )

        with g3:
            st.metric(
                "Skills Missing",
                len(gap["missing_skills"]),
            )

        with g4:
            st.metric(
                "Total Requirements",
                gap["total_required"],
            )

        st.markdown(
            f"### 🎯 {target_role}"
        )

        st.progress(
            readiness / 100
        )

        strength_col, missing_col = st.columns(2)

        with strength_col:
            with st.container(border=True):
                st.markdown(
                    "### ✅ Existing Strengths"
                )

                if gap["matched_skills"]:
                    tags = ""

                    for skill in gap["matched_skills"]:
                        tags += (
                            '<span class="skill-tag">'
                            + skill
                            + "</span>"
                        )

                    st.markdown(
                        tags,
                        unsafe_allow_html=True,
                    )

        with missing_col:
            with st.container(border=True):
                st.markdown(
                    "### ⚡ Skills to Develop"
                )

                if gap["missing_skills"]:
                    tags = ""

                    for skill in gap["missing_skills"]:
                        tags += (
                            '<span class="gap-tag">'
                            + skill
                            + "</span>"
                        )

                    st.markdown(
                        tags,
                        unsafe_allow_html=True,
                    )

                else:
                    st.success(
                        "Full skill alignment"
                    )

        if gap["missing_skills"]:
            st.info(
                "💡 **Recommended next skill:** "
                f"{gap['missing_skills'][0]}"
            )


# ============================================================
# CAREER ROUTES
# ============================================================

st.markdown(
    "<br><br>",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="section-title">
🗺️ Career Route Explorer
</div>

<div class="section-text">
Explore learning routes by traversing PREREQUISITE_OF
relationships across multiple hops.
</div>
""",
    unsafe_allow_html=True,
)

route_start_skill = st.selectbox(
    "Start from a skill",
    available_skills,
    key="route_start_skill",
)

route_button = st.button(
    "🗺️ Discover Learning Routes",
    use_container_width=True,
)

if route_button:
    with st.spinner(
        "Traversing multi-hop skill relationships..."
    ):
        routes = get_career_routes(
            route_start_skill
        )

    if not routes:
        st.info(
            "No downstream learning routes were found."
        )

    else:
        longest_route = max(
            routes,
            key=lambda item: item["hops"],
        )

        r1, r2, r3 = st.columns(3)

        with r1:
            st.metric(
                "Routes Found",
                len(routes),
            )

        with r2:
            st.metric(
                "Maximum Depth",
                f"{longest_route['hops']} hops",
            )

        with r3:
            st.metric(
                "Deepest Target",
                longest_route["target_skill"],
            )

        for route_data in routes:
            route_text = (
                " &nbsp; → &nbsp; ".join(
                    route_data["route"]
                )
            )

            hops = route_data["hops"]

            route_type = (
                "Multi-hop graph traversal"
                if hops >= 2
                else "Direct relationship"
            )

            st.markdown(
                f"""
<div class="route-box">
<div class="route-path">
{route_text}
</div>
<div class="route-meta">
{hops} hop{"s" if hops != 1 else ""}
• {route_type}
</div>
</div>
""",
                unsafe_allow_html=True,
            )


# ============================================================
# INTERACTIVE GRAPH EXPLORER
# ============================================================

st.markdown(
    "<br><br>",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="section-title">
🌐 Interactive Graph Explorer
</div>

<div class="section-text">
Explore the live CognoDB graph containing skills, career
roles, projects and domains.
</div>
""",
    unsafe_allow_html=True,
)

graph_button = st.button(
    "🌐 Load Interactive Career Graph",
    use_container_width=True,
)

if graph_button:
    with st.spinner(
        "Loading live graph data from CognoDB..."
    ):
        graph_data = get_graph_data()

    if not graph_data["nodes"]:
        st.warning(
            "No graph data is currently available."
        )

    else:
        gm1, gm2 = st.columns(2)

        with gm1:
            st.metric(
                "Graph Nodes",
                len(graph_data["nodes"]),
            )

        with gm2:
            st.metric(
                "Relationships",
                len(graph_data["edges"]),
            )

        network = Network(
            height="650px",
            width="100%",
            bgcolor="#0b1020",
            font_color="#ffffff",
            directed=True,
        )

        for node in graph_data["nodes"]:
            node_type = node["type"]

            if node_type == "Skill":
                node_color = "#6C63FF"
                node_shape = "dot"
                node_size = 20

            elif node_type == "JobRole":
                node_color = "#00B8D9"
                node_shape = "diamond"
                node_size = 28

            elif node_type == "Project":
                node_color = "#2ECC71"
                node_shape = "box"
                node_size = 25

            elif node_type == "CareerDomain":
                node_color = "#F5A623"
                node_shape = "hexagon"
                node_size = 30

            else:
                node_color = "#8A94A6"
                node_shape = "dot"
                node_size = 18

            network.add_node(
                node["id"],
                label=node["label"],
                title=(
                    f"<b>{node['label']}</b>"
                    f"<br>Type: {node_type}"
                ),
                color=node_color,
                shape=node_shape,
                size=node_size,
            )

        for edge in graph_data["edges"]:
            network.add_edge(
                edge["source"],
                edge["target"],
                label=edge["relationship"],
                title=edge["relationship"],
            )

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".html",
            mode="w",
            encoding="utf-8",
        ) as temp_file:
            temp_path = temp_file.name

        network.save_graph(
            temp_path
        )

        with open(
            temp_path,
            "r",
            encoding="utf-8",
        ) as html_file:
            graph_html = html_file.read()

        components.html(
            graph_html,
            height=680,
            scrolling=False,
        )


# ============================================================
# PROJECT FINDER
# ============================================================

st.markdown(
    "<br><br>",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="section-title">
💼 Project Finder
</div>

<div class="section-text">
Find portfolio projects by traversing
Project → USES → Skill relationships.
</div>
""",
    unsafe_allow_html=True,
)

project_skills = st.multiselect(
    "Select skills for project recommendations",
    available_skills,
    default=selected_skills,
    key="project_skills",
)

project_button = st.button(
    "🚀 Find Portfolio Projects",
    use_container_width=True,
)

if project_button:
    if not project_skills:
        st.warning(
            "Select at least one skill."
        )

    else:
        with st.spinner(
            "Traversing project-skill relationships..."
        ):
            projects = get_project_recommendations(
                project_skills
            )

        if not projects:
            st.info(
                "No matching projects were found."
            )

        else:
            top_project = projects[0]

            p1, p2, p3 = st.columns([2, 1, 1])

            with p1:
                st.metric(
                    "Recommended Project",
                    top_project["project"],
                )

            with p2:
                st.metric(
                    "Skill Match",
                    f"{top_project['match_percentage']}%",
                )

            with p3:
                st.metric(
                    "Skills Covered",
                    (
                        f"{top_project['matched_count']}/"
                        f"{top_project['total_skills']}"
                    ),
                )

            for index, project in enumerate(
                projects,
                start=1,
            ):
                with st.container(border=True):
                    st.markdown(
                        f"### {index}. {project['project']}"
                    )

                    st.progress(
                        project["match_percentage"] / 100
                    )

                    st.caption(
                        f"{project['matched_count']} of "
                        f"{project['total_skills']} "
                        f"project skills matched"
                    )

                    left, right = st.columns(2)

                    with left:
                        st.markdown(
                            "#### ✅ Skills You Have"
                        )

                        for skill in project["matched_skills"]:
                            st.markdown(
                                f"✓ {skill}"
                            )

                    with right:
                        st.markdown(
                            "#### 📚 Skills You Would Learn"
                        )

                        for skill in project["missing_skills"]:
                            st.markdown(
                                f"→ {skill}"
                            )


# ============================================================
# WHY GRAPH DATABASE
# ============================================================

st.markdown(
    "<br><br>",
    unsafe_allow_html=True,
)

with st.expander(
    "💡 Why does PathGraph AI use a graph database?"
):
    st.markdown(
        """
PathGraph AI models career development as connected knowledge.

Skills can be prerequisites for other skills, required by
multiple careers, and used by multiple projects.

For example:

**Python → Machine Learning → Deep Learning → Computer Vision**

Variable-length graph traversal makes these connected paths
natural to query with Cypher.

PathGraph AI communicates with CognoDB using parameterized
Cypher queries through the official Neo4j Python driver.
"""
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    "<br><br>",
    unsafe_allow_html=True,
)

st.divider()

st.markdown(
    """
<div class="small-muted">
PathGraph AI • Graph-powered career intelligence •
Powered by CognoDB
</div>
""",
    unsafe_allow_html=True,
)