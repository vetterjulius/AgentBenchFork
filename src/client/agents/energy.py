import os
import sys

from src.client.agent import AgentClient

# Ensure external energy_landscape package can be imported even if it's outside this repository.
here = os.path.abspath(os.path.dirname(__file__))
# Check local first
if os.path.isdir(os.path.join(os.getcwd(), "energy_landscape")):
    if os.getcwd() not in sys.path:
        sys.path.insert(0, os.getcwd())

from energy_landscape.adapters.agentbench import infer


class EnergyOrchestratorClient(AgentClient):

    def inference(self, history):
        return infer(history)
