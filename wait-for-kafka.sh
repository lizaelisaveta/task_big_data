#!/bin/sh
while ! nc -z kafka 9092; do
  echo "Waiting for Kafka..."
  sleep 2
done
exec "$@"
