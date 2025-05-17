import json
from kafka import KafkaProducer


class ProducerManager:
    """
    Wrapper around KafkaProducer to send JSON-encoded messages to a topic.
    """
    def __init__(self, broker):
        self.producer = KafkaProducer(
            bootstrap_servers=broker,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def send_messages(self, topic, messages):
        """
        Send a list of messages to the given Kafka topic.
        """
        for msg in messages:
            self.producer.send(topic, value=msg)
        self.producer.flush()
