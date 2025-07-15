# Spotify Data Pipeline

This project is a data pipeline for processing and analyzing Spotify data using `dbt`, `Airflow` and `PostgreSQL`.

## Prerequisites

- [Python 3.10](https://www.python.org/)
- [spotipy](https://spotipy.readthedocs.io/en/2.25.1/)
- [Pandas](https://pandas.pydata.org/)
- [PyArrow](https://arrow.apache.org/docs/python/index.html)
- [Psycopg2](https://www.psycopg.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Airflow](https://airflow.apache.org/docs/apache-airflow/stable/start.html)
- [dbt](https://docs.getdbt.com/docs/getting-started)

## Installation

1. **Clone this repository**:
   ```bash
   git clone https://github.com/Heryhelder/spotify-data-pipeline.git
   cd spotify-data-pipeline
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. **Install the Python packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your PostgreSQL database**:
   - Ensure that PostgreSQL is running.
   - Create a schema named `user-read-recently-played`.

5. **Set up spotipy**:
   - Create a Spotify client ID and client secret. [Instructions via spotipy](https://spotipy.readthedocs.io/en/2.25.1/#getting-started)
   - Set the `SPOTIPY_CLIENT_ID` and `SPOTIPY_CLIENT_SECRET` environment variables.

## How to Run

1. **Initialize Airflow**:
   ```bash
   airflow standalone
   ```

2. **Access the Airflow UI**: Open a web browser and go to `http://localhost:8080`.

3. **Run the DAG**: Click on the "DAGs" tab, choose the DAG you want to run, then click on "Run DAG".

## Resources

- [spotipy docs](https://spotipy.readthedocs.io/en/2.25.1/)
- [dbt docs](https://docs.getdbt.com/docs/introduction)
- [Airflow docs](https://airflow.apache.org/docs/apache-airflow/stable/index.html)
- [PostgreSQL docs](https://www.postgresql.org/docs/)
- [Pandas](https://pandas.pydata.org/docs/)
- [PyArrow](https://arrow.apache.org/docs/python/index.html)
- [Psycopg2](https://www.psycopg.org/docs/)