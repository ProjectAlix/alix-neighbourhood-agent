from agent import EventResearchAgent, EventInfoExtractionAgent, NewsletterWriterAgent
from website_config import n19qz_websites_config, me156jq_websites_config
from website_config_schema import WebsiteConfig
from get_events import get_events
from make_table import make_table
import asyncio

async def main():
    event_research_agent=EventResearchAgent()
    event_info_extraction_agent=EventInfoExtractionAgent()
    newsletter_writer_agent=NewsletterWriterAgent()
    website_config=WebsiteConfig(**me156jq_websites_config)
    processed_events=await get_events(event_research_agent, event_info_extraction_agent, website_config)
    formatted_events=make_table(processed_events)
    formatted_events=formatted_events.to_string()
    # formatted_events.to_csv("me156jq.csv
    agent=NewsletterWriterAgent()
    prompt=f"""
    Event listings:
    ---------------
    {formatted_events}
    """
    newsletter_writer_agent.run_task(prompt)