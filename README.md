# Enterprise AI Search & Knowledge Discovery Agent

![Enterprise AI Search Demo](./demo.gif)

An enterprise-grade semantic search and knowledge discovery agent built with **Google ADK (Agent Development Kit)** and **Vertex AI**. The agent indexes internal technical documentation, provides instant RAG search results with rich A2UI cards, and generates technical data flow architecture diagrams.

---

## 🌟 Key Features & Capabilities

- **🔍 Semantic Enterprise Search**: Search internal engineering guidelines, security policies, cloud architecture specs, and governance documents.
- **🎨 Native A2UI 0.8 Display Cards**: Renders structured document cards, category badges, author metadata, and search summaries natively in the UI.
- **🧠 PreloadMemoryTool**: Maintains cross-session awareness of role-based search preferences and user interest topics.
- **📊 Architecture Flowchart Generation**: Generates clean technical data flow diagrams for RAG vector search pipelines.
- **⚡ FastAPI A2A Frontend Proxy**: Secure backend proxy bridging browser interactions with the agent runtime.

---

## 🛠️ Implemented Tools & Architecture

| Component | Implementation | Description |
| :--- | :--- | :--- |
| **Agent Framework** | `google-adk` | Google ADK `LlmAgent` using Gemini models |
| **UI Rendering** | `a2ui-agent-sdk` | A2UI 0.8 schema cards for search results & citations |
| **Memory** | `PreloadMemoryTool` | Contextual session memory for recent search topics |
| **Diagram Generation**| `Vertex AI Imagen 3` | Technical architecture diagram generation |
| **Frontend Proxy** | `FastAPI + Uvicorn` | Modern dark-themed glassmorphic web interface |

---

## 🚀 Getting Started

### Prerequisites

- Python `>=3.11`
- `uv` package manager

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/arun-kranthi/buildwithgemini-ai-search-agent.git
   cd buildwithgemini-ai-search-agent
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Start the local server**:
   ```bash
   cd frontend
   PORT=8081 uv run python main.py
   ```

4. **Access the application**:
   Open your browser to port `8081` to start querying internal enterprise documentation.

---

## 🧪 Example Prompts

- `Search internal engineering docs for API authentication`
- `Summarize Q3 cloud architecture guidelines`
- `Generate RAG retrieval data flow diagram`

---

## 📄 License

Apache 2.0 License. Built for the Google Build with Gemini Track 2 Lab.
