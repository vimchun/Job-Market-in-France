FROM apache/airflow:3.0.2

COPY airflow/requirements.txt .

RUN pip install apache-airflow==${AIRFLOW_VERSION}  -r requirements.txt
