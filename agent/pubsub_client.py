from google.cloud import pubsub_v1
from generate_newsletter import generate_newsletter
import asyncio
class PubSubClient:
    def __init__(self, project_id, subscription_id):
        self.subscriber=pubsub_v1.SubscriberClient()
        self.subscription_path = self.subscriber.subscription_path(project_id, subscription_id)

    def process_message(self, message):
        print(f"Received message: {message.data.decode('utf-8')}")
        message.ack()
        response=asyncio.run(generate_newsletter())
        print(response)


    def listen_for_messages(self):
        future = self.subscriber.subscribe(self.subscription_path, callback=self.process_message)
        print(f"Listening for messages on {self.subscription_path}...")

        try:
            future.result()  # Keep listening
        except KeyboardInterrupt:
            future.cancel()

    