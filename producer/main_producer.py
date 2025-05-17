from kafka_clients import StockDataProducerApp
from config import INTERVAL as DEFAULT_INTERVAL, PERIOD as DEFAULT_PERIOD

def launch_producer(api: str, topic: str, interval=None, period=None):
    interval = interval or DEFAULT_INTERVAL
    period = period or DEFAULT_PERIOD

    app = StockDataProducerApp(api=api, topic=topic, interval=interval, period=period)
    app.run()


if __name__ == "__main__":
    launch_producer(api="yahoo", topic="finance-topic")
