# Epic Analysis with LangChain & PostgreSQL (pgvector)

This project is a **multi-agent system** built using **LangChain**, **PostgreSQL (pgvector)**, and **Ollama** to analyze epics, refine backlogs, and identify potential pitfalls. 

The system:
1. **Ingests an epic** (including Jira issues and Confluence docs).
2. **Finds similar historic epics** (from a specific Jira board).
3. **Compares the target epic to past data** to find missing requirements.
4. **Generates a refined backlog** with new user stories, dependencies, and risks.
5. **Stores epics as embeddings** and ensures idempotency to avoid duplicates.

---

## **🚀 Setup & Installation**

### **1️⃣ Clone the Repository**
```bash
git clone <your-repo-url>
cd epic-analysis
```

### **2️⃣ Install Dependencies**
```bash
pipenv install
```

### **3️⃣ Set Up `.env` File**
Create a `.env` file in the root directory:

```ini
# Jira API Configuration
JIRA_BASE_URL=https://your-jira-instance.atlassian.net
JIRA_EMAIL=your_email@example.com
JIRA_API_TOKEN=your_api_token
JIRA_BOARD_ID=your_board_id

# Confluence API Configuration
CONFLUENCE_BASE_URL=https://your-confluence-instance.atlassian.net
CONFLUENCE_API_TOKEN=your_api_token

# PostgreSQL Configuration (for pgvector storage)
DATABASE_URL=postgresql://your_username:your_password@127.0.0.1:5432/epic_db

# Ollama Model Configuration (for LLM analysis)
OLLAMA_MODEL=deepseek-r1:14b
```

---

## **📂 Project Structure**
```
/epic-analysis
│── .env                          # Environment variables (Jira, Confluence, DB)
│── Pipfile                       # Pipenv dependencies
│── orchestrator.py                # Main orchestrator to run agents
│── /agents
│   │── epic_ingestion_agent.py    # Collects epic issues & documentation
│   │── historic_analysis_agent.py # Retrieves & analyzes past epics
│   │── epic_comparison_agent.py   # Compares target epic vs past epics
│   │── refinement_agent.py        # Outputs new backlog items & risks
│   │── epic_storage_agent.py      # Fetches & stores historic epics
│── /tools
│   │── jira_tools.py              # Fetches Jira epics & issues
│   │── confluence_tools.py        # Fetches Confluence documentation
│   │── text_processing.py         # Text extraction & NLP utilities
│── /models
│   │── vector_store.py            # PostgreSQL pgvector-based vector database
```

---

## **🛠️ Agents Overview**

### **1️⃣ Epic Ingestion Agent (`epic_ingestion_agent.py`)**
- **Fetches target epic data** from Jira & Confluence.
- **Prepares input for analysis**.

### **2️⃣ Historic Analysis Agent (`historic_analysis_agent.py`)**
- **Finds similar past epics** using **pgvector embeddings** in PostgreSQL.

### **3️⃣ Epic Comparison Agent (`epic_comparison_agent.py`)**
- **Compares the target epic** with historic data.
- **Identifies missing requirements, dependencies, and risks**.

### **4️⃣ Refinement Agent (`refinement_agent.py`)**
- **Generates a refined backlog** with:
  - Missing user stories
  - Unmet requirements
  - Potential pitfalls

### **5️⃣ Epic Storage Agent (`epic_storage_agent.py`)**
- **Finds & stores historic epics** from a specific Jira board.
- **Ensures idempotency** (does not re-fetch stored epics).

---

## **🛠️ Tools Overview**

### **1️⃣ Jira Tools (`jira_tools.py`)**
- Fetches **epics, issues, and details** from Jira.

### **2️⃣ Confluence Tools (`confluence_tools.py`)**
- Fetches **related Confluence documentation**.

### **3️⃣ Vector Store (`vector_store.py`)**
- Uses **PostgreSQL (pgvector)** to store & retrieve epic embeddings.

---

## **🛠️ Running the System**

### **1️⃣ Run Database Migrations**
```bash
python -c "from models.vector_store import engine; with engine.connect() as conn: conn.execute(text('SELECT 1')); print('✅ Database connected')"
```

### **2️⃣ Store Historic Epics (One-Time Setup)**
```bash
python -m agents.epic_storage_agent
```

### **3️⃣ Run the Full Orchestrator**
```bash
python -m orchestrator
```

This will:
1. Fetch the target epic & Confluence docs.
2. Find similar past epics from the database.
3. Analyze missing stories, requirements, and risks.
4. Generate backlog refinements.

---

## **✅ Next Steps**
- **Add Slack/Email notifications** when refinements are generated.
- **Use OpenAI or Anthropic instead of Ollama** for remote LLM inference.
- **Enhance PostgreSQL indexing** for faster vector queries.

For questions, open an issue in the repository! 🚀
