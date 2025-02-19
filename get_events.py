from agent import EventResearchAgent
from website_config import n19qz_websites_config, me156jq_websites_config
import asyncio, json, time, random
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
from bs4 import BeautifulSoup
from typing import List
import asyncio
import logging



async def read_webpage(url: str):
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
            for tag in body.find_all():
                tag.attrs = {k: v for k, v in tag.attrs.items() if k == "href"}
            return str(body)
        except Exception as e:
            logging.error(f"Error occured reading {url}:{e}")
            return None
        finally:
            await context.close()


async def get_events(event_research_agent: EventResearchAgent, website_list:List):
    tasks = []
    extracted_events = []
    for website in website_list:
        tasks.append(read_webpage(website["url"]))
    results = await asyncio.gather(*tasks)  # Run all tasks concurrently
    for website, content in zip(website_list, results):
        if content is None:
            logging.error(f"Skipping {website['url']} due to missing content.")
            continue
        container_html=BeautifulSoup(website['container_html'], "html.parser")
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
        max_retries = 5
        base_delay = 1  
        for attempt in range(max_retries):
            try:
                output = event_research_agent.run_task(prompt)
                extracted_events.append(output)  
                break 
            except Exception as e:
                wait_time = base_delay * (2 ** attempt) + random.uniform(0, 0.5)
                logging.error(f"Error processing {website['url']}: {e}. Retrying in {wait_time:.2f} seconds...")
                time.sleep(wait_time)
        else:
            logging.error(f"Failed to process {website['url']} after {max_retries} retries. Skipping.")
            continue  
    with open("extracted_events_me156jq.json", "w") as f:
        f.write(json.dumps(extracted_events))
    return extracted_events

agent=EventResearchAgent()
website_list=me156jq_websites_config['websites']

asyncio.run(get_events(agent, website_list))