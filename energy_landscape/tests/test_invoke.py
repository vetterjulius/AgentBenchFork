import torch
import os
import sys

sys.path.insert(0, os.getcwd())

from energy_landscape.adapters.single_agent import EnergySingleAgent

def test_energy_single_agent_invoke():
    # Use dimension 32 to match default config.yaml
    agents = [
        {"id": "planner", "role": "Planner", "capability_embedding": torch.randn(32), "memory_state": {}},
        {"id": "sql", "role": "SQL Expert", "capability_embedding": torch.randn(32), "memory_state": {}},
        {"id": "verifier", "role": "Verifier", "capability_embedding": torch.randn(32), "memory_state": {}}
    ]
    agent = EnergySingleAgent(agents)
    result = agent.invoke("Generate a SQL query to list all users.")

    assert isinstance(result, str)
    assert "SELECT" in result
