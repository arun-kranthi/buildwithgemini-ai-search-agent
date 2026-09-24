# NexusSearch Master Enterprise AI — Autonomous Intelligence & MCP Hub

[![Gemini 2.5 Flash](https://img.shields.io/badge/Model-Gemini%202.5%20Flash-06b6d4?style=for-the-badge&logo=google)](https://ai.google.dev/)
[![Google ADK](https://img.shields.io/badge/Framework-Google%20ADK-3b82f6?style=for-the-badge)](https://github.com/google/adk)
[![MCP Enabled](https://img.shields.io/badge/Protocol-Model%20Context%20Protocol%20(MCP)-10b981?style=for-the-badge)](https://modelcontextprotocol.io)
[![Public REST APIs](https://img.shields.io/badge/Integrations-5%20Public%20REST%20APIs-f43f5e?style=for-the-badge)](https://github.com/google/adk)
[![A2UI Enabled](https://img.shields.io/badge/UI-A2UI%20Rich%20Cards-8b5cf6?style=for-the-badge)](https://github.com/google/a2ui)

**NexusSearch Master Enterprise AI** is an enterprise-grade autonomous intelligence platform powered by **Google ADK (Agent Development Kit)**, **Gemini 2.5 Flash**, **Model Context Protocol (MCP v1.0)**, and **FastAPI**.

It seamlessly connects enterprise ERP databases with live public web APIs and external MCP server microservices, executing real-time cross-system searches across:
1. **5 Enterprise Microservices**: E-Commerce Orders, Supply Chain Logistics, Salesforce CRM 360, SAP ERP Finance, and Workday HR & ServiceNow IT Directory.
2. **5 Public REST APIs**: CoinGecko Crypto Prices, Open-Meteo Weather Forecast, REST Countries Global Trade, HackerNews Algolia Search, and JSONPlaceholder Mock Payload.
3. **Model Context Protocol (MCP) Microservices**: Auto-registers external MCP servers (`firebase_mcp`, `google_developer_knowledge_mcp`) into the agent's runtime context.

![NexusSearch Master Enterprise AI Demo](demo.gif)

---

## 🌐 Integrated Public REST APIs & MCP Services

| Category | Provider / Standard | Function / Capabilities |
| :--- | :--- | :--- |
| 🪙 **Crypto Market Data** | **CoinGecko REST API** | Live prices for Bitcoin, Ethereum, Solana, and 24h market trends |
| 🌤 **Logistics Weather** | **Open-Meteo REST API** | Real-time weather, wind speeds, and climate conditions for transit hubs |
| 🌐 **Global Trade** | **REST Countries API** | Official country names, capitals, currency codes, and subregion stats |
| 📰 **Tech News & Trends** | **HackerNews Algolia API** | Live search across developer trends, AI news, and community scores |
| 🔌 **MCP Microservices** | **Model Context Protocol (MCP)** | Dynamic discovery and execution of external MCP server tools |

---

## 🏗 Master System Architecture

```
                                  +-------------------------------------------------+
                                  |  NexusSearch Master Glassmorphic Dashboard UI   |
                                  +-----------------------+-------------------------+
                                                          |
                                                 (FastAPI A2A Proxy)
                                                          v
                                  +-------------------------------------------------+
                                  |   Google ADK LlmAgent (Gemini 2.5 Flash Engine) |
                                  +----+---------------+---------------+-------+----+
                                       |               |               |
             +-------------------------+               |               +-------------------------+
             |                                         v                                         |
             v                         +-------------------------------+                         v
+--------------------------+           | 🔌 Connected MCP Servers      |           +--------------------------+
| 📦 Enterprise Microservices|           |  - Firebase MCP               |           | 🌐 Public REST Web APIs  |
|  - E-Commerce & Logistics|           |  - Google Dev Knowledge MCP   |           |  - CoinGecko Crypto API  |
|  - Salesforce CRM 360    |           |  - Custom Microservice MCP    |           |  - Open-Meteo Weather API |
|  - SAP ERP Finance       |           +-------------------------------+           |  - REST Countries API    |
|  - Workday HR & IT       |                                                       |  - HackerNews Algolia    |
+--------------------------+                                                       +--------------------------+
```

---

## 🚀 Quickstart & Setup Guide

### 1. Installation
```bash
git clone https://github.com/arun-kranthi/buildwithgemini-ai-search-agent.git
cd buildwithgemini-ai-search-agent
uv sync
```

### 2. Launching Master Application
```bash
cd frontend
PORT=8081 uv run python main.py
```

Open `http://localhost:8081` in your browser to try out live REST API queries, MCP tool execution, and enterprise cross-system searches!
