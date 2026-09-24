from google.adk.agents import LlmAgent
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from app.intent import STATIC_ENTERPRISE_SEARCH_INSTRUCTION
from app.search_tools import (
    search_orders_and_logistics,
    search_customer_360_finance,
    search_hr_and_it_directory,
    search_supply_chain_shortage
)
from app.image_gen_tools import generate_search_diagram
from app.a2ui_utils import a2ui_search_callback

agent = LlmAgent(
    name="enterprise_ai_search",
    model="gemini-2.5-flash",
    description="Enterprise Smart Search Agent across Supply Chain, CRM, SAP Finance, and HR/IT",
    instruction=STATIC_ENTERPRISE_SEARCH_INSTRUCTION,
    tools=[
        PreloadMemoryTool(),
        search_orders_and_logistics,
        search_customer_360_finance,
        search_hr_and_it_directory,
        search_supply_chain_shortage,
        generate_search_diagram,
    ],
    after_model_callback=a2ui_search_callback,
)
