#!/bin/bash

# Configuration
CONFIG="configs/assignments/energy_db.yaml"
LITE_CONFIG="configs/start_task_lite.yaml"

echo "Starting DBBench Task Workers..."
# Start the task worker in the background
python -m src.start_task -a --config $LITE_CONFIG &
WORKER_PID=$!

echo "Waiting for task workers to initialize (approx 1 minute)..."
# Wait for workers to be ready.
# We could poll the port but a simple sleep is often what AgentBench users do.
sleep 60

echo "Starting Assigner for Energy Agent on DBBench..."
python -m src.assigner --config $CONFIG

# Cleanup
echo "Cleaning up task workers..."
kill $WORKER_PID
