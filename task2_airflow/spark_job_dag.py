from airflow import DAG
from airflow.providers.yandex.operators.yandexcloud_dataproc import DataProcCreateJobOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'Daniil Sidorov',
    'start_date': datetime(2026, 6, 18),
}

with DAG(
    'kafka_to_s3_etl_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:

    # Запуск PySpark задания
    run_spark_job = DataProcCreateJobOperator(
        task_id='run_kafka_flatten_job',
        cluster_id='c9qocqvg94ksoian7qm2', # Твой ID кластера
        pyspark_job={
            'main_python_file_uri': 's3a://sidorov-etl-exam-bucket/kafka_flatten.py',
            'properties': {
                'spark.jars.packages': 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2'
            }
        }
    )
