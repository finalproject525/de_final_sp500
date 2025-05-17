""" 
To improve the modularity, clarity, and scalability.
The main_*.py scripts were moved into their respective folders (producer/, consumer/, etc.) to better organize the code by component.
This structure aligns with our Airflow-based orchestration, where each script will be executed in its own dedicated Docker container.
A run.py file was added at the root to simplify local development and testing without breaking Python module imports. 
"""
import sys
import os

# Add the parent directory of 'producer' to PYTHONPATH
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from producer.main_producer import main

if __name__ == "__main__":
    main()
