# 🧠 PathGraph AI

### Graph-Powered Career Intelligence Platform

PathGraph AI is an interactive career intelligence application built with **Python, Streamlit, Cypher, and CognoDB**.

Instead of treating skills, careers, projects, and learning paths as isolated records, PathGraph AI models them as a connected knowledge graph. Users can analyze career compatibility, discover skill gaps, explore multi-hop learning routes, visualize the graph, and identify portfolio projects based on their existing skills.

---

## 🚀 Live Demo

> Deployment URL will be added after deployment.

---

## 🎥 Demo Video

> Screen-recording URL will be added after recording.

---

## ✨ Key Features

### 🎯 Career Match Intelligence

Users select their current technical skills and PathGraph AI compares them with skills required by career roles stored in CognoDB.

The system returns:

- Career match percentage
- Matched skills
- Missing skills
- Total required skills
- Ranked career recommendations
- Recommended next skill to learn

---

### 🧩 Skill Gap Intelligence

Users can select a target career such as:

- Computer Vision Engineer
- Machine Learning Engineer
- GenAI Engineer
- Data Scientist
- Backend Developer
- Full-Stack Developer

PathGraph AI identifies the difference between the user's current skills and the skills required for the selected career.

The application calculates a **Career Readiness Score** and highlights both existing strengths and missing capabilities.

---

### 🗺️ Multi-Hop Career Route Explorer

PathGraph AI uses graph traversal to discover learning paths between skills.

Example:

```text
Python
   ↓
Machine Learning
   ↓
Deep Learning
   ↓
Computer Vision
```

This is represented using:

```text
(:Skill)-[:PREREQUISITE_OF]->(:Skill)
```

The application supports multi-hop traversal, allowing it to discover indirect learning relationships rather than only direct connections.

---

### 🌐 Interactive Graph Explorer

The application includes an interactive visualization of the live CognoDB graph.

Users can:

- Drag nodes
- Zoom into the graph
- Explore relationships
- Inspect skills
- Inspect career roles
- Inspect projects
- Inspect career domains

The visualization is generated using **PyVis** from data retrieved directly from CognoDB.

---

### 💼 Project Finder

PathGraph AI connects technical skills to portfolio projects.

The system traverses:

```text
(Project)-[:USES]->(Skill)
```

and ranks projects according to the user's existing skill set.

For every recommendation, the application shows:

- Project match percentage
- Skills already available
- Skills that can be learned
- Total skill coverage

This turns career analysis into an actionable portfolio-building recommendation.

---

## 🧠 Why a Graph Database?

Career development is naturally a connected problem.

A single skill may:

- Be required by multiple career roles
- Be used by multiple projects
- Depend on another skill
- Lead toward several different career paths

For example:

```text
Python
   ↓
Machine Learning
   ↓
Deep Learning
   ↓
Computer Vision
```

In a traditional relational database, discovering variable-length learning paths can require multiple joins and additional recursive logic.

A graph database represents these relationships directly.

With CognoDB and Cypher, PathGraph AI can express questions such as:

> Which careers best match my skills?

> Which skills am I missing for a particular career?

> What can I learn after Python?

> What multi-hop path leads from Python to Computer Vision?

> Which projects can I build using my existing skills?

These questions map naturally to graph traversal.

---

# 🕸️ Graph Data Model

PathGraph AI uses four primary node types:

### Skill

Represents a technical capability.

Examples:

```text
Python
Machine Learning
Deep Learning
TensorFlow
PyTorch
OpenCV
YOLO
RAG
LangChain
Docker
```

### JobRole

Represents a career target.

Examples:

```text
Computer Vision Engineer
Machine Learning Engineer
GenAI Engineer
Data Scientist
Backend Developer
Full-Stack Developer
```

### Project

Represents a portfolio project that uses a set of technical skills.

### CareerDomain

Represents a broader career category associated with job roles.

---

## Relationships

```text
(JobRole)-[:REQUIRES]->(Skill)

(Project)-[:USES]->(Skill)

(Skill)-[:PREREQUISITE_OF]->(Skill)

(JobRole)-[:BELONGS_TO]->(CareerDomain)
```

These relationships allow PathGraph AI to perform direct and multi-hop graph traversal.

---

## 📊 Data Model Diagram

![PathGraph AI Data Model](assets/pathgraph_data_model.png)

---

# 🔍 Example Cypher Queries

## Career Requirements

```cypher
MATCH (role:JobRole)-[:REQUIRES]->(skill:Skill)
RETURN role.name, collect(skill.name);
```

---

## Skill Gap Analysis

```cypher
MATCH (role:JobRole {name: $role_name})-[:REQUIRES]->(skill:Skill)

WITH collect(skill.name) AS required_skills

RETURN
    required_skills,
    [
        skill IN required_skills
        WHERE skill IN $user_skills
    ] AS matched_skills,
    [
        skill IN required_skills
        WHERE NOT skill IN $user_skills
    ] AS missing_skills;
```

User-provided values are passed as query parameters rather than concatenated into Cypher strings.

---

## Multi-Hop Learning Path

```cypher
MATCH path =
    (start:Skill {name: $start_skill})
    -[:PREREQUISITE_OF*1..4]->
    (target:Skill)

RETURN
    [node IN nodes(path) | node.name] AS route,
    target.name,
    length(path);
```

Example traversal:

```text
Python
→ Machine Learning
→ Deep Learning
→ Computer Vision
```

---

## Project Discovery

```cypher
MATCH (project:Project)-[:USES]->(skill:Skill)

WITH
    project,
    collect(skill.name) AS project_skills

RETURN
    project.name,
    project_skills;
```

---

# 🏗️ Architecture

```text
┌─────────────────────────────┐
│       Streamlit UI          │
│          app.py             │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       Service Layer         │
│                             │
│ career_service.py           │
│ graph_service.py            │
│ skill_service.py            │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│      Cypher Query Layer     │
│     queries/queries.py      │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│          CognoDB            │
│      Knowledge Graph        │
└─────────────────────────────┘
```

This separation keeps UI logic, business logic, graph queries, and database configuration modular and maintainable.

---

# 📁 Project Structure

```text
pathgraph-ai/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
│
├── assets/
│   └── pathgraph_data_model.png
│
├── config/
│   ├── __init__.py
│   └── database.py
│
├── data/
│   └── seed_data.json
│
├── queries/
│   ├── __init__.py
│   └── queries.py
│
├── scripts/
│   └── seed_database.py
│
└── services/
    ├── __init__.py
    ├── career_service.py
    ├── graph_service.py
    └── skill_service.py
```

---

# 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Interactive web interface |
| CognoDB | Managed graph database |
| Cypher | Graph querying and traversal |
| Neo4j Python Driver | Bolt database connectivity |
| PyVis | Interactive graph visualization |
| python-dotenv | Environment configuration |

---

# ⚙️ Local Setup

## 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd pathgraph-ai
```

---

## 2. Create a virtual environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure environment variables

Create a `.env` file based on `.env.example`.

Example:

```env
COGNODB_URI=your_cognodb_connection_uri
COGNODB_USERNAME=your_username
COGNODB_PASSWORD=your_password
```

> Never commit your real `.env` file or database password to GitHub.

---

## 5. Seed the graph

```bash
python -m scripts.seed_database
```

Expected output:

```text
PathGraph AI seed data loaded successfully!
```

---

## 6. Run the application

```bash
streamlit run app.py
```

Then open the local Streamlit URL displayed in the terminal.

---

# 🔐 Security

Database credentials are loaded from environment variables rather than being hard-coded into the source code.

User-provided values are supplied to Cypher queries through parameters such as:

```python
session.run(
    query,
    role_name=role_name,
    user_skills=user_skills
)
```

This avoids directly constructing Cypher queries from user input.

The `.env` file is excluded from version control through `.gitignore`.

---

# 🌱 Seed Data

The repository includes deterministic seed data and a seeding script so the graph can be recreated consistently.

Run:

```bash
python -m scripts.seed_database
```

The seeded knowledge graph contains skills, career roles, projects, career domains, and the relationships between them.

---

# 📸 Application Screenshots

Screenshots will be added before final submission.

Recommended screenshots:

1. PathGraph AI dashboard
2. Career Match results
3. Skill Gap analysis
4. Multi-hop Career Route Explorer
5. Interactive Graph Explorer
6. Project Finder results

---

# 🎯 Example User Journey

A user may enter:

```text
Python
Machine Learning
Deep Learning
OpenCV
TensorFlow
```

PathGraph AI can then:

1. Rank suitable career roles.
2. Calculate career match percentages.
3. Identify missing skills.
4. Analyze readiness for a selected career.
5. Traverse multi-hop learning routes.
6. Recommend relevant portfolio projects.
7. Visualize the connected career knowledge graph.

---

# 🚧 Current Scope

PathGraph AI currently uses a curated career knowledge graph intended to demonstrate graph modeling, traversal, parameterized Cypher queries, career reasoning, and interactive visualization.

The recommendation percentages represent **skill-overlap scores within the seeded graph**, not employment probabilities or predictions of hiring outcomes.

---

# 🔮 Future Improvements

Potential extensions include:

- Resume-based automatic skill extraction
- LLM-assisted career explanations
- Personalized learning roadmaps
- Larger career and skill knowledge graphs
- Job-market data integration
- Course recommendations
- Graph embeddings
- Semantic skill matching
- User profiles and saved career paths

---

# 👨‍💻 Author

**Govind Sannith Reddy**

Software Engineering / AI-ML Candidate

---

# 📄 License

This project was developed as part of a technical assessment.