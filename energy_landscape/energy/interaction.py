import torch
from energy_landscape.energy.base import EnergyTerm

class InteractionEnergy(EnergyTerm):
    def compute(self, state):
        co = state.X.T @ state.X
        return -(state.Theta * co).sum() / (state.N * state.M)
