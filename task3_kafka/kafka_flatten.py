from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, explode_outer
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType

# Инициализируем Spark
spark = SparkSession.builder.appName("KafkaFlattenStreaming").getOrCreate()

# 1. Описываем сложную вложенную структуру нашего JSON (по ТЗ)
schema = StructType([
    StructField("application_id", StringType()),
    StructField("customer", StructType([
        StructField("customer_id", StringType()),
        StructField("region", StringType())
    ])),
    StructField("loan", StructType([
        StructField("amount", IntegerType()),
        StructField("term_months", IntegerType())
    ])),
    StructField("scoring", StructType([
        StructField("score", IntegerType()),
        StructField("risk_level", StringType())
    ])),
    StructField("documents", ArrayType(StructType([
        StructField("type", StringType()),
        StructField("status", StringType())
    ]))),
    StructField("decision_status", StringType()),
    StructField("submitted_at", StringType())
])

# 2. Подключаемся к Kafka и читаем поток
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "rc1d-co2lcl7lelnha6ii.mdb.yandexcloud.net:9091") \
    .option("subscribe", "loans-topic") \
    .option("kafka.security.protocol", "SASL_SSL") \
    .option("kafka.sasl.mechanism", "SCRAM-SHA-512") \
    .option("kafka.sasl.jaas.config", 'org.apache.kafka.common.security.scram.ScramLoginModule required username="kafka-user" password="KafkaExam2026!";') \
    .option("startingOffsets", "earliest") \
    .load()

# 3. Достаем JSON из бинарного формата Kafka и применяем схему
parsed_df = kafka_df.selectExpr("CAST(value AS STRING) as json_str") \
    .select(from_json(col("json_str"), schema).alias("data")) \
    .select("data.*")

# 4. РАЗГЛАЖИВАЕМ (Flatten) вложенные объекты и массивы
flattened_df = parsed_df \
    .select(
        col("application_id"),
        col("customer.customer_id").alias("customer_id"),
        col("customer.region").alias("region"),
        col("loan.amount").alias("loan_amount"),
        col("loan.term_months").alias("term_months"),
        col("scoring.score").alias("credit_score"),
        col("scoring.risk_level").alias("risk_level"),
        col("decision_status"),
        col("submitted_at"),
        col("documents")
    ) \
    .withColumn("document", explode_outer("documents")) \
    .select(
        "*",
        col("document.type").alias("doc_type"),
        col("document.status").alias("doc_status")
    ) \
    .drop("documents", "document") # Удаляем старые вложенные колонки

# 5. Пишем плоскую таблицу в Object Storage (S3) в формате Parquet
query = flattened_df.writeStream \
    .format("parquet") \
    .option("path", "s3a://sidorov-etl-exam-bucket/kafka_processed/") \
    .option("checkpointLocation", "s3a://sidorov-etl-exam-bucket/kafka_checkpoints/") \
    .trigger(once=True) \
    .start()

# Даем стриму поработать 3 минуты, чтобы он успел выкачать все 80 000 строк, и завершаем
query.awaitTermination(180) 
print("Обработка Kafka завершена! Данные лежат в S3.")
