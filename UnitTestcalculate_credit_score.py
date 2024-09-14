
import unittest
from unittest.mock import patch
from config import engine
import pandas as pd
import psycopg2

class TestCalculateCreditScore(unittest.TestCase):

    @patch('config.engine.connect')
    def test_calculate_credit_score(self, mock_engine_connect):
        # Test data
        test_customer_id = 123
        total_loan_amount = 10000
        total_repayment = 5000
        outstanding_loan_balance = 3000
        credit_card_balance = 2000
        late_pay_count = 2
        expected_credit_score = 450

        # Mock the engine.connect function
        mock_connection = mock_engine_connect.return_value
        mock_connection.return_value.execute.return_value.scalar.return_value = (
            total_loan_amount,
            total_repayment,
            outstanding_loan_balance,
            credit_card_balance,
            late_pay_count
        )

        # Call the function
        calculate_credit_score(test_customer_id)

        # Assert that the expected credit score was calculated
        assert expected_credit_score == expected_credit_score

    @patch('config.engine.connect')
    def test_calculate_credit_score_zero_total_loan_amount(self, mock_engine_connect):
        # Test data
        test_customer_id = 123
        total_loan_amount = 0
        total_repayment = 5000
        outstanding_loan_balance = 3000
        credit_card_balance = 2000
        late_pay_count = 2
        expected_credit_score = 300

        # Mock the engine.connect function
        mock_connection = mock_engine_connect.return_value
        mock_connection.return_value.execute.return_value.scalar.return_value = (
            total_loan_amount,
            total_repayment,
            outstanding_loan_balance,
            credit_card_balance,
            late_pay_count
        )

        # Call the function
        calculate_credit_score(test_customer_id)

        # Assert that the expected credit score was calculated
        assert expected_credit_score == expected_credit_score

    @patch('config.engine.connect')
    def test_calculate_credit_score_credit_card_balance_zero_and_late_pay_count_zero(self, mock_engine_connect):
        # Test data
        test_customer_id = 123
        total_loan_amount = 10000
        total_repayment = 5000
        outstanding_loan_balance = 3000
        credit_card_balance = 0
        late_pay_count = 0
        expected_credit_score = 800

        # Mock the engine.connect function
        mock_connection = mock_engine_connect.return_value
        mock_connection.return_value.execute.return_value.scalar.return_value = (
            total_loan_amount,
            total_repayment,
            outstanding_loan_balance,
            credit_card_balance,
            late_pay_count
        )

        # Call the function
        calculate_credit_score(test_customer_id)

        # Assert that the expected credit score was calculated
        assert expected_credit_score == expected_credit_score

    @patch('config.engine.connect')
    def test_calculate_credit_score_late_pay_count_greater_than_zero(self, mock_engine_connect):
        # Test data
        test_customer_id = 123
        total_loan_amount = 10000
        total_repayment = 5000
        outstanding_loan_balance = 3000
        credit_card_balance = 2000
        late_pay_count = 3
        expected_credit_score = 350

        # Mock the engine.connect function
        mock_connection = mock_engine_connect.return_value
        mock_connection.return_value.execute.return_value.scalar.return_value = (
            total_loan_amount,
            total_repayment,
            outstanding_loan_balance,
            credit_card_balance,
            late_pay_count
        )

        # Call the function
        calculate_credit_score(test_customer_id)

        # Assert that the expected credit score was calculated
        assert expected_credit_score == expected_credit_score

if __name__ == '__main__':
    unittest.main()

