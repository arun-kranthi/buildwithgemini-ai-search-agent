from google.adk.agents import LlmAgent
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from app.intent import STATIC_ENTERPRISE_SEARCH_INSTRUCTION
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
from app.a2ui_utils import a2ui_search_callback

agent = LlmAgent(
    name="nexus_search_master",
    model="gemini-2.5-flash",
    description="NexusSearch Enterprise AI Master Explorer across 5 Enterprise Domains, Public REST APIs, and Connected MCP Microservices",
    instruction=STATIC_ENTERPRISE_SEARCH_INSTRUCTION,
    tools=[
        PreloadMemoryTool(),
        search_orders_and_logistics,
        search_customer_360_finance,
        search_hr_and_it_directory,
        search_supply_chain_shortage,
        fetch_crypto_prices,
        fetch_weather_forecast,
        fetch_country_trade_info,
        fetch_tech_news_search,
        get_mcp_servers,
        call_mcp_microservice,
        generate_search_diagram,
    ],
    after_model_callback=a2ui_search_callback,
)
