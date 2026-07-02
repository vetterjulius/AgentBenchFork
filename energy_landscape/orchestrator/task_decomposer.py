from __future__ import annotations

from typing import List

import torch

from energy_landscape.benchmark.agentbench.adapter import BenchmarkTask
from energy_landscape.orchestrator.base import Task


class TaskDecomposer:
    """Decompose a benchmark instruction into a small task graph."""

    def __init__(self, d: int = 8):
        self.d = d

    def decompose(self, task: BenchmarkTask) -> List[Task]:
        # Handle cases where task is just a string (as in EnergySingleAgent.invoke)
        if isinstance(task, str):
            instruction = task.lower()
            task_id = "task-input"
        else:
            instruction = task.instruction.lower()
            task_id = task.id

        template = [
            "schema analysis",
            "entity identification",
            "query planning",
            "sql generation",
            "verification",
        ]
        if "sql" in instruction:
            template = [
                "schema analysis",
                "query planning",
                "sql generation",
                "verification",
            ]

        embeddings = []
        for label in template:
            emb = torch.zeros(self.d, dtype=torch.float32)
            for idx, char in enumerate(label):
                emb[idx % self.d] += (ord(char) % 7) / 10.0
            embeddings.append(emb)

        return [
            Task(
                id=f"{task_id}:{idx}",
                embedding=embedding,
                dependencies=[] if idx == 0 else [f"{task_id}:{idx - 1}"],
                estimated_cost=1.0 + 0.2 * idx,
                estimated_risk=0.05 * (idx + 1),
            )
            for idx, embedding in enumerate(embeddings)
        ]
