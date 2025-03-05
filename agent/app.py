from flask import Flask
from pubsub_client import PubSubClient
from generate_newsletter import generate_newsletter
import os

app = Flask(__name__)

GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
SUBSCRIPTION_ID = os.getenv("SUBSCRIPTION_ID")

pubsub_client = PubSubClient(GOOGLE_PROJECT_ID, SUBSCRIPTION_ID)

@app.route('/')
def index():
    return 'Pub/Sub Listener is running!'

@app.route('/newsletter')
async def get_newsletter():
    response=await generate_newsletter()
    return response