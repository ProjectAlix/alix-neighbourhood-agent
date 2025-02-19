from pydantic import BaseModel
from typing import List

class Website(BaseModel):
    url:str
    example:str
    container_html:str

class WebsiteConfig(BaseModel):
    postcode: str
    websites: List[Website]