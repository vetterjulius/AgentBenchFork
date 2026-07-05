# Guide: Running Energy Agent System in AgentBench (DB/SQL)

This guide explains how to run the Energy Agent System for the DB/SQL benchmark in AgentBench.

---

## 🚀 Version 1: The "Hybrid" Local Run (Recommended for Windows)

This mode runs the **Energy Agent** and **DB Benchmark** as local Python processes (using SQLite), while using a single Docker container for the essential AgentBench Controller.

1. **Prerequisites**:
   - Install Docker (for the Controller).
   - Python 3.9+.
   - Install requirements: `pip install -r requirements.txt`.
2. **Open PowerShell**: Navigate to the `AgentBench` folder.
3. **Run the Hybrid Script**:
   ```powershell
   .\scripts\run_energy_dbbench_local.ps1
   ```
4. **What happens?**:
   - It starts a minimal Docker environment (`controller`, `redis`).
   - It starts local task workers using `src/start_task.py`.
   - It starts the assigner to run the tasks.
5. **Check Results**: Your results will be in the `outputs/energy_db_local/` folder.

---

## 🐋 Version 2: The "Full Docker" Run (MySQL)

Use this if you want to test with a real MySQL environment.

1. **Install Docker**: Make sure Docker is running.
2. **Pull MySQL Image**: `docker pull mysql:8`.
3. **Run the Script**:
   - **Windows**: `.\scripts\run_energy_dbbench.ps1`
   - **Linux/Mac**: `bash scripts/run_energy_dbbench.sh`
4. **Check Results**: Your results will be in the `outputs/energy_db/` folder.

---

## 📋 Version 3: The "I want to know what I'm doing" Guide

### 1. Prerequisites
- **Python 3.9**: Recommended for AgentBench.
- **Dependencies**: Install them if you haven't:
  ```bash
  pip install -r requirements.txt
  ```
- **Docker**: Required for the Controller.

### 2. Running the Benchmark Manually (Hybrid Mode)
1. **Start Infrastructure**:
   ```bash
   docker compose -f extra/docker-compose-lite.yml up -d
   ```
2. **Start Task Workers**: These manage the actual database environment locally.
   ```bash
   python -m src.start_task -a --config configs/start_task_lite.yaml
   ```
3. **Start the Assigner**: This tells the Energy Agent to solve the tasks.
   ```bash
   python -m src.assigner --config configs/assignments/energy_db_local.yaml
   ```

---

## ⚙️ Technical Details & Troubleshooting

### How it works
- **Energy Agent**: Located in `energy_landscape/`. It uses an energy-based landscape and simulated annealing to orchestrate tasks between sub-agents (Planner, SQL Expert, Verifier).
- **SQLite Adapter**: We modified AgentBench's DB task to support a `force_sqlite` mode, allowing it to run without a MySQL container.
- **Config**:
    - `configs/assignments/energy_db_local.yaml` is the entry point for local SQLite runs.

### Troubleshooting

#### Port 5000 is blocked
If you see an error about port 5000:
- **Mac Users**: Go to System Settings > General > AirPlay & Handoff and turn off "AirPlay Receiver".
- **Others**: Run `kill $(lsof -t -i :5000)` to free the port.

#### Docker Errors
If the controller fails to start:
- Check if Docker is running (`docker ps`).

#### Missing Dependencies
If you get `ModuleNotFoundError`:
- Ensure you are in the correct Virtualenv.
- Run `pip install -r requirements.txt`.
