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
