# Guide: Running Energy Agent System in AgentBench (DB/SQL)

This guide explains how to run the Energy Agent System for the DB/SQL benchmark in AgentBench.

---

## 🚀 Version 1: The "I just want it to work" Quick Start (For Idiots)

1. **Install Docker**: Make sure Docker is installed and running on your computer.
2. **Open a Terminal**: Navigate to the `AgentBench` folder.
3. **Pull Database Image**:
   ```bash
   docker pull mysql:8
   ```
4. **Run the Magic Script**:
   ```bash
   bash scripts/run_energy_dbbench.sh
   ```
5. **Wait**: It will take about a minute to start the servers, and then it will start running the tasks.
6. **Check Results**: Your results will be in the `outputs/energy_db/` folder.

---

## 📋 Version 2: The "I want to know what I'm doing" Guide

### 1. Prerequisites
- **Python 3.9**: Recommended for AgentBench.
- **Dependencies**: Install them if you haven't:
  ```bash
  pip install -r requirements.txt
  pip install torch>=2.0.0 pyyaml>=6.0
  ```
- **Docker**: Required for the MySQL environment.

### 2. Preparation
The DB benchmark needs a MySQL container. AgentBench handles the connection, but the image must exist:
```bash
docker pull mysql:8
```

### 3. Running the Benchmark
We use a two-step process:
1. **Start Task Workers**: These manage the actual database environment.
   ```bash
   python -m src.start_task -a --config configs/start_task_lite.yaml
   ```
   *(Wait until you see "200 OK" messages, usually takes ~1 min)*
2. **Start the Assigner**: This tells the Energy Agent to solve the tasks.
   ```bash
   python -m src.assigner --config configs/assignments/energy_db.yaml
   ```

---

## ⚙️ Version 3: Technical Details & Troubleshooting

### How it works
- **Energy Agent**: Located in `energy_landscape/`. It uses an energy-based landscape and simulated annealing to orchestrate tasks between sub-agents (Planner, SQL Expert, Verifier).
- **AgentBench Adapter**: `src/client/agents/energy.py` connects AgentBench's request-response cycle to the Energy Agent's `infer()` function.
- **Config**:
    - `configs/agents/energy.yaml` defines the agent for AgentBench.
    - `configs/assignments/energy_db.yaml` defines the run (1 concurrent worker, DB task only).

### Troubleshooting

#### Port 5000 is blocked
If you see an error about port 5000:
- **Mac Users**: Go to System Settings > General > AirPlay & Handoff and turn off "AirPlay Receiver".
- **Others**: Run `kill $(lsof -t -i :5000)` to free the port.

#### Docker Errors
If the task workers fail to start:
- Check if Docker is running (`docker ps`).
- Ensure you have enough disk space for the MySQL image.

#### Missing Dependencies
If you get `ModuleNotFoundError`:
- Ensure you are in the correct Conda/Virtualenv.
- Ensure `torch` and `pyyaml` are installed.

### File Structure for Energy Agent
- `energy_landscape/`: The core logic of your multi-agent system.
- `configs/assignments/energy_db.yaml`: The specific benchmark setup.
- `scripts/run_energy_dbbench.sh`: Automation for local runs.

---

## 🚧 Blockers & Limitations
- **Concurrency**: Currently set to 1 for stability in local runs. Increasing this in `configs/assignments/energy_db.yaml` might require more RAM/CPU.
- **Memory**: The system requires enough RAM to run both the Python orchestrator and the Dockerized MySQL. 8GB+ is recommended.
