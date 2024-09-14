
import unittest
from your_module import calculate_credit_score  # Replace with the actual module name
import pandas as pd

class TestCalculateCreditScore(unittest.TestCase):
    def test_valid_customer_id(self):
        # Arrange
        customer_id = 123

        # Act
        credit_score = calculate_credit_score(customer_id)

        # Assert
        self.assertIsNotNone(credit_score)
        self.assertIsInstance(credit_score, (int, float))
        self.assertGreaterEqual(credit_score, 300)
        self.assertLessEqual(credit_score, 850)

    def test_invalid_customer_id(self):
        # Arrange
        customer_id = None

        # Act and Assert
        with self.assertRaises(TypeError):
            calculate_credit_score(customer_id)

    def test_no_loans(self):
        # Arrange
        customer_id = 456

        # Act
        credit_score = calculate_credit_score(customer_id)

        # Assert
        self.assertIsNotNone(credit_score)
        self.assertIsInstance(credit_score, (int, float))
        self.assertGreaterEqual(credit_score, 300)
        self.assertLessEqual(credit_score, 850)

    def test_no_credit_card(self):
        # Arrange
        customer_id = 789

        # Act
        credit_score = calculate_credit_score(customer_id)

        # Assert
        self.assertIsNotNone(credit_score)
        self.assertIsInstance(credit_score, (int, float))
        self.assertGreaterEqual(credit_score, 300)
        self.assertLessEqual(credit_score, 850)

    def test_late_payments(self):
        # Arrange
        customer_id = 901

        # Act
        credit_score = calculate_credit_score(customer_id)

        # Assert
        self.assertIsNotNone(credit_score)
        self.assertIsInstance(credit_score, (int, float))
        self.assertGreaterEqual(credit_score, 300)
        self.assertLessEqual(credit_score, 850)

    def test_low_credit_score(self):
        # Arrange
        customer_id = 234

        # Act
        credit_score = calculate_credit_score(customer_id)

        # Assert
        self.assertIsNotNone(credit_score)
        self.assertIsInstance(credit_score, (int, float))
        self.assertLess(credit_score, 500)

    def test_database_error(self):
        # Arrange
        customer_id = 567

        # Act and Assert
        with self.assertRaises(psycopg2.Error):
            calculate_credit_score(customer_id)

if __name__ == '__main__':
    unittest.main()
