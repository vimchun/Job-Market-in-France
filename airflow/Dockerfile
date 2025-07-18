FROM apache/airflow:3.0.3

COPY airflow/requirements.txt .

RUN pip install apache-airflow==${AIRFLOW_VERSION}  -r requirements.txt
