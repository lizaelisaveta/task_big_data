# Task Big Data

## Описание

Проект реализует ML API для предсказания длительности поездки на такси, использует Kafka для передачи результатов и PostgreSQL для хранения инференсов. DVC используется для работы с датасетом.

## Требования

* Python 3.11
* Docker & Docker Compose
* DVC

## Установка и настройка

### 1. Клонируем репозиторий и создаем виртуальное окружение

```bash
git clone https://github.com/username/task_big_data.git task_big_data
cd task_big_data
python -m venv .venv
source .venv/bin/activate
```

### 2. Загружаем переменные окружения и Vault

```bash
export $(cat .env | xargs)
export VAULT_PASS=ваш_пароль
```

### 3. Загрузка данных через DVC из бакета Yandex Cloud

```bash
dvc pull
```

### 4. Воспроизведение пайплайна DVC для предобработки данных и обучения модели

```bash
dvc repro
```

### 5. Сборка и запуск Docker-контейнеров

```bash
docker-compose build
docker-compose up -d
```


## Структура проекта

```
task_big_data/
│
├─ .dvc/
│  └─ config              # Настройки для подключения к облачному хранилищу
├─ ansible/
│  └─ secrets.yml         # Зашифрованные секреты
├─ data/                  # Папка для данных и предобработанных 
│  ├─ processed/
│  └─ raw/
├─ model/                 # Сохранённая ML модель
├─ notebooks/  
│  └─ model.ipynb/        # Блокнот с обзором датасета и кодом модели 
├─ tests/
│  ├── conftest.py        # фикстуры для базы данных и клиента FastAPI
│  ├── test_api.py        # тесты для FastAPI
│  ├── test_model.py      # тесты модели
│  ├── test_kafka.py      # тесты Kafka producer/consumer
│  ├── test_preprocess.py # тесты предобработки
│  └── test_train.py      # тесты обучения
├─ src/
│  ├─ api/
│  │  ├─ main.py          # FastAPI сервис
│  │  └─ db.py            # Работа с БД через SQLAlchemy(PostgreSQL)
│  ├─ kafka_producer.py   # Producer Kafka
│  ├─ kafka_consumer.py   # Consumer Kafka
│  ├─ model.py            # Для загрузки обученной модели
│  ├─ preprocess.py       # Предобработка данных
│  └─ train.py            # Обучение модели
├─ Dockerfile
├─ docker-compose.yml
├─ requirements.txt
├─ dvc.yaml               # Пайплайн предобработки и обучения модели
├─ generate_env.py        # Расшифровка секретов в .env
└─ wait-for-kafka.sh      # Скрипт ожидания включения Kafka
```

## Использование

### Сервисы:
*  app — FastAPI API
*  kafka_consumer — потребитель сообщений Kafka и запись в БД
*  postgres — база данных
*  kafka + zookeeper — система обмена сообщениями

### 1. Проверка статуса API

```bash
curl http://localhost:8000/
```

Ожидаемый ответ:

```json
{"status": "ok", "message": "ML API is running 🚀"}
```

### 2. Отправка запроса на предсказание

```bash
curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d '{"trip_distance":3.5,"passenger_count":1}'
```

Ожидаемый ответ:

```json
{"prediction": 1131.76}
```

### 3. Проверка записей в PostgreSQL

```bash
docker exec -it task_big_data-postgres-1 psql -U postgres -d modeldb
modeldb=# SELECT * FROM inference_results;
```

### 4. Просмотр сообщений в Kafka

```bash
docker exec -it task_big_data-kafka-1 kafka-console-consumer --bootstrap-server kafka:9092 --topic model_results --from-beginning
```

## Интеграция с Kafka

* Producer находится в `src/kafka_producer.py`
* Consumer находится в `src/kafka_consumer.py`
* Все сообщения с результатами работы модели публикуются в топик `model_results`.

## Интеграция с DVC

Для скачивания датасета NYC Yellow Taxi Data из бакета Yandex Cloud:

```bash
dvc pull
```

* Датасет: [NYC Yellow Taxi Trip Data](https://www.kaggle.com/datasets/elemento/nyc-yellow-taxi-trip-data?select=yellow_tripdata_2016-03.csv) (1.91 Gb)

## Автоматическая генерация dev_sec_ops.yml

Для автоматической генерации dev_sec_ops.yml используем скрипт generate_dev_sec_ops.sh для подписи docker образа, хэш последних 5 коммитов в репозитории модели, степень покрытия тестами:

```bash
chmod +x generate_dev_sec_ops.sh
./generate_dev_sec_ops.sh
```

## Тесты

Используется pytest + pytest-cov для покрытия кода:

```bash
python -m pytest --cov=src --cov-report=term
```

Покрытие по модулю:

Name                    Stmts   Miss  Cover
-------------------------------------------
src/api/db.py              25     12    52%
src/api/main.py            27      3    89%
src/kafka_consumer.py      21     21     0%
src/kafka_producer.py       9      0   100%
src/model.py               10      0   100%
src/preprocess.py          39     16    59%
src/train.py               36     17    53%
-------------------------------------------
TOTAL                     167     69    59%