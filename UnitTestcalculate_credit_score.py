
import unittest
from unittest.mock import Mock
from your_module import calculate_credit_score  # Replace with the actual name of the module

class TestCalculateCreditScore(unittest.TestCase):
    def setUp(self):
        self.config = Mock(spec=dict, engine=Mock(name='engine'))
        self.engine = self.config.engine
        self.engine.execute = Mock(return_value=[(1, 2, 3), (4, 5, 6), 7])  # Mock result for each query

    def test_calculate_credit_score_valid_customer(self):
        self.config.engine.execute = Mock(return_value=[(100, 200, 50), (4, 5, 6), 7])  # Mock result for each query
        result = calculate_credit_score(1)
        self.assertAlmostEqual(result, 650.0)

    def test_calculate_credit_score_no_loans(self):
        self.config.engine.execute = Mock(return_value=[(0, 0, 0), (4, 5, 6), 7])  # Mock result for each query
        result = calculate_credit_score(1)
        self.assertAlmostEqual(result, 650.0)

    def test_calculate_credit_score_late_payments(self):
        self.config.engine.execute = Mock(return_value=[(100, 200, 50), (4, 5, 6), 3])  # Mock result for each query
        result = calculate_credit_score(1)
        self.assertAlmostEqual(result, 550.0)

    def test_calculate_credit_score_zero_credit_card_balance(self):
        self.config.engine.execute = Mock(return_value=[(100, 200, 50), (0, 0, 0), 7])  # Mock result for each query
        result = calculate_credit_score(1)
        self.assertAlmostEqual(result, 650.0)

    def test_calculate_credit_score_high_credit_card_utilization(self):
        self.config.engine.execute = Mock(return_value=[(100, 200, 50), (4000, 0, 0), 7])  # Mock result for each query
        result = calculate_credit_score(1)
        self.assertAlmostEqual(result, 550.0)

    def test_calculate_credit_score_invalid_customer(self):
        with self.assertRaises(ValueError):
            calculate_credit_score(0)

    def test_calculate_credit_score_database_error(self):
        self.config.engine.execute = Mock(side_effect=Exception('Database error'))
        with self.assertRaises(Exception):
            calculate_credit_score(1)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
