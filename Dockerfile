FROM apache/airflow:3.0.2

COPY requirements.txt .

RUN pip install apache-airflow==${AIRFLOW_VERSION}  -r requirements.txt
