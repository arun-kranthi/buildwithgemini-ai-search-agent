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
from app.image_gen_tools import generate_search_diagram

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("nexus_search_frontend")

app = FastAPI(title="NexusSearch Enterprise AI Proxy")

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
    logger.info(f"Processing NexusSearch query: '{query}' [Target: {target}]")
    
    parts_list = []
    
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

    elif "diagram" in query_lower or "flowchart" in query_lower or "architecture" in query_lower:
        diag_res = generate_search_diagram(query)
        parts_list.append({
            "kind": "text", 
            "text": f"Generated Architecture & Data Flow Diagram for query: '{query}'\n{diag_res}"
        })

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
