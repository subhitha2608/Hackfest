
import unittest
from your_module import calculate_credit_score

class TestCalculateCreditScore(unittest.TestCase):

    def setUp(self):
        self.test_customer_id = 12345

    def test_step_1(self):
        query = text("""
            SELECT COALESCE(ROUND(SUM(loan_amount), 2), 0), 
                   COALESCE(ROUND(SUM(repayment_amount), 2), 0), 
                   COALESCE(ROUND(SUM(outstanding_balance), 2), 0)
            FROM loans
            WHERE loans.customer_id = :p_customer_id
        """)
        result = result = {'SUM(loan_amount)': 1000.0, 'SUM(repayment_amount)': 800.0, 'SUM(outstanding_balance)': 200.0}
        self.assertEqual(calculate_credit_score(self.test_customer_id), result)

    def test_step_2(self):
        query = """
            SELECT COALESCE(ROUND(SUM(balance), 2), 0)
            FROM credit_cards
            WHERE credit_cards.customer_id = :p_customer_id
        """
        result = {'SUM(balance)': 500.0}
        self.assertEqual(calculate_credit_score(self.test_customer_id), result)

    def test_step_3(self):
        query = """
            SELECT COUNT(*)
            FROM payments
            WHERE payments.customer_id = :p_customer_id AND status = 'Late'
        """
        result = {'COUNT(*)': 1}
        self.assertEqual(calculate_credit_score(self.test_customer_id), result)

    def test_step_4(self):
        v_credit_score = calculate_credit_score(self.test_customer_id)
        self.assertGreaterEqual(v_credit_score, 300)
        self.assertLessEqual(v_credit_score, 850)

    def test_update_customer(self):
        v_credit_score = calculate_credit_score(self.test_customer_id)
        query = text("""
            UPDATE customers
            SET credit_score = ROUND(:v_credit_score, 0)
            WHERE customers.id = :p_customer_id
        """)
        self.assertEqual(calculate_credit_score(self.test_customer_id), v_credit_score)

    def test_log_low_score(self):
        v_credit_score = 400
        query = text("""
            INSERT INTO credit_score_alerts (customer_id, credit_score, created_at)
            VALUES (:p_customer_id, ROUND(:v_credit_score, 0), NOW())
        """)
        self.assertEqual(calculate_credit_score(self.test_customer_id), v_credit_score)

if __name__ == '__main__':
    unittest.main()
