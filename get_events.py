from agent import EventResearchAgent, EventInfoExtractionAgent
from website_config import n19qz_websites_config, me156jq_websites_config
from website_config_schema import WebsiteConfig
import asyncio, json, time, random
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
from bs4 import BeautifulSoup
from typing import List
import asyncio
import logging



async def read_webpage(url: str, get_text:bool):
    TIMEOUT = 60000
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
            )
            page = await context.new_page()
            await stealth_async(page)
            await page.goto(url, timeout=TIMEOUT, wait_until="networkidle")
            content = await page.content()
            soup = BeautifulSoup(content, "html.parser")
            # for element in soup(['style', 'script']):
            #     element.decompose()
            body = soup.body
            if body is None:
                raise ValueError("Body element not found")
            if get_text:
                return body.get_text()
            for tag in body.find_all():
                tag.attrs = {k: v for k, v in tag.attrs.items() if k == "href"}
            return str(body)
        except Exception as e:
            logging.error(f"Error occured reading {url}:{e}")
            return None
        finally:
            await context.close()

async def extract_events(event_research_agent:EventResearchAgent, website_list: List):
    semaphore = asyncio.Semaphore(10)  # Limit concurrent requests to prevent overloading
    extracted_events = []

    async def fetch_and_process(website):
        async with semaphore:
            content = await read_webpage(website["url"], get_text=False)  
        if content is None:
            logging.error(f"Skipping {website['url']} due to missing content.")
            return []

        # Clean container HTML
        container_html = BeautifulSoup(website['container_html'], "html.parser")
        for tag in container_html.find_all():
            tag.attrs = {k: v for k, v in tag.attrs.items() if k == "href"}

        prompt = f"""
        HTML Content:
        {str(content)}
        Example format:
        {website['example']}
        Example html event container:
        {str(container_html)}
        """

        # Retry mechanism for LLM response
        max_retries = 5
        base_delay = 1  
        for attempt in range(max_retries):
            try:
                output = await asyncio.to_thread(event_research_agent.run_task, prompt)  # Run in thread pool
                if isinstance(output, dict) and "events" in output:
                    return output["events"]
                else:
                    logging.error(f"Unexpected response format from {website['url']}: {output}")
                    return []
            except Exception as e:
                wait_time = base_delay * (2 ** attempt) + random.uniform(0, 0.5)
                logging.error(f"Error processing {website['url']}: {e}. Retrying in {wait_time:.2f} seconds...")
                await asyncio.sleep(wait_time)
        logging.error(f"Failed to process {website['url']} after {max_retries} retries. Skipping.")
        return []

    tasks = [fetch_and_process(website) for website in website_list]
    results = await asyncio.gather(*tasks)

    extracted_events = [event for sublist in results for event in sublist]

    # Step 2: Save combined events to JSON
    # with open("extracted_events.json", "w") as f:
    #     json.dump(extracted_events, f, indent=2)

    return extracted_events

async def get_event_details(event_info_extraction_agent, extracted_events: List):
    semaphore = asyncio.Semaphore(10)  # Limit concurrency
    async def extract_detail(event):
        async with semaphore:
            if event.get("detail_link") and event.get("detail_link")!="":
                content = await read_webpage(event["detail_link"], get_text=True)
                if content is None:
                    logging.error(f"Skipping {event['title']} due to missing content.")
                    return event # Return the unmodified event
            else:
                content=json.dumps(event)
            prompt = f"Event:\n{content}"
            max_retries = 5
            base_delay = 1  
            for attempt in range(max_retries):
                    try:
                        output = await asyncio.to_thread(event_info_extraction_agent.run_task, prompt)
                        if isinstance(output, dict):
                            event['details'] = output  # Update event with extracted details
                        else:
                            logging.error(f"Unexpected response format from {event['detail_link']}: {output}")
                        return event  # Return modified event
                    except Exception as e:
                        wait_time = base_delay * (2 ** attempt) + random.uniform(0, 0.5)
                        logging.error(f"Error processing {event['detail_link']}: {e}. Retrying in {wait_time:.2f} seconds...")
                        await asyncio.sleep(wait_time)

            logging.error(f"Failed to process {event['detail_link']} after {max_retries} retries. Skipping.")
        return event  # Ensure event is always returned

    # Run all tasks concurrently
    tasks = [extract_detail(event) for event in extracted_events]
    processed_events = await asyncio.gather(*tasks)
    return processed_events  # Return updated list of events


async def get_events(event_research_agent: EventResearchAgent, event_info_extraction_agent:EventInfoExtractionAgent, website_config:WebsiteConfig):
    start_time=time.time()# TO-DO inject dependency here
    website_list=website_config.websites
    website_list=[website.model_dump(by_alias=True) for website in website_list]
    extracted_events=await (extract_events(event_research_agent,website_list))
    processed_events=await (get_event_details(event_info_extraction_agent, extracted_events))
    with open("final_output.json", "w") as f:
        f.write(json.dumps(processed_events))
    end_time = time.time()  # End timing
    elapsed_time = end_time - start_time
    print(f"Script completed in {elapsed_time:.2f} seconds.")

event_research_agent=EventResearchAgent()
event_info_extraction_agent=EventInfoExtractionAgent()
website_config=WebsiteConfig(**me156jq_websites_config)
asyncio.run(get_events(event_research_agent, event_info_extraction_agent, website_config))