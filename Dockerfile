# FROM apache/airflow:2.11.0
FROM apache/airflow:3.0.1

COPY requirements.txt .

# RUN pip install  --no-cache-dir  -r requirements.txt

# from doc:
# ADD requirements.txt .
RUN pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt
