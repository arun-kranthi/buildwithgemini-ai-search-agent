# Enterprise AI Search Agent

An enterprise-grade autonomous AI search agent powered by Google ADK (Agent Development Kit), Gemini 2.5 Flash, and Vertex AI. It provides cross-system search across 5 key enterprise domains: Supply Chain & Logistics, E-Commerce Orders, Salesforce CRM 360, SAP ERP Finance, and Workday HR & ServiceNow IT Asset Directory.

![Enterprise AI Search Demo](demo.gif)

## Key Features & Capabilities

- **E-Commerce & Supply Chain Search**: Search orders (`ORD-98214`), line items, warehouse stock levels, carrier details (`TRK-9921`), and delivery ETAs.
- **Salesforce CRM 360 & SAP Finance**: Query customer profiles (`CUST-ACME-001`), ARR tier, assigned Account Executive, credit limits, and overdue invoices (`INV-8812`).
- **Workday HR & ServiceNow IT Directory**: Search employee profiles (`EMP-104` Sarah Jenkins), assigned laptops, dual-monitor setups, and system security clearance roles.
- **Autonomous Multi-System Crisis Resolution**: Performs multi-system cross-cutting analysis when a critical part shortage occurs (e.g. `SKU-4091` in Dallas), identifying impacted customer orders, CRM account owners, invoice hold statuses, and HR escalation leads.
- **A2UI Rich Display Cards**: Emits structured A2UI display cards rendered in the custom glassmorphic web UI.

## Project Structure

```
ai-search-agent/
├── app/
│   ├── agentic_explorer.py  # ADK LlmAgent definition
│   ├── intent.py            # Agent prompt instructions
│   ├── mock_systems.py      # Mock enterprise datasets across 5 domains
│   ├── search_tools.py      # Function tools for enterprise search
│   ├── image_gen_tools.py   # Architecture diagram generator tool
│   └── a2ui_utils.py        # A2UI callback handlers
├── frontend/
│   ├── main.py              # FastAPI A2A proxy server
│   └── static/
│       └── index.html       # Enterprise Dark UI with prompt chips & A2UI renderer
├── demo.gif                 # Animated demo walkthrough
├── pyproject.toml           # Hatchling package configuration
└── agents-cli-manifest.yaml # Agents-CLI manifest configuration
```

## Running Locally

1. **Install Dependencies**:
   ```bash
   uv sync
   ```

2. **Start the Frontend & Search Server**:
   ```bash
   cd frontend
   PORT=8081 uv run python main.py
   ```

3. **Open in Browser**:
   Navigate to `http://localhost:8081` to interact with the Enterprise AI Search Agent interface and try out the example prompt chips.
