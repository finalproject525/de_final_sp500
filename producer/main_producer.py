import queue
from producer.core import YahooFinanceClient, ProducerManager, FinanceFetcher, KafkaSender
from config import USE_SYMBOLES_TEST, SYMBOLS_TEST, BROKER, TOPIC, PERIOD, INTERVAL, API_BATCH_SIZE
from finance.functions import get_sp500_symbol


def main(params=None):
    """
    Main entrypoint: sets up the pipeline and runs fetch/send threads.
    Accepts optional override parameters for Airflow or CLI.
    """
    params = params or {}

    use_symbols_test = params.get("use_symbols_test", USE_SYMBOLES_TEST)
    symbols_test = params.get("symbols_test", SYMBOLS_TEST)
    broker = params.get("broker", BROKER)
    topic = params.get("topic", TOPIC)
    period = params.get("period", PERIOD)
    interval = params.get("interval", INTERVAL)
    batch_size = params.get("batch_size", API_BATCH_SIZE)
    api_name = params.get("api_name", "yahoo")

    # Select symbols to fetch
    symbols = symbols_test if use_symbols_test else get_sp500_symbol()['Symbol'].to_list()

    data_queue = queue.Queue()

    # Choose client
    if api_name == "yahoo":
        client = YahooFinanceClient(symbols, batch_size, period, interval)
    else:
        raise NotImplementedError(f"API '{api_name}' is not supported.")

    producer = ProducerManager(broker)
    fetcher = FinanceFetcher(client, data_queue)
    sender = KafkaSender(producer, topic, data_queue)

    # Start threads
    fetcher.start()
    sender.start()
    fetcher.join()
    sender.join()


if __name__ == "__main__":
    main()
