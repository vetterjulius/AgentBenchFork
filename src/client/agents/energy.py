import os
import sys

from src.client.agent import AgentClient

# Ensure external energy_landscape package can be imported even if it's outside this repository.
here = os.path.abspath(os.path.dirname(__file__))
candidates = [os.getcwd()]
candidates += [os.path.abspath(os.path.join(os.getcwd(), *(['..'] * i))) for i in range(1, 6)]
for path in candidates:
    if os.path.isdir(os.path.join(path, "energy_landscape")):
        if path not in sys.path:
            sys.path.insert(0, path)
        break

from energy_landscape.adapters.agentbench import infer


class EnergyOrchestratorClient(AgentClient):

    def inference(self, history):
        return infer(history)
