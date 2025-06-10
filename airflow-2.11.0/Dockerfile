FROM apache/airflow:2.11.0
# FROM apache/airflow:3.0.1

COPY requirements.txt .

# testé sur 2.11.0 :
# RUN pip install  --no-cache-dir  -r requirements.txt

# testé sur 3.0.1 :
RUN pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt
