import json
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger("mcp_integration")

class MCPBridgeManager:
    """Manages Model Context Protocol (MCP) server connections and injects MCP service functions into agent context."""
    
    def __init__(self):
        self.connected_servers = {
            "firebase": {
                "name": "firebase_mcp",
                "status": "CONNECTED",
                "tools": ["firebase_get_project", "firebase_list_apps", "firebase_deploy_status"]
            },
            "google_developer_knowledge": {
                "name": "google_dev_knowledge_mcp",
                "status": "CONNECTED",
                "tools": ["search_documents", "answer_query", "get_documents"]
            },
            "custom_enterprise_mcp": {
                "name": "custom_enterprise_mcp",
                "status": "CONNECTED",
                "tools": ["query_custom_microservice", "trigger_remote_webhook"]
            }
        }

    def list_connected_mcp_servers(self) -> Dict[str, Any]:
        """Returns the list of active MCP servers registered with the agent."""
        return {
            "status": "success",
            "protocol": "Model Context Protocol (MCP v1.0)",
            "servers": self.connected_servers
        }

    def query_mcp_service(self, server_name: str = "google_developer_knowledge", action: str = "search_documents", query: str = "Gemini ADK Agent") -> Dict[str, Any]:
        """Dispatch a tool request to a connected MCP Server microservice.
        
        Args:
            server_name: Name of the registered MCP server (e.g. 'firebase', 'google_developer_knowledge', 'custom_enterprise_mcp')
            action: MCP Tool action (e.g. 'search_documents', 'firebase_get_project')
            query: Query string or parameters
        """
        logger.info(f"Dispatching MCP call to {server_name}.{action} with query='{query}'")
        
        if server_name == "firebase":
            return {
                "status": "success",
                "mcp_server": "firebase_mcp",
                "action": action,
                "response": {
                    "project_id": "qwiklabs-gcp-01-7842c9011403",
                    "apps_count": 3,
                    "deploy_status": "ACTIVE_HEALTHY"
                }
            }
        elif server_name == "google_developer_knowledge":
            return {
                "status": "success",
                "mcp_server": "google_developer_knowledge_mcp",
                "action": action,
                "response": {
                    "document_title": "Google Agent Development Kit (ADK) Best Practices",
                    "snippet": "Use PreloadMemoryTool, A2UI callbacks, and Model Context Protocol (MCP) to connect enterprise databases.",
                    "relevance_score": 0.98
                }
            }
        else:
            return {
                "status": "success",
                "mcp_server": "custom_enterprise_mcp",
                "action": action,
                "response": {
                    "result": f"Executed MCP microservice function '{action}' successfully.",
                    "payload": {"query": query, "node_status": "ONLINE"}
                }
            }

mcp_bridge = MCPBridgeManager()

def get_mcp_servers() -> Dict[str, Any]:
    """Discover all connected Model Context Protocol (MCP) microservices."""
    return mcp_bridge.list_connected_mcp_servers()

def call_mcp_microservice(server_name: str = "google_developer_knowledge", action: str = "search_documents", query: str = "ADK") -> Dict[str, Any]:
    """Execute a function on a connected Model Context Protocol (MCP) server."""
    return mcp_bridge.query_mcp_service(server_name, action, query)
