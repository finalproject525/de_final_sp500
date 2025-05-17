# 🐳 Docker Setup – SP500 Final Project

This folder contains the complete Docker configuration for running and developing the `sp500` project locally using Docker Compose.

---

## 📦 Included Services

| Service            | Description                                                              |
|--------------------|--------------------------------------------------------------------------|
| `kafka`            | Kafka broker for streaming financial data                                |
| `zookeeper`        | Coordination service required by Kafka                                   |
| `postgres`         | PostgreSQL database used by Airflow                                      |
| `airflow-webserver`| Web UI to manage Airflow DAGs                                            |
| `airflow-scheduler`| Schedules and executes Airflow DAGs                                      |
| `airflow-init`     | Initializes Airflow and creates default admin user                       |
| `kafka-producer`   | Produces financial data to Kafka using `yfinance`                        |
| `kafka-consumer`   | Spark Streaming job: consumes Kafka and writes to S3                     |
| `dev_env_light`    | Lightweight development container with SSH, Apache Spark, Python, etc.   |

---

## 🚀 Getting Started

### 1. Build and launch all services

Run from this directory:

```bash
docker-compose up --build -d
```

This uses the project name defined in `.env`:

```env
COMPOSE_PROJECT_NAME=sp500_final
```

---

## 💻 Connect via VS Code (Remote SSH)

1. Open VS Code
2. Connect to `dev_env_light` using port `22023`
3. Default credentials: `user=root`, `password=root` (or use SSH key if configured)

Optional entry for your `~/.ssh/config`:

```ssh
Host sp500-dev
  HostName localhost
  Port 22023
  User root
```

---

## 🧪 Python Virtual Environment

Inside the container or via VS Code:

```bash
cd /project/workspace/sp500
./utils/bootstrap_venv.sh
```

This script will:
- Create `.venv/` in the project root
- Install dependencies from `requirements.txt`
- Automatically activate the virtual environment in future sessions

---

## ⚙️ Apache Spark

Apache Spark 3.5 is installed at `/opt/spark`.

You can run:
```bash
spark-submit your_script.py
pyspark
```

The Spark UI is available at:
[http://localhost:4040](http://localhost:4040)

---

## 📁 Folder Structure

```
docker/
├── docker-compose.yaml       # Docker services definition
├── Dockerfile.dev_env_light  # Dev container with SSH, Spark, Python
├── Dockerfile.producer       # Kafka producer container
├── Dockerfile.spark_consumer # Spark consumer container
├── .env                      # Compose project name
└── README.md                 # This file
```

---

## 📝 Notes

- Root password is `root` (development only)
- Airflow UI: [http://localhost:8083](http://localhost:8083)
- The project code is shared in `workspace/sp500` and accessible to all services

---
