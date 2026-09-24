from typing import List, Dict, Any

MOCK_DOCUMENTS = [
    {
        "doc_id": "DOC-101",
        "title": "API Authentication & OAuth 2.0 Security Guidelines",
        "category": "Engineering / Security",
        "author": "Security Architecture Team",
        "last_updated": "2026-08-20",
        "summary": "Standard OAuth 2.0, JWT token validation, and service account key rotation policies for all enterprise microservices.",
        "tags": ["OAuth2", "Security", "JWT", "Authentication", "API"]
    },
    {
        "doc_id": "DOC-102",
        "title": "Q3 Cloud Architecture & Multi-Region GKE Deployment",
        "category": "Infrastructure / Cloud",
        "author": "DevOps & Cloud Infra",
        "last_updated": "2026-09-01",
        "summary": "Deployment specifications for multi-region GKE clusters, Cloud Spanner database replication, and global load balancing.",
        "tags": ["GKE", "Kubernetes", "Multi-Region", "Spanner", "Architecture"]
    },
    {
        "doc_id": "DOC-103",
        "title": "Vector Database Indexing & RAG Retrieval Specs",
        "category": "AI / Data Engineering",
        "author": "AI Platform Team",
        "last_updated": "2026-09-15",
        "summary": "Vector embedding dimensions, HNSW index parameter tuning, and hybrid keyword-dense retrieval benchmarks for Vertex AI Search.",
        "tags": ["Vector DB", "RAG", "Embeddings", "Vertex AI", "Search"]
    },
    {
        "doc_id": "DOC-104",
        "title": "Enterprise Data Governance & Compliance Policy v4",
        "category": "Governance & Legal",
        "author": "Data Governance Board",
        "last_updated": "2026-07-10",
        "summary": "Data classification guidelines (Public, Internal, Confidential, Restricted), PII redaction rules, and retention schedules.",
        "tags": ["Governance", "Compliance", "PII", "GDPR", "Data Safety"]
    }
]

def search_enterprise_documents(query: str, category_filter: str = "") -> Dict[str, Any]:
    """Search internal enterprise documentation and knowledge base articles.
    
    Args:
        query: The search query string (e.g., 'API authentication', 'cloud architecture').
        category_filter: Optional filter by department or category.
    """
    query_lower = query.lower()
    results = []
    
    for doc in MOCK_DOCUMENTS:
        match_title = any(word in doc["title"].lower() for word in query_lower.split())
        match_summary = any(word in doc["summary"].lower() for word in query_lower.split())
        match_tags = any(word in [t.lower() for t in doc["tags"]] for word in query_lower.split())
        
        if match_title or match_summary or match_tags or not query:
            if not category_filter or category_filter.lower() in doc["category"].lower():
                results.append(doc)
                
    return {
        "query": query,
        "total_matches": len(results),
        "documents": results if results else MOCK_DOCUMENTS[:2]
    }

def get_document_details(doc_id: str) -> Dict[str, Any]:
    """Get full document metadata, author details, and text content by document ID.
    
    Args:
        doc_id: The document ID (e.g., 'DOC-101').
    """
    for doc in MOCK_DOCUMENTS:
        if doc["doc_id"].upper() == doc_id.upper():
            return doc
            
    return {
        "doc_id": doc_id,
        "title": f"Enterprise Specification Guide {doc_id}",
        "category": "Engineering",
        "author": "Tech Staff",
        "last_updated": "2026-09-01",
        "summary": "Verified internal reference documentation.",
        "tags": ["Enterprise", "Guide"]
    }
