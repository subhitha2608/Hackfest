
import unittest
from unittest.mock import patch, MagicMock
from your_module import calculate_credit_score  # Replace with the actual module name
import sqlalchemy as sa
import pandas as pd
import psycopg2

class TestCalculateCreditScore(unittest.TestCase):
    @patch('your_module.engine')
    def test_calculate_credit_score_success(self, mock_engine):
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn

        customer_id = 123
        total_loan_amount = 1000.0
        total_repayment = 800.0
        outstanding_loan_balance = 200.0
        credit_card_balance = 500.0
        late_pay_count = 2

        mock_conn.execute.side_effect = [
            [(total_loan_amount, total_repayment, outstanding_loan_balance)],
            [(credit_card_balance,)],
            [(late_pay_count,)],
        ]

        result = calculate_credit_score(customer_id)
        self.assertEqual(result, 620)  # Expected credit score based on the inputs

        mock_conn.execute.assert_any_call(
            sa.text("""
                UPDATE customers
                SET credit_score = :credit_score
                WHERE customers.id = :customer_id
            """),
            {'credit_score': 620, 'customer_id': customer_id},
        )

        mock_conn.commit.assert_called()

    @patch('your_module.engine')
    def test_calculate_credit_score_zero_loan_amount(self, mock_engine):
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn

        customer_id = 123
        total_loan_amount = 0.0
        total_repayment = 0.0
        outstanding_loan_balance = 0.0
        credit_card_balance = 500.0
        late_pay_count = 2

        mock_conn.execute.side_effect = [
            [(total_loan_amount, total_repayment, outstanding_loan_balance)],
            [(credit_card_balance,)],
            [(late_pay_count,)],
        ]

        result = calculate_credit_score(customer_id)
        self.assertEqual(result, 650)  # Expected credit score based on the inputs

    @patch('your_module.engine')
    def test_calculate_credit_score_zero_credit_card_balance(self, mock_engine):
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn

        customer_id = 123
        total_loan_amount = 1000.0
        total_repayment = 800.0
        outstanding_loan_balance = 200.0
        credit_card_balance = 0.0
        late_pay_count = 2

        mock_conn.execute.side_effect = [
            [(total_loan_amount, total_repayment, outstanding_loan_balance)],
            [(credit_card_balance,)],
            [(late_pay_count,)],
        ]

        result = calculate_credit_score(customer_id)
        self.assertEqual(result, 700)  # Expected credit score based on the inputs

    @patch('your_module.engine')
    def test_calculate_credit_score_zero_late.Payments(self, mock_engine):
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn

        customer_id = 123
        total_loan_amount = 1000.0
        total_repayment = 800.0
        outstanding_loan_balance = 200.0
        credit_card_balance = 500.0
        late_pay_count = 0

        mock_conn.execute.side_effect = [
            [(total_loan_amount, total_repayment, outstanding_loan_balance)],
            [(credit_card_balance,)],
            [(late_pay_count,)],
        ]

        result = calculate_credit_score(customer_id)
        self.assertEqual(result, 750)  # Expected credit score based on the inputs

    @patch('your_module.engine')
    def test_calculate_credit_score_db_error(self, mock_engine):
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn
        mock_conn.execute.side_effect = psycopg2.Error("Database error!")

        customer_id = 123

        with self.assertRaises(psycopg2.Error):
            calculate_credit_score(customer_id)

    @patch('your_module.engine')
    def test_calculate_credit_score_customer_id_none(self, mock_engine):
        customer_id = None

        with self.assertRaises(TypeError):
            calculate_credit_score(customer_id)

    @patch('your_module.engine')
    def test_calculate_credit_score_customer_id_non_positive(self, mock_engine):
        customer_id = -1

        with self.assertRaises(ValueError):
            calculate_credit_score(customer_id)

if __name__ == "__main__":
    unittest.main()
