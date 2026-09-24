import os
import uuid
import logging
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from a2ui.schema.manager import A2uiSchemaManager

from app.search_tools import search_enterprise_documents, get_document_details
from app.image_gen_tools import generate_search_diagram

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai_search_frontend")

app = FastAPI(title="Enterprise AI Search Frontend Proxy")
a2ui_manager = A2uiSchemaManager(version="0.8")

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

@app.post("/chat")
async def chat(req: ChatRequest):
    session_id = req.session_id or str(uuid.uuid4())
    logger.info(f"Processing query: {req.message}")
    
    parts_list = []
    query_lower = req.message.lower()
    
    if "diagram" in query_lower or "flowchart" in query_lower:
        diag_res = generate_search_diagram(req.message)
        parts_list.append({
            "kind": "text", 
            "text": f"Generated Architecture & Data Flow Diagram for: '{req.message}'\n{diag_res}"
        })
    else:
        res = search_enterprise_documents(req.message)
        docs = res.get("documents", [])
        
        parts_list.append({
            "kind": "text", 
            "text": f"Found {len(docs)} verified internal enterprise documentation guides matching '{req.message}':"
        })
        
        card_parts = [
            {"id": "card_root", "component": {"Card": {"child": "column_main"}}},
            {"id": "column_main", "component": {"Column": {"children": {"explicitList": ["text_title", "divider_1"] + [f"text_doc_{i}" for i in range(len(docs))]}}}},
            {"id": "text_title", "component": {"Text": {"text": {"literalString": f"🔍 Enterprise Search: {req.message}"}, "usageHint": "h3"}}},
            {"id": "divider_1", "component": {"Divider": {}}}
        ]
        
        for idx, doc in enumerate(docs):
            card_parts.append({
                "id": f"text_doc_{idx}",
                "component": {
                    "Text": {
                        "text": {"literalString": f"📄 [{doc.get('doc_id')}] {doc.get('title')}\nCategory: {doc.get('category')} | Author: {doc.get('author')}\nSummary: {doc.get('summary')}"},
                        "usageHint": "body"
                    }
                }
            })
            
        surface_update = {
            "surfaceUpdate": {
                "surfaceId": "search_results",
                "components": card_parts
            }
        }
        parts_list.append({"kind": "a2ui", "data": surface_update})
        
    return {"session_id": session_id, "parts": parts_list}

static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8081))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
