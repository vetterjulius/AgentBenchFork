import argparse
import os
import subprocess
import sys
import time
import yaml
from typing import Dict, List

def load_config(config_path: str):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def main():
    parser = argparse.ArgumentParser(description="Start AgentBench task workers locally.")
    parser.add_argument("--config", "-c", type=str, default="configs/start_task_lite.yaml")
    parser.add_argument("--all", "-a", action="store_true", help="Start all tasks in config.")
    parser.add_argument("--specific", "-s", nargs='+', help="Start specific tasks: task1 count1 task2 count2...")
    parser.add_argument("--controller", "-C", type=str, default="http://localhost:5000/api", help="Controller API URL.")

    args = parser.parse_args()

    if not os.path.exists(args.config):
        print(f"Config file not found: {args.config}")
        sys.exit(1)

    config = load_config(args.config)

    tasks_to_start = {}
    if args.all:
        tasks_to_start = config.get('start', {})
    elif args.specific:
        for i in range(0, len(args.specific), 2):
            task_name = args.specific[i]
            count = int(args.specific[i+1])
            tasks_to_start[task_name] = count

    if not tasks_to_start:
        print("No tasks to start. Use -a or -s.")
        return

    worker_processes = []

    # Determine local IP for the worker to register itself.
    # 'localhost' often doesn't work when the controller is in Docker.
    import socket
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except:
        local_ip = "127.0.0.1"

    # Start Workers
    port = 5021
    for task_name, count in tasks_to_start.items():
        for i in range(count):
            print(f"Starting Worker for {task_name} on port {port} (IP: {local_ip})...")

            # Use the definition import from the config, fallback to default assembly
            definition = config.get('definition', {})
            task_config_path = definition.get('import', 'configs/tasks/task_assembly.yaml')
            if isinstance(task_config_path, list):
                # If it's a list, we might need a better way to find the right file,
                # but usually the first one is the assembly.
                task_config_path = task_config_path[0]

            # Ensure path is relative to repo root if needed
            if not os.path.isabs(task_config_path) and not os.path.exists(task_config_path):
                 # Try prepending configs/ if it's just 'tasks/...'
                 potential_path = os.path.join("configs", task_config_path)
                 if os.path.exists(potential_path):
                     task_config_path = potential_path

            # Register as the host IP so Dockerized controller can reach back
            self_url = f"http://{local_ip}:{port}/api"

            stdout_log = f"worker_{task_name}_{i}_stdout.log"
            stderr_log = f"worker_{task_name}_{i}_stderr.log"
            print(f"  Logging to {stdout_log} and {stderr_log}")

            p = subprocess.Popen(
                [
                    sys.executable, "-m", "agentrl.worker",
                    task_name,
                    "-c", task_config_path,
                    "--self", self_url,
                    "--controller", args.controller,
                    "--port", str(port),
                    "--log-level", "INFO"
                ],
                stdout=open(stdout_log, "w", encoding="utf-8"),
                stderr=open(stderr_log, "w", encoding="utf-8")
            )
            worker_processes.append(p)
            port += 1

    print(f"Started {len(worker_processes)} worker(s). Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
            # Check if any process died
            for p in worker_processes:
                if p.poll() is not None:
                    print(f"A worker process exited with code {p.returncode}")
                    # In a real scenario we might want to restart it or exit
    except KeyboardInterrupt:
        print("Stopping workers...")
    finally:
        for p in worker_processes:
            p.terminate()
        print("Done.")

if __name__ == "__main__":
    main()
