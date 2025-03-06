from agent import EventResearchAgent, EventInfoExtractionAgent, NewsletterWriterAgent
from website_config import n19qz_websites_config, me156jq_websites_config
from website_config_schema import WebsiteConfig
from get_events import get_events
from make_table import make_table
from email_service import EmailService
from typing import List
import logging, io




   
async def generate_newsletter(recipient_emails:List[str]=[]):
    try:
        email_service=EmailService(sender_email="daria@projectalix.com")
        event_research_agent=EventResearchAgent()
        event_info_extraction_agent=EventInfoExtractionAgent()
        newsletter_writer_agent=NewsletterWriterAgent()
        website_config=WebsiteConfig(**me156jq_websites_config)
        processed_events=await get_events(event_research_agent, event_info_extraction_agent, website_config)
        formatted_events=make_table(processed_events)
        csv_buffer=io.StringIO()
        formatted_events.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        prompt=f"""
        Event listings:
        ---------------
        {formatted_events.to_string()}
        """
        newsletter=newsletter_writer_agent.run_task(prompt)
        attachments={
"events.csv":csv_buffer.getvalue(),
"newsletter.md":newsletter
        }
        email_service.send_email_with_attachment(content="A newsletter", subject="Newsletter", recipient_emails=recipient_emails, attachments=attachments)
        message="Newsletter sent successfully!"
        response= {
            "message": message, 
            "data":{
                "text": newsletter, "table": formatted_events.to_string() # Maybe we can display the response on the frontend as well idkkkk
            }
        } 
        print(response)
        return response
    except Exception as e:
        message=f"An error occurred generating newsletter:{e}"
        logging.error(message)
        return {
            "message": message, "data":None
        }

