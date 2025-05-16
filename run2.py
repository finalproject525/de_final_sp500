""" 
To improve the modularity, clarity, and scalability.
The main_*.py scripts were moved into their respective folders (producer/, consumer/, etc.) to better organize the code by component.
This structure aligns with our Airflow-based orchestration, where each script will be executed in its own dedicated Docker container.
A run.py file was added at the root to simplify local development and testing without breaking Python module imports. 
"""
from producer.main_producer import main as main_prod_yfinance
from consumer.main_consumer import main as main_cons_yfinance


main_cons_yfinance()