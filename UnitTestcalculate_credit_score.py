
import unittest
from unittest.mock import patch
from your_module import update_credit_score  # Replace with the actual name of your module

class TestUpdateCreditScore(unittest.TestCase):
    @patch('your_module.engine')
    @patch('your_module.connection')
    def test_update_credit_score_no_loans(self, mock_connection, mock_engine):
        # Test with no loans for the customer
        p_customer_id = 1
        update_credit_score(p_customer_id)
        self.assertEqual(mock_connection.execute.call_count, 4)
        self.assertEqual(mock_connection.execute.text, 'SELECT COALESCE(ROUND(SUM(loan_amount), 2), 0) FROM loans WHERE loans.customer_id = :customer_id')
        self.assertEqual(mock_connection.execute.text, 'SELECT COALESCE(ROUND(SUM(repayment_amount), 2), 0) FROM loans WHERE loans.customer_id = :customer_id')
        self.assertEqual(mock_connection.execute.text, 'SELECT COALESCE(ROUND(SUM(outstanding_balance), 2), 0) FROM loans WHERE loans.customer_id = :customer_id')
        self.assertEqual(mock_connection.execute.text, 'SELECT COALESCE(ROUND(SUM(balance), 2), 0) FROM credit_cards WHERE credit_cards.customer_id = :customer_id')

    @patch('your_module.engine')
    @patch('your_module.connection')
    def test_update_credit_score_with_loans(self, mock_connection, mock_engine):
        # Test with some loans for the customer
        p_customer_id = 1
        total_loan_amount = 1000
        total_repayment = 800
        outstanding_loan_balance = 200
        credit_card_balance = 0
        late_pay_count = 0
        with mock_connection as conn:
            conn.execute.return_value.fetchall.return_value = [(total_loan_amount,), (total_repayment,), (outstanding_loan_balance,)]
            update_credit_score(p_customer_id)
            self.assertEqual(mock_connection.execute.call_count, 4)
            self.assertEqual(mock_connection.execute.text, 'SELECT COALESCE(ROUND(SUM(loan_amount), 2), 0) FROM loans WHERE loans.customer_id = :customer_id')
            self.assertEqual(mock_connection.execute.text, 'SELECT COALESCE(ROUND(SUM(repayment_amount), 2), 0) FROM loans WHERE loans.customer_id = :customer_id')
            self.assertEqual(mock_connection.execute.text, 'SELECT COALESCE(ROUND(SUM(outstanding_balance), 2), 0) FROM loans WHERE loans.customer_id = :customer_id')
            self.assertEqual(mock_connection.execute.text, 'SELECT COALESCE(ROUND(SUM(balance), 2), 0) FROM credit_cards WHERE credit_cards.customer_id = :customer_id')

    @patch('your_module.engine')
    @patch('your_module.connection')
    def test_update_credit_score_late_pays(self, mock_connection, mock_engine):
        # Test with some late pays for the customer
        p_customer_id = 1
        total_loan_amount = 1000
        total_repayment = 800
        outstanding_loan_balance = 200
        credit_card_balance = 500
        late_pay_count = 2
        with mock_connection as conn:
            conn.execute.return_value.fetchall.return_value = [(total_loan_amount,), (total_repayment,), (outstanding_loan_balance,)]
            conn.execute.return_value.fetchall.return_value = [(credit_card_balance,)]
            conn.execute.return_value.fetchall.return_value = [(late_pay_count,)]
            update_credit_score(p_customer_id)
            self.assertEqual(mock_connection.execute.call_count, 7)
            self.assertEqual(mock_connection.execute.text, 'SELECT COALESCE(ROUND(SUM(loan_amount), 2), 0) FROM loans WHERE loans.customer_id = :customer_id')
            self.assertEqual(mock_connection.execute.text, 'SELECT COALESCE(ROUND(SUM(repayment_amount), 2), 0) FROM loans WHERE loans.customer_id = :customer_id')
            self.assertEqual(mock_connection.execute.text, 'SELECT COALESCE(ROUND(SUM(outstanding_balance), 2), 0) FROM loans WHERE loans.customer_id = :customer_id')
            self.assertEqual(mock_connection.execute.text, 'SELECT COALESCE(ROUND(SUM(balance), 2), 0) FROM credit_cards WHERE credit_cards.customer_id = :customer_id')
            self.assertEqual(mock_connection.execute.text, 'SELECT COUNT(*) FROM payments WHERE payments.customer_id = :customer_id AND status = ''Late''')

    @patch('your_module.engine')
    @patch('your_module.connection')
    def test_update_credit_score_low_score_alert(self, mock_connection, mock_engine):
        # Test with a low score trigger alert
        p_customer_id = 1
        total_loan_amount = 1000
        total_repayment = 800
        outstanding_loan_balance = 200
        credit_card_balance = 500
        late_pay_count = 2
        with mock_connection as conn:
            conn.execute.return_value.fetchall.return_value = [(total_loan_amount,), (total_repayment,), (outstanding_loan_balance,)]
            conn.execute.return_value.fetchall.return_value = [(credit_card_balance,)]
            conn.execute.return_value.fetchall.return_value = [(late_pay_count,)]
            update_credit_score(p_customer_id)
            self.assertEqual(mock_connection.execute.call_count, 7)
            self.assertEqual(mock_connection.execute.text, 'SELECT COALESCE(ROUND(SUM(loan_amount), 2), 0) FROM loans WHERE loans.customer_id = :customer_id')
            self.assertEqual(mock_connection.execute.text, 'SELECT COALESCE(ROUND(SUM(repayment_amount), 2), 0) FROM loans WHERE loans.customer_id = :customer_id')
            self.assertEqual(mock_connection.execute.text, 'SELECT COALESCE(ROUND(SUM(outstanding_balance), 2), 0) FROM loans WHERE loans.customer_id = :customer_id')
            self.assertEqual(mock_connection.execute.text, 'SELECT COALESCE(ROUND(SUM(balance), 2), 0) FROM credit_cards WHERE credit_cards.customer_id = :customer_id')
            self.assertEqual(mock_connection.execute.text, 'SELECT COUNT(*) FROM payments WHERE payments.customer_id = :customer_id AND status = ''Late''')
            self.assertEqual(mock_connection.execute.text, 'UPDATE customers SET credit_score = ROUND(:v_credit_score, 0) WHERE customers.id = :customer_id')
            self.assertEqual(mock_connection.execute.text, 'INSERT INTO credit_score_alerts (customer_id, credit_score, created_at) VALUES (:customer_id, ROUND(:v_credit_score, 0), NOW())')

if __name__ == '__main__':
    unittest.main()
