FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY model/ model/    
COPY ansible/secrets.yml ansible/secrets.yml

ARG VAULT_PASS
RUN if [ -n "$VAULT_PASS" ]; then echo "$VAULT_PASS" > /tmp/.vault_pass && \
    apt-get update && apt-get install -y ansible && \
    ansible-vault view ansible/secrets.yml --vault-password-file /tmp/.vault_pass > /tmp/secrets && \
    rm -f /tmp/.vault_pass; fi

ENV MODEL_PATH=/app/model/rf_2016-03.joblib
ENV KAFKA_BOOTSTRAP=kafka:9092

EXPOSE 8000

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
