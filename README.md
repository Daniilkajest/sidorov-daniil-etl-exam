

sidorov-daniil-etl-exam

Практическая работа. Модуль 4 (экзамен)

Дисциплина: ETL-процессы

Студент: Сидоров Даниил

Преподаватель: Артём Озерков
Цель проекта

Интеграция новых источников данных и реализация ETL/Streaming-процессов с использованием стека Yandex Cloud для формирования аналитической отчетности.
Отчет о проделанной работе

Задание 1. Работа с Yandex DataTransfer

Статус: Выполнено
![Task 1 Execution](https://github.com/user-attachments/assets/9f83b2df-2eaa-4b07-8fec
Описание: Настроена миграция данных из исходных источников в Yandex Object Storage.

Задание 2. Автоматизация при помощи Apache AirFlow

Статус: Выполнено

Описание: Разработан DAG для оркестрации Spark-задач. Процесс автоматизирует обработку данных и их сохранение в целевой бакет.
### Логика работы DAG (spark_job_dag):
1. **Create Cluster** (Managed Service for Data Processing)
2. **Execute PySpark Job** (обработка данных в S3)
3. **Delete Cluster** (очистка ресурсов для экономии)

Технические логи выполнения задачи:
![Logs](https://github.com/user-attachments/assets/712f22ce-c807-405c-8795-f73cb9d191e3)
Задание 3. Работа с Apache Kafka и PySpark

Статус: Выполнено
### Техническое подтверждение работы пайплайна:
![Pipeline Logs](https://github.com/user-attachments/assets/712f22ce-c807-405c-8795-f73cb9d191e3)
![Query Execution](https://github.com/user-attachments/assets/e8612076-960e-4270-8c50-aa65ac9b8b0c)
![Processing Results](https://github.com/user-attachments/assets/f025bc70-ad21-49f7-8e00-d66edc735c7c)
Описание: Реализован Structured Streaming для чтения и парсинга вложенного JSON-потока в плоскую структуру DataFrame.

Задание 4. Визуализация в DataLens

Статус: Выполнено


Описание: Данные, полученные в результате ETL-процесса, были визуализированы в DataLens. Загрузка данных производилась через предварительно подготовленный CSV-файл, полученный из S3.

[Посмотреть настройки DataLens](https://github.com/user-attachments/assets/fc2eaedb-5c3f-44fb-b43a-3b81387c833d)

