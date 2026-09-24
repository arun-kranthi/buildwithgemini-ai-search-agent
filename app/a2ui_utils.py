import json
from google.genai import types
from a2ui.schema.manager import A2uiSchemaManager

a2ui_manager = A2uiSchemaManager(version="0.8")

def a2ui_search_callback(callback_context, model_response):
    """ADK callback to transform tool responses into native A2UI 0.8 cards."""
    if not hasattr(model_response, "candidates") or not model_response.candidates:
        return
        
    for candidate in model_response.candidates:
        if not hasattr(candidate, "content") or not candidate.content or not candidate.content.parts:
            continue
            
        for part in candidate.content.parts:
            if hasattr(part, "function_response") and part.function_response:
                fn_name = part.function_response.name
                fn_resp = part.function_response.response
                
                if fn_name == "search_enterprise_documents":
                    docs = fn_resp.get("documents", [])
                    if docs:
                        card_parts = [
                            {"id": "card_root", "component": {"Card": {"child": "column_main"}}},
                            {"id": "column_main", "component": {"Column": {"children": {"explicitList": ["text_title", "divider_1"] + [f"text_doc_{i}" for i in range(len(docs))]}}}},
                            {"id": "text_title", "component": {"Text": {"text": {"literalString": f"🔍 Search Results for: {fn_resp.get('query', '')}"}, "usageHint": "h3"}}},
                            {"id": "divider_1", "component": {"Divider": {}}}
                        ]
                        
                        for idx, doc in enumerate(docs):
                            doc_id = f"text_doc_{idx}"
                            card_parts.append({
                                "id": doc_id,
                                "component": {
                                    "Text": {
                                        "text": {"literalString": f"📄 [{doc.get('doc_id')}] {doc.get('title')}\nCategory: {doc.get('category')} | Author: {doc.get('author')}\nSummary: {doc.get('summary')}"},
                                        "usageHint": "body"
                                    }
                                }
                            })
                            
                        surface_update = a2ui_manager.create_surface_update(
                            surface_id="search_results",
                            components=card_parts
                        )
                        
                        candidate.content.parts.append(
                            types.Part.from_bytes(
                                data=json.dumps(surface_update).encode("utf-8"),
                                mime_type="application/json+a2ui"
                            )
                        )
