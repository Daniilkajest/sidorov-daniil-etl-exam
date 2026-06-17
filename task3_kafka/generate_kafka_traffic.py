import json
import random
import os
from datetime import datetime
from kafka import KafkaProducer


BROKER = "rc1d-co2lcl7lelnha6ii.mdb.yandexcloud.net" 
TOPIC = "loans-topic"
PASSWORD = "KafkaExam2026!"

CERT_PATH = "/home/sidorovdaniil/.kafka/YandexInternalRootCA.crt" 

try:
    producer = KafkaProducer(
        bootstrap_servers=BROKER,
        security_protocol="SASL_SSL",
        sasl_mechanism="SCRAM-SHA-512",
        sasl_plain_username="kafka-user",
        sasl_plain_password=PASSWORD,
        ssl_cafile=CERT_PATH
    )
    print("Успешное подключение к Yandex Kafka!")
except Exception as e:
    print(f"Ошибка подключения: {e}")
    exit(1)

regions = ["DE-HE", "DE-BY", "DE-BE", "DE-NW"]
statuses = ["verified", "pending", "rejected"]
decision_statuses = ["manual_review", "approved", "rejected"]

print("Начинаем генерацию 20+ МБ данных. Это займет пару минут...")

# Для 20 мегабайт нам понадобится около 80 000 сообщений (каждое весит ~250-300 байт)
for i in range(1, 80001):
    data = {
        "application_id": f"loan_{random.randint(100000, 999999)}",
        "customer": {
            "customer_id": f"cust_{random.randint(100, 999)}",
            "region": random.choice(regions)
        },
        "loan": {
            "amount": random.randint(5, 50) * 1000,
            "term_months": random.choice([12, 24, 36, 48, 60])
        },
        "scoring": {
            "score": random.randint(300, 850),
            "risk_level": random.choice(["low", "medium", "high"])
        },
        "documents": [
            {
                "type": "passport",
                "status": random.choice(statuses)
            }
        ],
        "decision_status": random.choice(decision_statuses),
        "submitted_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    }

    # Отправляем JSON в топик
    producer.send(TOPIC, value=json.dumps(data).encode('utf-8'))

    # Печатаем прогресс каждые 5000 сообщений
    if i % 5000 == 0:
        print(f"Отправлено {i} сообщений...")

producer.flush()
print("Генерация завершена! 20 МБ данных успешно залиты в топик Kafka.")
