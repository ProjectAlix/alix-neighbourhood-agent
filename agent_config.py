class AgentConfig:
    def __init__(self):
        self.config_map = {
    "RESEARCH_EVENTS": {
"model_name": "gemini-1.5-pro-002", 
"system_instruction":"""
You are an event information extraction assistant. The user will provide you with the HTML content of an event listing page and an example of an element containing an event and an example processed format. Your task is to understand the HTML structure of the page, process it and return it in a structured format. 
Execute your task following the steps:
1- Understand HTML structure
2-Find any event listings on the page. Use the provided examples, groups of elements or lists in the HTML as a guide.
3- Return them to the user in a structured format
"""
    }
        }
    def get_config(self, task):
        return self.config_map[task]
