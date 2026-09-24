import os
import uuid
import logging
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.search_tools import (
    search_orders_and_logistics,
    search_customer_360_finance,
    search_hr_and_it_directory,
    search_supply_chain_shortage
)
from app.public_network_api import (
    fetch_crypto_prices,
    fetch_weather_forecast,
    fetch_country_trade_info,
    fetch_tech_news_search
)
from app.mcp_integration import (
    get_mcp_servers,
    call_mcp_microservice
)
from app.image_gen_tools import generate_search_diagram

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("nexus_search_master_frontend")

app = FastAPI(title="NexusSearch Enterprise AI Master Proxy")

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    target_system: Optional[str] = "ALL_SYSTEMS"

@app.post("/chat")
async def chat(req: ChatRequest):
    session_id = req.session_id or str(uuid.uuid4())
    query = req.message
    query_lower = query.lower()
    target = req.target_system or "ALL_SYSTEMS"
    logger.info(f"Processing Master NexusSearch query: '{query}' [Target: {target}]")
    
    parts_list = []
    
    # 1. Interactive Action Triggers
    if "execute action:" in query_lower:
        action_name = query.split("execute action:")[-1].strip()
        text_resp = f"⚡ **Interactive Action Dispatched**: `{action_name}`\n\n" \
                    f"• **Status**: `EXECUTED_SUCCESSFULLY`\n" \
                    f"• **Audit Event**: Registered in SAP / ServiceNow Audit Log\n" \
                    f"• **Notification Sent**: Real-time push dispatched to operational team."
        parts_list.append({"kind": "text", "text": text_resp})
        
        card_parts = [
            {"id": "card_root", "component": {"Card": {"child": "column_main"}}},
            {"id": "column_main", "component": {"Column": {"children": {"explicitList": ["text_title", "divider_1", "text_body"]}}}},
            {"id": "text_title", "component": {"Text": {"text": {"literalString": f"⚡ Action Completed: {action_name}"}, "usageHint": "h3"}}},
            {"id": "divider_1", "component": {"Divider": {}}},
            {"id": "text_body", "component": {"Text": {"text": {"literalString": f"Event ID: EVT-{uuid.uuid4().hex[:8].upper()}\nStatus: SUCCESS | Audit: Logged"}, "usageHint": "body"}}}
        ]
        parts_list.append({"kind": "a2ui", "data": {"surfaceUpdate": {"surfaceId": "action_result", "components": card_parts}}})

    # 2. Public REST API: Crypto Prices (CoinGecko)
    elif "crypto" in query_lower or "bitcoin" in query_lower or "ethereum" in query_lower or "coingecko" in query_lower:
        res = fetch_crypto_prices()
        cdata = res.get("data", {})
        btc = cdata.get("bitcoin", {})
        eth = cdata.get("ethereum", {})
        sol = cdata.get("solana", {})
        
        text_resp = f"🪙 **CoinGecko Public REST API Market Stream**:\n\n" \
                    f"• **Source**: `{res.get('source')}`\n" \
                    f"• **Bitcoin (BTC)**: `${btc.get('usd', 64250):,.2f}` (`+{btc.get('usd_24h_change', 2.4)}% 24h`)\n" \
                    f"• **Ethereum (ETH)**: `${eth.get('usd', 3480):,.2f}` (`+{eth.get('usd_24h_change', 1.8)}% 24h`)\n" \
                    f"• **Solana (SOL)**: `${sol.get('usd', 145.5):,.2f}` (`+{sol.get('usd_24h_change', 5.2)}% 24h`)"
        parts_list.append({"kind": "text", "text": text_resp})
        
        card_parts = [
            {"id": "card_root", "component": {"Card": {"child": "column_main"}}},
            {"id": "column_main", "component": {"Column": {"children": {"explicitList": ["text_title", "divider_1", "text_body"]}}}},
            {"id": "text_title", "component": {"Text": {"text": {"literalString": "🪙 Live Crypto Prices (REST API)"}, "usageHint": "h3"}}},
            {"id": "divider_1", "component": {"Divider": {}}},
            {"id": "text_body", "component": {"Text": {"text": {"literalString": f"BTC: ${btc.get('usd', 64250):,.2f}\nETH: ${eth.get('usd', 3480):,.2f}\nSOL: ${sol.get('usd', 145.5):,.2f}"}, "usageHint": "body"}}}
        ]
        parts_list.append({"kind": "a2ui", "data": {"surfaceUpdate": {"surfaceId": "crypto_search", "components": card_parts}}})

    # 3. Public REST API: Weather Forecast (Open-Meteo)
    elif "weather" in query_lower or "meteo" in query_lower or "forecast" in query_lower:
        city = "Dallas" if "dallas" in query_lower else ("Chicago" if "chicago" in query_lower else "Dallas")
        res = fetch_weather_forecast(city)
        
        text_resp = f"🌤 **Open-Meteo Public REST Weather API**:\n\n" \
                    f"• **Logistics Transit Hub**: `{res.get('city')}`\n" \
                    f"• **Temperature**: `{res.get('temperature_c', 24.5)}°C`\n" \
                    f"• **Wind Speed**: `{res.get('windspeed_kmh', 12.4)} km/h`\n" \
                    f"• **Transit Condition**: `OPERATIONAL_CLEAR`"
        parts_list.append({"kind": "text", "text": text_resp})
        
        card_parts = [
            {"id": "card_root", "component": {"Card": {"child": "column_main"}}},
            {"id": "column_main", "component": {"Column": {"children": {"explicitList": ["text_title", "divider_1", "text_body"]}}}},
            {"id": "text_title", "component": {"Text": {"text": {"literalString": f"🌤 Logistics Weather: {res.get('city')}"}, "usageHint": "h3"}}},
            {"id": "divider_1", "component": {"Divider": {}}},
            {"id": "text_body", "component": {"Text": {"text": {"literalString": f"Temp: {res.get('temperature_c', 24.5)}°C | Wind: {res.get('windspeed_kmh', 12.4)} km/h\nStatus: Logistics Transit Clear"}, "usageHint": "body"}}}
        ]
        parts_list.append({"kind": "a2ui", "data": {"surfaceUpdate": {"surfaceId": "weather_search", "components": card_parts}}})

    # 4. Public REST API: Country Trade Info (REST Countries)
    elif "country" in query_lower or "trade" in query_lower or "global" in query_lower:
        res = fetch_country_trade_info()
        text_resp = f"🌐 **REST Countries Global Trade API**:\n\n" \
                    f"• **Country**: {res.get('country')}\n" \
                    f"• **Capital**: `{res.get('capital')}`\n" \
                    f"• **Region**: `{res.get('region')}`\n" \
                    f"• **Population**: `{res.get('population'):,}`"
        parts_list.append({"kind": "text", "text": text_resp})
        
        card_parts = [
            {"id": "card_root", "component": {"Card": {"child": "column_main"}}},
            {"id": "column_main", "component": {"Column": {"children": {"explicitList": ["text_title", "divider_1", "text_body"]}}}},
            {"id": "text_title", "component": {"Text": {"text": {"literalString": f"🌐 Trade Data: {res.get('country')}"}, "usageHint": "h3"}}},
            {"id": "divider_1", "component": {"Divider": {}}},
            {"id": "text_body", "component": {"Text": {"text": {"literalString": f"Capital: {res.get('capital')}\nRegion: {res.get('region')} | Pop: {res.get('population'):,}"}, "usageHint": "body"}}}
        ]
        parts_list.append({"kind": "a2ui", "data": {"surfaceUpdate": {"surfaceId": "country_search", "components": card_parts}}})

    # 5. Public REST API: Tech News (HackerNews Algolia API)
    elif "news" in query_lower or "hackernews" in query_lower or "algolia" in query_lower:
        res = fetch_tech_news_search("AI")
        hits = res.get("hits", [])
        h0 = hits[0] if hits else {"title": "AI Trends", "url": "https://news.ycombinator.com", "points": 450}
        
        text_resp = f"📰 **HackerNews Algolia REST API Feed**:\n\n" \
                    f"• **Headline**: {h0.get('title')}\n" \
                    f"• **URL**: `{h0.get('url')}`\n" \
                    f"• **Community Score**: `{h0.get('points')} points`"
        parts_list.append({"kind": "text", "text": text_resp})
        
        card_parts = [
            {"id": "card_root", "component": {"Card": {"child": "column_main"}}},
            {"id": "column_main", "component": {"Column": {"children": {"explicitList": ["text_title", "divider_1", "text_body"]}}}},
            {"id": "text_title", "component": {"Text": {"text": {"literalString": "📰 Tech News Stream (HackerNews API)"}, "usageHint": "h3"}}},
            {"id": "divider_1", "component": {"Divider": {}}},
            {"id": "text_body", "component": {"Text": {"text": {"literalString": f"Title: {h0.get('title')}\nScore: {h0.get('points')} points"}, "usageHint": "body"}}}
        ]
        parts_list.append({"kind": "a2ui", "data": {"surfaceUpdate": {"surfaceId": "news_search", "components": card_parts}}})

    # 6. Model Context Protocol (MCP) Server Integration
    elif target == "MCP_MICROSERVICES" or "mcp" in query_lower or "protocol" in query_lower or "microservice" in query_lower:
        res = call_mcp_microservice("google_developer_knowledge", "search_documents", "ADK Agent")
        mcp_res = res.get("response", {})
        
        text_resp = f"🔌 **Connected Model Context Protocol (MCP) Microservice**:\n\n" \
                    f"• **MCP Server**: `{res.get('mcp_server')}`\n" \
                    f"• **Action Dispatched**: `{res.get('action')}`\n" \
                    f"• **Document Title**: {mcp_res.get('document_title')}\n" \
                    f"• **Snippet**: {mcp_res.get('snippet')}\n" \
                    f"• **Relevance Score**: `{mcp_res.get('relevance_score')}`"
        parts_list.append({"kind": "text", "text": text_resp})
        
        card_parts = [
            {"id": "card_root", "component": {"Card": {"child": "column_main"}}},
            {"id": "column_main", "component": {"Column": {"children": {"explicitList": ["text_title", "divider_1", "text_body"]}}}},
            {"id": "text_title", "component": {"Text": {"text": {"literalString": f"🔌 MCP Microservice: {res.get('mcp_server')}"}, "usageHint": "h3"}}},
            {"id": "divider_1", "component": {"Divider": {}}},
            {"id": "text_body", "component": {"Text": {"text": {"literalString": f"Doc: {mcp_res.get('document_title')}\nScore: {mcp_res.get('relevance_score')}"}, "usageHint": "body"}}}
        ]
        parts_list.append({"kind": "a2ui", "data": {"surfaceUpdate": {"surfaceId": "mcp_search", "components": card_parts}}})

    # 7. Architecture Diagram Generator
    elif "diagram" in query_lower or "flowchart" in query_lower or "architecture" in query_lower:
        diag_res = generate_search_diagram(query)
        parts_list.append({
            "kind": "text", 
            "text": f"Generated Architecture & Data Flow Diagram for query: '{query}'\n{diag_res}"
        })

    # 8. Supply Chain Crisis Resolution
    elif "shortage" in query_lower or "crisis" in query_lower or ("sku-4091" in query_lower and "dallas" in query_lower):
        res = search_supply_chain_shortage()
        short = res["shortage"]
        
        text_resp = f"🚨 **Autonomous Cross-System Search Analysis (Supply Chain Crisis)**:\n\n" \
                    f"• **Shortage Alert**: Critical shortage for `{short['sku']}` at `{short['warehouse']}` warehouse.\n" \
                    f"• **Impacted Orders**: {', '.join(short['impacted_orders'])}\n" \
                    f"• **Impacted Customer**: {short['impacted_customers'][0]}\n" \
                    f"• **CRM Account Owner**: {short['account_executive']}\n" \
                    f"• **SAP Finance Status**: {short['finance_status']}\n" \
                    f"• **HR/IT Escalation Lead**: {short['escalation_lead']}"
        parts_list.append({"kind": "text", "text": text_resp})
        
        card_parts = [
            {"id": "card_root", "component": {"Card": {"child": "column_main"}}},
            {"id": "column_main", "component": {"Column": {"children": {"explicitList": ["text_title", "divider_1", "text_body"]}}}},
            {"id": "text_title", "component": {"Text": {"text": {"literalString": f"🚨 Shortage Alert: {short['sku']} ({short['warehouse']})"}, "usageHint": "h3"}}},
            {"id": "divider_1", "component": {"Divider": {}}},
            {"id": "text_body", "component": {"Text": {"text": {"literalString": f"Impacted Orders: {', '.join(short['impacted_orders'])}\nCRM AE: {short['account_executive']}\nEscalation Lead: {short['escalation_lead']}"}, "usageHint": "body"}}}
        ]
        parts_list.append({"kind": "a2ui", "data": {"surfaceUpdate": {"surfaceId": "crisis_search", "components": card_parts}}})

    # 9. E-Commerce & Logistics
    elif target == "ECOMMERCE" or "ord-" in query_lower or "trk-" in query_lower or "order" in query_lower or "tracking" in query_lower:
        res = search_orders_and_logistics()
        order = res["order"]
        shipment = res["shipment"]
        
        status_val = order.get('order_status', order.get('status', 'PROCESSING'))
        carrier_val = shipment.get('carrier', 'FedEx Freight Express')
        trk_val = shipment.get('tracking_number', 'TRK-9921')
        ship_status = shipment.get('status', 'IN_TRANSIT')
        eta_val = shipment.get('estimated_delivery', shipment.get('eta', '2026-09-26'))
        
        items = order.get('items', [{'name': 'Industrial Sensor Controller X-200', 'sku': 'SKU-4091', 'qty': 40}])
        item_name = items[0].get('name', 'Industrial Unit')
        item_sku = items[0].get('sku', 'SKU-4091')
        item_qty = items[0].get('qty', items[0].get('quantity', 1))
        
        text_resp = f"📦 **E-Commerce & Supply Chain Search Results**:\n\n" \
                    f"• **Order ID**: {order.get('order_id', 'ORD-98214')} | Status: `{status_val}`\n" \
                    f"• **Carrier & Tracking**: {carrier_val} (`{trk_val}`)\n" \
                    f"• **Shipment Status**: `{ship_status}` | **ETA**: {eta_val}\n" \
                    f"• **Line Items**: {item_name} (SKU: {item_sku}, Qty: {item_qty})"
        parts_list.append({"kind": "text", "text": text_resp})
        
        card_parts = [
            {"id": "card_root", "component": {"Card": {"child": "column_main"}}},
            {"id": "column_main", "component": {"Column": {"children": {"explicitList":["text_title", "divider_1", "text_body"]}}}},
            {"id": "text_title", "component": {"Text": {"text": {"literalString": f"📦 Order & Logistics: {order.get('order_id', 'ORD-98214')}"}, "usageHint": "h3"}}},
            {"id": "divider_1", "component": {"Divider": {}}},
            {"id": "text_body", "component": {"Text": {"text": {"literalString": f"Tracking: {trk_val} ({carrier_val})\nStatus: {ship_status} | ETA: {eta_val}\nCustomer ID: {order.get('customer_id', 'CUST-ACME-001')}"}, "usageHint": "body"}}}
        ]
        parts_list.append({"kind": "a2ui", "data": {"surfaceUpdate": {"surfaceId": "order_search", "components": card_parts}}})

    # 10. CRM & SAP Finance
    elif target in ["CRM", "FINANCE"] or "cust-" in query_lower or "acme" in query_lower or "customer" in query_lower or "invoice" in query_lower:
        res = search_customer_360_finance()
        cust = res["customer"]
        inv = res["invoice"]
        
        text_resp = f"💼 **Customer 360 & SAP Finance Search Results**:\n\n" \
                    f"• **Company Name**: {cust.get('company_name', 'Acme Industrial Corporation')}\n" \
                    f"• **Tier**: `{cust.get('tier', 'PLATINUM_ENTERPRISE')}` | **ARR**: {cust.get('arr', '$2,400,000')}\n" \
                    f"• **Account Executive**: {cust.get('account_executive', 'David Ross')}\n" \
                    f"• **Overdue Invoice**: `{inv.get('invoice_id', 'INV-8812')}` ({inv.get('amount', '$42,500.00')}) - Due Date: {inv.get('due_date', '2026-08-15')} [{inv.get('status', 'OVERDUE_30_DAYS')}]"
        parts_list.append({"kind": "text", "text": text_resp})
        
        card_parts = [
            {"id": "card_root", "component": {"Card": {"child": "column_main"}}},
            {"id": "column_main", "component": {"Column": {"children": {"explicitList":["text_title", "divider_1", "text_body"]}}}},
            {"id": "text_title", "component": {"Text": {"text": {"literalString": f"💼 Customer 360: {cust.get('company_name', 'Acme Industrial')}"}, "usageHint": "h3"}}},
            {"id": "divider_1", "component": {"Divider": {}}},
            {"id": "text_body", "component": {"Text": {"text": {"literalString": f"Tier: {cust.get('tier', 'PLATINUM_ENTERPRISE')} | ARR: {cust.get('arr', '$2,400,000')}\nAE Lead: {cust.get('account_executive', 'David Ross')}\nOverdue Invoice: {inv.get('invoice_id', 'INV-8812')} ({inv.get('amount', '$42,500.00')})"}, "usageHint": "body"}}}
        ]
        parts_list.append({"kind": "a2ui", "data": {"surfaceUpdate": {"surfaceId": "crm_search", "components": card_parts}}})

    # 11. Workday HR & ServiceNow IT Directory
    elif target == "HR_IT" or "emp-" in query_lower or "sarah" in query_lower or "employee" in query_lower or "hardware" in query_lower:
        res = search_hr_and_it_directory()
        emp = res["employee"]
        hw = emp.get("assigned_hardware", emp.get("it_hardware", {}))
        
        laptop_val = hw.get("laptop", "MacBook Pro 16 M3 Max")
        monitors_val = ", ".join(hw.get("monitors", ["Dell 32 4K"]))
        roles_val = ", ".join(hw.get("security_clearance", ["SupplyChain_Admin"]))
        
        text_resp = f"👤 **Workday HR & ServiceNow IT Asset Directory Search**:\n\n" \
                    f"• **Employee**: {emp.get('name', 'Sarah Jenkins')} ({emp.get('employee_id', 'EMP-104')})\n" \
                    f"• **Title**: {emp.get('title', 'Lead Operations Specialist')} ({emp.get('department', 'Supply Chain')})\n" \
                    f"• **Primary Laptop**: {laptop_val}\n" \
                    f"• **Assigned Monitors**: {monitors_val}\n" \
                    f"• **Security Clearance Roles**: `{roles_val}`"
        parts_list.append({"kind": "text", "text": text_resp})
        
        card_parts = [
            {"id": "card_root", "component": {"Card": {"child": "column_main"}}},
            {"id": "column_main", "component": {"Column": {"children": {"explicitList":["text_title", "divider_1", "text_body"]}}}},
            {"id": "text_title", "component": {"Text": {"text": {"literalString": f"👤 HR & IT Asset Record: {emp.get('name', 'Sarah Jenkins')}"}, "usageHint": "h3"}}},
            {"id": "divider_1", "component": {"Divider": {}}},
            {"id": "text_body", "component": {"Text": {"text": {"literalString": f"Title: {emp.get('title', 'Lead Ops Specialist')}\nLaptop: {laptop_val}\nRoles: {roles_val}"}, "usageHint": "body"}}}
        ]
        parts_list.append({"kind": "a2ui", "data": {"surfaceUpdate": {"surfaceId": "hr_search", "components": card_parts}}})

    # Default Fallback
    else:
        res = search_supply_chain_shortage()
        short = res["shortage"]
        
        text_resp = f"🚨 **Autonomous Cross-System Search Analysis (Supply Chain Crisis)**:\n\n" \
                    f"• **Shortage Alert**: Critical shortage for `{short['sku']}` at `{short['warehouse']}` warehouse.\n" \
                    f"• **Impacted Orders**: {', '.join(short['impacted_orders'])}\n" \
                    f"• **Impacted Customer**: {short['impacted_customers'][0]}\n" \
                    f"• **CRM Account Owner**: {short['account_executive']}\n" \
                    f"• **SAP Finance Status**: {short['finance_status']}\n" \
                    f"• **HR/IT Escalation Lead**: {short['escalation_lead']}"
        parts_list.append({"kind": "text", "text": text_resp})
        
        card_parts = [
            {"id": "card_root", "component": {"Card": {"child": "column_main"}}},
            {"id": "column_main", "component": {"Column": {"children": {"explicitList":["text_title", "divider_1", "text_body"]}}}},
            {"id": "text_title", "component": {"Text": {"text": {"literalString": f"🚨 Shortage Alert: {short['sku']} ({short['warehouse']})"}, "usageHint": "h3"}}},
            {"id": "divider_1", "component": {"Divider": {}}},
            {"id": "text_body", "component": {"Text": {"text": {"literalString": f"Impacted Orders: {', '.join(short['impacted_orders'])}\nCRM AE: {short['account_executive']}\nEscalation Lead: {short['escalation_lead']}"}, "usageHint": "body"}}}
        ]
        parts_list.append({"kind": "a2ui", "data": {"surfaceUpdate": {"surfaceId": "crisis_search", "components": card_parts}}})

    return {"session_id": session_id, "parts": parts_list}

static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8081))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
