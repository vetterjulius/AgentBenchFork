import unittest

from src.configs import ConfigLoader
from src.typings.config import AssignmentConfig


class EnergyAssignmentConfigTest(unittest.TestCase):
    def test_energy_db_assignment_defines_energy_orchestrator(self):
        config = ConfigLoader().load_from("configs/assignments/energy_db.yaml")

        self.assertIn("energy-orchestrator", config["definition"]["agent"])

        value = AssignmentConfig.model_validate(config)
        AssignmentConfig.post_validate(value)


if __name__ == "__main__":
    unittest.main()
