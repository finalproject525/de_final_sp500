from finance.YahooFinance import YahooBatchFinanceClient


class YahooFinanceClient:
    """
    Client that retrieves stock market data from Yahoo Finance
    and yields it in batches.
    """
    def __init__(self, symbols, batch_size, period, interval):
        self.symbols = symbols
        self.batch_size = batch_size
        self.period = period
        self.interval = interval

    def fetch_batches(self):
        """
        Yield batches of market data as list of dictionaries.
        """
        client = YahooBatchFinanceClient(
            symbols=self.symbols,
            batch_size=self.batch_size,
            period=self.period,
            interval=self.interval
        )

        for batch in client._chunk_list(self.symbols, self.batch_size):
            client_batch = YahooBatchFinanceClient(
                symbols=batch,
                batch_size=self.batch_size,
                period=self.period,
                interval=self.interval
            )
            client_batch.fetch_all()
            yield client_batch.to_dict_records()
