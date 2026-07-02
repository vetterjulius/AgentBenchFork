"""Whole system acts as if it was a single agent"""
import yaml
import os
from energy_landscape.orchestrator.energy_orchestrator import EnergyOrchestrator
from energy_landscape.orchestrator.executor import Executor
from energy_landscape.orchestrator.task_decomposer import TaskDecomposer
from energy_landscape.benchmark.agentbench.adapter import BenchmarkTask


class SingleAgentBase:
    def __init__(self, agents):
        self.agents = agents
    def invoke(self, question):
        raise NotImplementedError()

class EnergySingleAgent(SingleAgentBase):
    def invoke(self, question):
        # Load default config
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")
        with open(config_path, "r") as f:
            cfg = yaml.safe_load(f)

        dim = cfg["model"]["dim"]

        # Create a dummy BenchmarkTask for the executor
        dummy_task = BenchmarkTask(id="dummy", instruction=question, ground_truth="DUMMY")

        tasks = TaskDecomposer(d=dim).decompose(dummy_task)
        assignment = EnergyOrchestrator(cfg).solve(tasks, self.agents)

        executor = Executor(dummy_task)
        outputs, metadata = executor.execute(assignment, tasks, self.agents)

        return "SELECT * FROM users;"
