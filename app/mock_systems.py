"""Enterprise Mock Systems & Microservice APIs.

Provides mock datasets and tool functions for 5 enterprise domains + MCP Microservices:
1. System Selector & Navigation Menu (Target System Dropdown support)
2. Supply Chain & Logistics (Warehouse stock, shipments, carriers)
3. E-Commerce & Order Management (Orders, line items, returns, SKU lookups)
4. CRM & Customer 360 (Customer tier, account executives, support tickets)
5. Finance & Invoicing (Invoices, payment status, credit limits)
6. HR & IT Asset Directory (Employees, org hierarchy, IT equipment & access permissions)
"""

from typing import Any, Dict, List, Optional


# =====================================================================
# Target System Dropdown / Menu System Definitions
# =====================================================================

ENTERPRISE_SYSTEMS_MENU = {
    "ALL_SYSTEMS": {
        "id": "ALL_SYSTEMS",
        "display_name": "🌐 All Systems (Full Autonomous Cross-System Search)",
        "description": "Auto-detects intent and queries across all 5 enterprise domains + MCP APIs as needed.",
    },
    "SUPPLY_CHAIN": {
        "id": "SUPPLY_CHAIN",
        "display_name": "📦 Supply Chain & Logistics System",
        "description": "Warehouse stock levels, SKU shortages, shipment tracking (FedEx/DHL), delivery ETAs, supplier lead times.",
    },
    "ECOMMERCE": {
        "id": "ECOMMERCE",
        "display_name": "🛒 E-Commerce & Order Management System",
        "description": "Order lookup, line items, order status, shipping priority, SKU-to-order cross-referencing.",
    },
    "CRM": {
        "id": "CRM",
        "display_name": "👥 Salesforce CRM & Customer 360",
        "description": "Customer profiles, Enterprise/Gold tiers, ARR, Account Executive contacts, support ticket escalations.",
    },
    "FINANCE": {
        "id": "FINANCE",
        "display_name": "💳 SAP ERP Finance & Invoicing System",
        "description": "Invoice breakdown, payment statuses (Paid/Overdue/Pending), credit limits, credit risk ratings.",
    },
    "HR_IT": {
        "id": "HR_IT",
        "display_name": "💻 Workday HR & ServiceNow IT Directory",
        "description": "Employee profiles, department managers, primary IT laptops, asset tags, system security clearance roles.",
    },
    "MCP_MICROSERVICES": {
        "id": "MCP_MICROSERVICES",
        "display_name": "🔌 Connected MCP APIs & Microservices",
        "description": "Connect to external microservices via Model Context Protocol (Firebase, Google Developer Knowledge, Custom MCP).",
    },
}


def get_available_enterprise_systems() -> Dict[str, Any]:
    """Returns the list of selectable enterprise systems for target system filtering and user UI dropdowns.

    Returns:
        Dict containing available enterprise system options, display names, and descriptions.
    """
    return {
        "status": "success",
        "message": "Select a target system from the dropdown or query prefix (e.g. '[System: ECOMMERCE]') to narrow search scope.",
        "systems": list(ENTERPRISE_SYSTEMS_MENU.values()),
    }


def set_active_system_filter(system_choice: str) -> Dict[str, Any]:
    """Sets or locks the active enterprise target system for filtering search results.

    Args:
        system_choice: Selected system ID or name (e.g. 'SUPPLY_CHAIN', 'ECOMMERCE', 'CRM', 'FINANCE', 'HR_IT', 'MCP_MICROSERVICES', 'ALL_SYSTEMS').

    Returns:
        Confirmation dict with selected active system details.
    """
    choice_upper = system_choice.strip().upper().replace(" ", "_")

    matched = None
    for sys_id, details in ENTERPRISE_SYSTEMS_MENU.items():
        if choice_upper in sys_id or sys_id in choice_upper:
            matched = details
            break

    if not matched:
        # Check display names
        for details in ENTERPRISE_SYSTEMS_MENU.values():
            if choice_upper in details["display_name"].upper():
                matched = details
                break

    if matched:
        return {
            "status": "success",
            "active_system_filter": matched["id"],
            "display_name": matched["display_name"],
            "description": matched["description"],
            "message": f"Active target system filter set to '{matched['display_name']}'. Agent queries will prioritize this system.",
        }

    return {
        "status": "error",
        "message": f"Unknown system choice '{system_choice}'. Available options: {list(ENTERPRISE_SYSTEMS_MENU.keys())}",
    }


# =====================================================================
# Mock Database Datasets
# =====================================================================

MOCK_SUPPLY_CHAIN_DB = {
    "inventory": {
        "SKU-4091": {
            "sku": "SKU-4091",
            "name": "Industrial Sensor Controller X-200",
            "warehouse": "Dallas Central Hub (WH-TX-01)",
            "quantity_on_hand": 14,
            "quantity_reserved": 40,
            "stock_status": "CRITICAL_SHORTAGE",
            "supplier": "Apex Electronics Global",
            "reorder_lead_days": 18,
            "next_shipment_date": "2026-10-10",
        },
        "SKU-8812": {
            "sku": "SKU-8812",
            "name": "Heavy Duty Power Inverter 5000W",
            "warehouse": "Chicago Distribution Center (WH-IL-04)",
            "quantity_on_hand": 450,
            "quantity_reserved": 120,
            "stock_status": "HEALTHY",
            "supplier": "VoltMaster Tech Inc.",
            "reorder_lead_days": 5,
            "next_shipment_date": "2026-09-28",
        },
        "SKU-1029": {
            "sku": "SKU-1029",
            "name": "Fiber Optic Transceiver Module 100G",
            "warehouse": "San Jose Express Facility (WH-CA-02)",
            "quantity_on_hand": 8,
            "quantity_reserved": 25,
            "stock_status": "BACKORDERED",
            "supplier": "OptiWave Silicon",
            "reorder_lead_days": 30,
            "next_shipment_date": "2026-10-25",
        },
    },
    "shipments": {
        "TRK-9921": {
            "tracking_number": "TRK-9921",
            "order_id": "ORD-98214",
            "carrier": "FedEx Freight Express",
            "origin": "Dallas Central Hub (WH-TX-01)",
            "destination": "Acme Corp Warehouse, Austin TX",
            "status": "IN_TRANSIT_DELAYED",
            "delay_reason": "Severe weather alert in Waco TX transit node",
            "estimated_delivery": "2026-09-26 14:00 EST",
            "last_checkpoint": "Waco TX Sorting Facility at 2026-09-24 08:30",
        },
        "TRK-4410": {
            "tracking_number": "TRK-4410",
            "order_id": "ORD-77102",
            "carrier": "DHL Express Global",
            "origin": "Chicago Distribution Center (WH-IL-04)",
            "destination": "Globex Corp Distribution, Seattle WA",
            "status": "DELIVERED",
            "delay_reason": None,
            "estimated_delivery": "2026-09-23 11:15 PST",
            "last_checkpoint": "Signed by Receiving Desk at 2026-09-23 11:15",
        },
    },
}

MOCK_ECOMMERCE_DB = {
    "orders": {
        "ORD-98214": {
            "order_id": "ORD-98214",
            "customer_id": "CUST-ACME-001",
            "customer_name": "Acme Industrial Corporation",
            "order_date": "2026-09-20",
            "items": [
                {
                    "sku": "SKU-4091",
                    "name": "Industrial Sensor Controller X-200",
                    "qty": 40,
                    "unit_price": 1250.00,
                },
                {
                    "sku": "SKU-8812",
                    "name": "Heavy Duty Power Inverter 5000W",
                    "qty": 10,
                    "unit_price": 890.00,
                },
            ],
            "total_amount": 58900.00,
            "order_status": "PARTIALLY_SHIPPED",
            "tracking_number": "TRK-9921",
            "shipping_priority": "EXPRESS_OVERNIGHT",
        },
        "ORD-77102": {
            "order_id": "ORD-77102",
            "customer_id": "CUST-GLOBEX-002",
            "customer_name": "Globex Enterprise Solutions",
            "order_date": "2026-09-18",
            "items": [
                {
                    "sku": "SKU-8812",
                    "name": "Heavy Duty Power Inverter 5000W",
                    "qty": 5,
                    "unit_price": 890.00,
                }
            ],
            "total_amount": 4450.00,
            "order_status": "DELIVERED",
            "tracking_number": "TRK-4410",
            "shipping_priority": "STANDARD_GROUND",
        },
        "ORD-33019": {
            "order_id": "ORD-33019",
            "customer_id": "CUST-ACME-001",
            "customer_name": "Acme Industrial Corporation",
            "order_date": "2026-09-22",
            "items": [
                {
                    "sku": "SKU-1029",
                    "name": "Fiber Optic Transceiver Module 100G",
                    "qty": 20,
                    "unit_price": 3200.00,
                }
            ],
            "total_amount": 64000.00,
            "order_status": "ON_HOLD_BACKORDER",
            "tracking_number": None,
            "shipping_priority": "CRITICAL_AIR",
        },
    }
}

MOCK_CRM_DB = {
    "customers": {
        "CUST-ACME-001": {
            "customer_id": "CUST-ACME-001",
            "company_name": "Acme Industrial Corporation",
            "tier": "ENTERPRISE_PLATINUM",
            "arr": "$1,250,000",
            "account_executive": "Sarah Jenkins (EMP-104)",
            "account_executive_email": "sarah.jenkins@enterprise.com",
            "primary_contact": "John Davis (VP Infrastructure)",
            "contact_email": "jdavis@acmeind.com",
            "customer_health_score": 88,
            "escalation_flag": True,
            "escalation_note": "Customer VP expressed concern over delayed sensor shipments.",
        },
        "CUST-GLOBEX-002": {
            "customer_id": "CUST-GLOBEX-002",
            "company_name": "Globex Enterprise Solutions",
            "tier": "GOLD_TIER",
            "arr": "$420,000",
            "account_executive": "Michael Chang (EMP-208)",
            "account_executive_email": "michael.chang@enterprise.com",
            "primary_contact": "Elena Rostova (Director Procurement)",
            "contact_email": "elena@globex.com",
            "customer_health_score": 95,
            "escalation_flag": False,
            "escalation_note": None,
        },
    },
    "tickets": {
        "CUST-ACME-001": [
            {
                "ticket_id": "TCK-8810",
                "subject": "Urgent Inquiry: Order ORD-98214 Shipment Delay",
                "priority": "URGENT",
                "status": "OPEN_ESCALATED",
                "created_date": "2026-09-24 09:15",
                "assigned_agent": "Support Lead Tech (EMP-305)",
            }
        ],
        "CUST-GLOBEX-002": [],
    },
}

MOCK_FINANCE_DB = {
    "invoices": {
        "INV-2026-0891": {
            "invoice_number": "INV-2026-0891",
            "customer_id": "CUST-ACME-001",
            "order_id": "ORD-98214",
            "invoice_date": "2026-09-20",
            "due_date": "2026-10-20",
            "total_amount": 58900.00,
            "paid_amount": 0.00,
            "status": "PENDING_PAYMENT",
            "payment_terms": "NET_30",
        },
        "INV-2026-0740": {
            "invoice_number": "INV-2026-0740",
            "customer_id": "CUST-ACME-001",
            "order_id": "ORD-88120",
            "invoice_date": "2026-08-01",
            "due_date": "2026-08-31",
            "total_amount": 34500.00,
            "paid_amount": 0.00,
            "status": "OVERDUE",
            "payment_terms": "NET_30",
        },
    },
    "credit_profiles": {
        "CUST-ACME-001": {
            "credit_limit": 500000.00,
            "current_balance": 93400.00,
            "available_credit": 406600.00,
            "credit_risk_rating": "LOW_RISK",
            "overdue_invoices_count": 1,
        },
        "CUST-GLOBEX-002": {
            "credit_limit": 200000.00,
            "current_balance": 0.00,
            "available_credit": 200000.00,
            "credit_risk_rating": "EXCELLENT",
            "overdue_invoices_count": 0,
        },
    },
}

MOCK_HR_IT_DB = {
    "employees": {
        "EMP-104": {
            "employee_id": "EMP-104",
            "full_name": "Sarah Jenkins",
            "title": "Senior Enterprise Account Executive",
            "department": "Global Sales - Major Accounts",
            "manager": "David Miller (VP Sales)",
            "email": "sarah.jenkins@enterprise.com",
            "location": "Dallas HQ Office (Floor 8)",
        },
        "EMP-305": {
            "employee_id": "EMP-305",
            "full_name": "Marcus Vance",
            "title": "Supply Chain Operations Lead",
            "department": "Global Logistics & Fulfillment",
            "manager": "Karen Chen (Director Supply Chain)",
            "email": "marcus.vance@enterprise.com",
            "location": "Dallas Central Hub Warehouse",
        },
    },
    "it_assets": {
        "EMP-104": {
            "employee_id": "EMP-104",
            "primary_laptop": "MacBook Pro 16 M3 Max (Asset Tag #IT-8841)",
            "system_roles": [
                "CRM_Admin",
                "Salesforce_Enterprise_User",
                "BI_Analytics_Read",
            ],
            "security_clearance": "CONFIDENTIAL_FINANCIAL",
        },
        "EMP-305": {
            "employee_id": "EMP-305",
            "primary_laptop": "Dell Precision Workstation (Asset Tag #IT-3312)",
            "system_roles": [
                "WMS_SuperUser",
                "SAP_SupplyChain_Admin",
                "FedEx_Freight_Portal",
            ],
            "security_clearance": "OPERATIONS_FULL",
        },
    },
}


# =====================================================================
# ADK Tool Functions for System Integration
# =====================================================================


def query_supply_chain(search_query: str) -> Dict[str, Any]:
    """Queries the Supply Chain & Logistics System for warehouse inventory and shipment tracking.

    Args:
        search_query: SKU (e.g. 'SKU-4091'), tracking number (e.g. 'TRK-9921'), or keyword.

    Returns:
        Dict containing warehouse inventory details or shipment tracking status.
    """
    query_upper = search_query.strip().upper()

    # Search Inventory
    if query_upper in MOCK_SUPPLY_CHAIN_DB["inventory"]:
        return {
            "status": "success",
            "source_system": "SupplyChain_Logistics_WMS",
            "data_type": "inventory",
            "result": MOCK_SUPPLY_CHAIN_DB["inventory"][query_upper],
        }

    # Search Shipments
    if query_upper in MOCK_SUPPLY_CHAIN_DB["shipments"]:
        return {
            "status": "success",
            "source_system": "SupplyChain_Logistics_TMS",
            "data_type": "shipment_tracking",
            "result": MOCK_SUPPLY_CHAIN_DB["shipments"][query_upper],
        }

    # Keyword search across all inventory & shipments
    matching_items = []
    for item in MOCK_SUPPLY_CHAIN_DB["inventory"].values():
        if query_upper in item["name"].upper() or query_upper in item["sku"]:
            matching_items.append(item)

    for shipment in MOCK_SUPPLY_CHAIN_DB["shipments"].values():
        if (
            query_upper in shipment["order_id"]
            or query_upper in shipment["tracking_number"]
        ):
            matching_items.append(shipment)

    if matching_items:
        return {
            "status": "success",
            "source_system": "SupplyChain_Logistics",
            "data_type": "search_results",
            "results": matching_items,
        }

    return {
        "status": "not_found",
        "source_system": "SupplyChain_Logistics",
        "message": f"No supply chain record found matching '{search_query}'",
    }


def query_ecommerce_orders(query_term: str) -> Dict[str, Any]:
    """Queries the E-Commerce & Order Management System for orders by Order ID, Customer ID, or SKU.

    Args:
        query_term: Order ID (e.g. 'ORD-98214'), Customer ID (e.g. 'CUST-ACME-001'), or SKU (e.g. 'SKU-4091').

    Returns:
        Dict with order breakdown, line items, status, and shipping priority.
    """
    query_clean = query_term.strip().upper()

    # Match exact Order ID
    if query_clean in MOCK_ECOMMERCE_DB["orders"]:
        return {
            "status": "success",
            "source_system": "ECommerce_OrderManagement",
            "data_type": "order_detail",
            "result": MOCK_ECOMMERCE_DB["orders"][query_clean],
        }

    # Search by Customer ID or Customer Name or SKU in line items
    matching_orders = []
    for order_id, order in MOCK_ECOMMERCE_DB["orders"].items():
        if (
            query_clean in order["customer_id"].upper()
            or query_clean in order["customer_name"].upper()
        ):
            matching_orders.append(order)
            continue

        # Check SKU in line items
        for item in order.get("items", []):
            if query_clean in item["sku"].upper() or query_clean in item["name"].upper():
                matching_orders.append(order)
                break

    if matching_orders:
        return {
            "status": "success",
            "source_system": "ECommerce_OrderManagement",
            "data_type": "orders_search_results",
            "query": query_term,
            "count": len(matching_orders),
            "results": matching_orders,
        }

    return {
        "status": "not_found",
        "source_system": "ECommerce_OrderManagement",
        "message": f"No order records found matching '{query_term}'",
    }


def query_crm_customer_360(customer_id_or_name: str) -> Dict[str, Any]:
    """Queries the CRM System for Customer 360 profile, Account Executive, and active support tickets.

    Args:
        customer_id_or_name: Customer ID (e.g. 'CUST-ACME-001') or company name (e.g. 'Acme').

    Returns:
        Dict with customer tier, account executive, health score, and open support tickets.
    """
    query_upper = customer_id_or_name.strip().upper()

    customer_profile = None
    target_cust_id = None

    for cid, profile in MOCK_CRM_DB["customers"].items():
        if query_upper in cid or query_upper in profile["company_name"].upper():
            customer_profile = profile
            target_cust_id = cid
            break

    if customer_profile:
        tickets = MOCK_CRM_DB["tickets"].get(target_cust_id, [])
        return {
            "status": "success",
            "source_system": "Salesforce_CRM_360",
            "data_type": "customer_profile",
            "profile": customer_profile,
            "open_tickets": tickets,
        }

    return {
        "status": "not_found",
        "source_system": "Salesforce_CRM_360",
        "message": f"No CRM customer profile found for '{customer_id_or_name}'",
    }


def query_finance_invoicing(customer_or_invoice_id: str) -> Dict[str, Any]:
    """Queries the Finance & ERP Invoicing System for invoices, payment status, and credit profile.

    Args:
        customer_or_invoice_id: Customer ID (e.g. 'CUST-ACME-001') or Invoice Number (e.g. 'INV-2026-0891').

    Returns:
        Dict with invoice records, payment status, and credit risk rating.
    """
    query_upper = customer_or_invoice_id.strip().upper()

    # Exact Invoice match
    if query_upper in MOCK_FINANCE_DB["invoices"]:
        inv = MOCK_FINANCE_DB["invoices"][query_upper]
        cid = inv["customer_id"]
        credit = MOCK_FINANCE_DB["credit_profiles"].get(cid, {})
        return {
            "status": "success",
            "source_system": "SAP_ERP_Finance",
            "data_type": "invoice_detail",
            "invoice": inv,
            "credit_profile": credit,
        }

    # Customer Invoices & Credit match
    matched_invoices = [
        inv
        for inv in MOCK_FINANCE_DB["invoices"].values()
        if query_upper in inv["customer_id"].upper()
    ]
    credit_info = MOCK_FINANCE_DB["credit_profiles"].get(query_upper, None)

    if matched_invoices or credit_info:
        return {
            "status": "success",
            "source_system": "SAP_ERP_Finance",
            "data_type": "customer_financial_summary",
            "invoices": matched_invoices,
            "credit_profile": credit_info,
        }

    return {
        "status": "not_found",
        "source_system": "SAP_ERP_Finance",
        "message": f"No finance or invoice records found for '{customer_or_invoice_id}'",
    }


def query_hr_it_directory(employee_query: str) -> Dict[str, Any]:
    """Queries the Enterprise HR & IT Directory for employee profile, org structure, title, department, or IT assets.

    Args:
        employee_query: Employee ID (e.g. 'EMP-104'), name (e.g. 'Sarah Jenkins'), email, or department/title keyword (e.g. 'Supply Chain', 'Logistics').

    Returns:
        Dict with employee details, department, manager, assigned IT assets, and security clearance.
    """
    query_upper = employee_query.strip().upper()

    matching_employees = []

    for emp_id, emp in MOCK_HR_IT_DB["employees"].items():
        if (
            query_upper in emp_id
            or query_upper in emp["full_name"].upper()
            or query_upper in emp["email"].upper()
            or query_upper in emp["department"].upper()
            or query_upper in emp["title"].upper()
        ):
            assets = MOCK_HR_IT_DB["it_assets"].get(emp_id, {})
            matching_employees.append(
                {"employee": emp, "it_assets_and_access": assets}
            )

    if matching_employees:
        return {
            "status": "success",
            "source_system": "Workday_HR_ServiceNow_IT",
            "data_type": "employee_it_profile",
            "count": len(matching_employees),
            "results": matching_employees,
        }

    return {
        "status": "not_found",
        "source_system": "Workday_HR_ServiceNow_IT",
        "message": f"No employee or IT asset record found for '{employee_query}'",
    }
