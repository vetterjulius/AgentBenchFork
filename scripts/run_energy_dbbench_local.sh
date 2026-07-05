#!/bin/bash

# Configuration
CONFIG="configs/assignments/energy_db_local.yaml"
LITE_CONFIG="configs/start_task_lite.yaml"
DOCKER_LITE="extra/docker-compose-lite.yml"

echo "Starting minimal Docker infrastructure (Controller & Redis)..."
docker compose -f $DOCKER_LITE up -d

echo "Waiting for infrastructure to be ready..."
sleep 5

echo "Starting DBBench Task Workers locally..."
# Start the task worker in the background
python -m src.start_task -a --config $LITE_CONFIG &
WORKER_PID=$!

echo "Waiting for task workers to initialize..."
sleep 10

echo "Starting Assigner for Energy Agent on DBBench (LOCAL)..."
python -m src.assigner --config $CONFIG

# Cleanup
echo "Cleaning up..."
kill $WORKER_PID
docker compose -f $DOCKER_LITE down
