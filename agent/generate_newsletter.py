from agent import EventResearchAgent, EventInfoExtractionAgent, NewsletterWriterAgent
from website_config import n19qz_websites_config, me156jq_websites_config
from website_config_schema import WebsiteConfig
from get_events import get_events
from make_table import make_table
from email_service import EmailService
import logging



   
async def generate_newsletter():
    try:
        email_service=EmailService(sender_email="daria@projectalix.com")
        recipient_email="darianaumova5@gmail.com"
        event_research_agent=EventResearchAgent()
        event_info_extraction_agent=EventInfoExtractionAgent()
        newsletter_writer_agent=NewsletterWriterAgent()
        website_config=WebsiteConfig(**me156jq_websites_config)
        processed_events=await get_events(event_research_agent, event_info_extraction_agent, website_config)
        formatted_events=make_table(processed_events)
        csv_file_path="me156jq_table.csv"
        md_file_path="me156jq.md"
        formatted_events.to_csv(csv_file_path)
        formatted_events=formatted_events.to_string()
        prompt=f"""
        Event listings:
        ---------------
        {formatted_events}
        """
        newsletter=newsletter_writer_agent.run_task(prompt)
        with open(md_file_path, "w") as f:
            f.write(newsletter)
        email_service.send_email_with_attachment(content="A newsletter", subject="Newsletter", recipient_email=recipient_email, attachment_file_paths=[csv_file_path, md_file_path])
        response= {
            "message": message, 
            "data":{
                "text": newsletter, "table": formatted_events # Maybe we can display the response on the frontend as well idkkkk
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

