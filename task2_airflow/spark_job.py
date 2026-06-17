import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

def main():
    # Инициализация Spark сессии
    spark = SparkSession.builder \
        .appName("Exam_ETL_Loan_Processing") \
        .getOrCreate()

    # Пути к бакету (S3A коннектор для Yandex Cloud)
    input_path = "s3a://sidorov-etl-exam-bucket/loan_applications.csv"
    output_path = "s3a://sidorov-etl-exam-bucket/processed_loans_parquet/"

    print(f"Reading data from: {input_path}")
    
    # Чтение сырого CSV
    df = spark.read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .csv(input_path)

    # Трансформация: берем только одобренные заявки и тех, у кого нормальный кредитный рейтинг
    processed_df = df.filter(
        (col("decision_status") == "approved") & 
        (col("credit_score") >= 400)
    )

    print(f"Writing processed data to: {output_path}")

    # Запись результата в Parquet (с перезаписью, если папка уже есть)
    processed_df.write \
        .mode("overwrite") \
        .parquet(output_path)

    print("PySpark job successfully completed!")

if __name__ == "__main__":
    main()
