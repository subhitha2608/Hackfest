
import unittest
from unittest.mock import patch
from your_module import calculate_credit_score  # Replace with the actual module name

class TestCalculateCreditScore(unittest.TestCase):
    def setUp(self):
        self.engine = engine  # assuming engine is a valid SQLAlchemy engine
        self.connection = self.engine.connect()

    def tearDown(self):
        self.connection.close()

    @patch('your_module.engine.connect')
    def test_calculate_credit_score_positive(self, mock_connect):
        # Mock the database queries to return expected results
        mock_connect.return_value.execute.return_value.fetchone.side_effect = [
            (1000.0, 800.0, 200.0),  # loan amounts
            (500.0,),  # credit card balance
            (0,),  # late payments
        ]

        customer_id = 1
        result = calculate_credit_score(customer_id)
        self.assertAlmostEqual(result, 740, places=0)  # expected credit score

    @patch('your_module.engine.connect')
    def test_calculate_credit_score_no_loans(self, mock_connect):
        # Mock the database queries to return expected results
        mock_connect.return_value.execute.return_value.fetchone.side_effect = [
            (0.0, 0.0, 0.0),  # no loans
            (500.0,),  # credit card balance
            (0,),  # late payments
        ]

        customer_id = 1
        result = calculate_credit_score(customer_id)
        self.assertAlmostEqual(result, 650, places=0)  # expected credit score

    @patch('your_module.engine.connect')
    def test_calculate_credit_score_no_credit_card(self, mock_connect):
        # Mock the database queries to return expected results
        mock_connect.return_value.execute.return_value.fetchone.side_effect = [
            (1000.0, 800.0, 200.0),  # loan amounts
            (0.0,),  # no credit card balance
            (0,),  # late payments
        ]

        customer_id = 1
        result = calculate_credit_score(customer_id)
        self.assertAlmostEqual(result, 740, places=0)  # expected credit score

    @patch('your_module.engine.connect')
    def test_calculate_credit_score_late_payments(self, mock_connect):
        # Mock the database queries to return expected results
        mock_connect.return_value.execute.return_value.fetchone.side_effect = [
            (1000.0, 800.0, 200.0),  # loan amounts
            (500.0,),  # credit card balance
            (2,),  # 2 late payments
        ]

        customer_id = 1
        result = calculate_credit_score(customer_id)
        self.assertAlmostEqual(result, 640, places=0)  # expected credit score

    @patch('your_module.engine.connect')
    def test_calculate_credit_score_invalid_customer_id(self, mock_connect):
        # Mock the database queries to return None
        mock_connect.return_value.execute.return_value.fetchone.return_value = None

        customer_id = 123456  # invalid customer ID
        with self.assertRaises(RuntimeError):
            calculate_credit_score(customer_id)

    @patch('your_module.engine.connect')
    def test_calculate_credit_score_connection_error(self, mock_connect):
        # Mock the database connection to raise an error
        mock_connect.return_value.execute.side_effect = psycopg2.Error("Mock connection error")

        customer_id = 1
        with self.assertRaises(psycopg2.Error):
            calculate_credit_score(customer_id)

if __name__ == '__main__':
    unittest.main()
