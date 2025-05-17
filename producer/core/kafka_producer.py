import json
from kafka import KafkaProducer


class ProducerManager:
    """
    Wrapper around KafkaProducer to send JSON-encoded messages to a topic.
    """
    def __init__(self, broker):
        self.producer = KafkaProducer(
            bootstrap_servers=broker,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            api_version=(2, 8)
        )

    def send_messages(self, topic, messages):
        print(f"🛠 Sending to topic: {topic}, number of messages: {len(messages)}")

        for msg in messages:
            try:
                self.producer.send(topic, value=msg)
            except Exception as e:
                print(f"❌ Failed to send message: {e}")
                raise

        self.producer.flush()
