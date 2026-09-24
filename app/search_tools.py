from typing import Dict, Any, List
from app.mock_systems import (
    MOCK_SUPPLY_CHAIN_DB,
    MOCK_ECOMMERCE_DB,
    MOCK_CRM_DB,
    MOCK_FINANCE_DB,
    MOCK_HR_IT_DB
)

def search_orders_and_logistics(order_id: str = "ORD-98214", tracking_number: str = "TRK-9921") -> Dict[str, Any]:
    """Query E-Commerce Order Management & Logistics tracking system."""
    order = MOCK_ECOMMERCE_DB["orders"].get(order_id, {
        "order_id": order_id,
        "customer_id": "CUST-ACME-001",
        "customer_name": "Acme Industrial Corporation",
        "order_status": "PARTIALLY_SHIPPED",
        "total_amount": 58900.00,
        "items": [{"sku": "SKU-4091", "name": "Industrial Sensor Controller X-200", "qty": 40}],
        "tracking_number": tracking_number
    })
    shipment = MOCK_SUPPLY_CHAIN_DB["shipments"].get(tracking_number, {
        "carrier": "FedEx Freight Express",
        "tracking_number": tracking_number,
        "status": "IN_TRANSIT_DELAYED",
        "estimated_delivery": "2026-09-26 14:00 EST"
    })
    return {"domain": "ECOMMERCE_LOGISTICS", "order": order, "shipment": shipment}

def search_customer_360_finance(customer_id: str = "CUST-ACME-001") -> Dict[str, Any]:
    """Query Salesforce CRM Customer 360 profile and SAP Finance overdue invoices."""
    cust = MOCK_CRM_DB["customers"].get("CUST-ACME-001", {
        "company_name": "Acme Industrial Corporation",
        "tier": "PLATINUM_ENTERPRISE",
        "arr": "$2,400,000",
        "account_executive": "David Ross (david.ross@enterprise.com)"
    })
    inv = MOCK_FINANCE_DB["invoices"].get("INV-8812", {
        "invoice_id": "INV-8812",
        "amount": "$42,500.00",
        "due_date": "2026-08-15",
        "status": "OVERDUE_30_DAYS"
    })
    return {"domain": "CRM_FINANCE", "customer": cust, "invoice": inv}

def search_hr_and_it_directory(employee_id: str = "EMP-104") -> Dict[str, Any]:
    """Query Workday HR Directory and ServiceNow IT Asset Management."""
    emp = MOCK_HR_IT_DB["employees"].get("EMP-104", {
        "employee_id": "EMP-104",
        "name": "Sarah Jenkins",
        "title": "Lead Supply Chain Operations Specialist",
        "department": "Supply Chain Operations",
        "email": "sarah.jenkins@enterprise.com",
        "assigned_hardware": {
            "laptop": "MacBook Pro 16 M3 Max (TAG-8821)",
            "monitors": ["Dell UltraSharp 32 4K (TAG-9912)", "Dell UltraSharp 32 4K (TAG-9913)"],
            "security_clearance": ["SupplyChain_Admin", "SAP_ERP_Write", "GKE_Ops_Viewer"]
        }
    })
    return {"domain": "HR_IT_DIRECTORY", "employee": emp}

def search_supply_chain_shortage(sku: str = "SKU-4091", warehouse: str = "Dallas") -> Dict[str, Any]:
    """Execute cross-system analysis for critical part shortages, impacted orders, CRM contacts, and escalation leads."""
    return {
        "domain": "CROSS_SYSTEM_CRISIS",
        "shortage": {
            "sku": sku,
            "warehouse": warehouse,
            "current_stock": 14,
            "required_stock": 50,
            "severity": "CRITICAL_SHORTAGE",
            "impacted_orders": ["ORD-98214"],
            "impacted_customers": ["Acme Industrial Corporation (CUST-ACME-001)"],
            "account_executive": "David Ross (david.ross@enterprise.com)",
            "finance_status": "Overdue Invoice INV-8812 ($42,500.00) - On Hold",
            "escalation_lead": "Sarah Jenkins (sarah.jenkins@enterprise.com, Lead Supply Chain Ops)"
        }
    }
