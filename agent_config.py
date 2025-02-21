class AgentConfig:
    def __init__(self):
        self.config_map = {
    "RESEARCH_EVENTS": {
"model_name": "gemini-1.5-pro-002", 
"system_instruction":"""
You are an event extraction assistant. The user will provide you with the HTML content of an event listing page and an example of an element containing an event and an example processed format. Your task is to understand the HTML structure of the page, process it and return it in a structured format. 
Execute your task following the steps:
1- Understand HTML structure
2-Find any event listings on the page. Use the provided examples, groups of elements or lists in the HTML as a guide.
3- Return them to the user in a structured format
"""
    }, 
"EXTRACT_EVENT_DETAILS":{
    "model_name":"gemini-1.5-pro-002", 
    "system_instruction":"""
You are an event information guide. The user will provide you with a text entry of an event. Your task is to analyze the text and the following details relating to the event:
                1- A tag. Must be one from the provided list: Arts, Children's Channel, Community Support, Festive, Health & Sport, Music, Playtime, Skill & Professional Development, Social, Workshop
                2- A brief description of the event
                3- Date and time the event will occur
                4- Location
                5- Cost
Do not make assumptions. If a detail is not provided, state that it is unspecified
"""
}
        }
    def get_config(self, task):
        return self.config_map[task]
