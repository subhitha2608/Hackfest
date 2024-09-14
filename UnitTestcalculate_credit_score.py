
import unittest
from unittest.mock import patch, Mock
from your_module import calculate_credit_score

class TestCalculateCreditScore(unittest.TestCase):

    @patch('your_module.engine.execute')
    def test_calculate_credit_score(self, mock_execute):
        result1 = [(100.0, 50.0, 20.0), ]
        result2 = [(10.0, )]
        result3 = [(1, )]
        
        mock_execute.side_effect = [result1, result2, result3]

        p_customer_id = 1
        calculate_credit_score(p_customer_id)

        mock_execute.assert_any_call(text("""
            SELECT COALESCE(ROUND(SUM(loan_amount), 2), 0), 
                   COALESCE(ROUND(SUM(repayment_amount), 2), 0), 
                   COALESCE(ROUND(SUM(outstanding_balance), 2), 0)
            FROM loans
            WHERE loans.customer_id = :p_customer_id
        """), p_customer_id=p_customer_id, return_scalar=True)
        mock_execute.assert_any_call(text("""
            SELECT COALESCE(ROUND(SUM(balance), 2), 0)
            FROM credit_cards
            WHERE credit_cards.customer_id = :p_customer_id
        """), p_customer_id=p_customer_id, return_scalar=True)
        mock_execute.assert_any_call(text("""
            SELECT COUNT(*)
            FROM payments
            WHERE payments.customer_id = :p_customer_id AND status = 'Late'
        """), p_customer_id=p_customer_id, return_scalar=True)
        mock_execute.assert_any_call(text("""
            UPDATE customers
            SET credit_score = ROUND(:v_credit_score, 0)
            WHERE customers.id = :p_customer_id
        """), p_customer_id=p_customer_id, v_credit_score=0, return_scalar=True)
        mock_execute.assert_any_call(text("""
            INSERT INTO credit_score_alerts (customer_id, credit_score, created_at)
            VALUES (:p_customer_id, ROUND(:v_credit_score, 0), NOW())
        """), p_customer_id=p_customer_id, v_credit_score=0, return_scalar=True)

    @patch('your_module.engine.execute')
    def test_calculate_credit_score_second_call(self, mock_execute):
        result1 = [(200.0, 100.0, 30.0), ]
        result2 = [(20.0, )]
        result3 = [(2, )]
        
        mock_execute.side_effect = [result1, result2, result3]

        p_customer_id = 2
        calculate_credit_score(p_customer_id)

        mock_execute.assert_any_call(text("""
            SELECT COALESCE(ROUND(SUM(loan_amount), 2), 0), 
                   COALESCE(ROUND(SUM(repayment_amount), 2), 0), 
                   COALESCE(ROUND(SUM(outstanding_balance), 2), 0)
            FROM loans
            WHERE loans.customer_id = :p_customer_id
        """), p_customer_id=p_customer_id, return_scalar=True)
        mock_execute.assert_any_call(text("""
            SELECT COALESCE(ROUND(SUM(balance), 2), 0)
            FROM credit_cards
            WHERE credit_cards.customer_id = :p_customer_id
        """), p_customer_id=p_customer_id, return_scalar=True)
        mock_execute.assert_any_call(text("""
            SELECT COUNT(*)
            FROM payments
            WHERE payments.customer_id = :p_customer_id AND status = 'Late'
        """), p_customer_id=p_customer_id, return_scalar=True)
        mock_execute.assert_any_call(text("""
            UPDATE customers
            SET credit_score = ROUND(:v_credit_score, 0)
            WHERE customers.id = :p_customer_id
        """), p_customer_id=p_customer_id, v_credit_score=0, return_scalar=True)
        mock_execute.assert_any_call(text("""
            INSERT INTO credit_score_alerts (customer_id, credit_score, created_at)
            VALUES (:p_customer_id, ROUND(:v_credit_score, 0), NOW())
        """), p_customer_id=p_customer_id, v_credit_score=0, return_scalar=True)

    @patch('your_module.engine.execute')
    def test_calculate_credit_score_no_loan(self, mock_execute):
        result1 = [(0.0, 0.0, 0.0), ]
        result2 = [(0.0, )]
        result3 = [(0, )]
        
        mock_execute.side_effect = [result1, result2, result3]

        p_customer_id = 1
        calculate_credit_score(p_customer_id)

        mock_execute.assert_any_call(text("""
            SELECT COALESCE(ROUND(SUM(loan_amount), 2), 0), 
                   COALESCE(ROUND(SUM(repayment_amount), 2), 0), 
                   COALESCE(ROUND(SUM(outstanding_balance), 2), 0)
            FROM loans
            WHERE loans.customer_id = :p_customer_id
        """), p_customer_id=p_customer_id, return_scalar=True)
        mock_execute.assert_any_call(text("""
            SELECT COALESCE(ROUND(SUM(balance), 2), 0)
            FROM credit_cards
            WHERE credit_cards.customer_id = :p_customer_id
        """), p_customer_id=p_customer_id, return_scalar=True)
        mock_execute.assert_any_call(text("""
            SELECT COUNT(*)
            FROM payments
            WHERE payments.customer_id = :p_customer_id AND status = 'Late'
        """), p_customer_id=p_customer_id, return_scalar=True)
        mock_execute.assert_any_call(text("""
            UPDATE customers
            SET credit_score = ROUND(:v_credit_score, 0)
            WHERE customers.id = :p_customer_id
        """), p_customer_id=p_customer_id, v_credit_score=400, return_scalar=True)
        mock_execute.assert_any_call(text("""
            INSERT INTO credit_score_alerts (customer_id, credit_score, created_at)
            VALUES (:p_customer_id, ROUND(:v_credit_score, 0), NOW())
        """), p_customer_id=p_customer_id, v_credit_score=400, return_scalar=True)

    @patch('your_module.engine.execute')
    def test_calculate_credit_score_negative_value(self, mock_execute):
        result1 = [(-100.0, 50.0, 20.0), ]
        result2 = [(10.0, )]
        result3 = [(1, )]
        
        mock_execute.side_effect = [result1, result2, result3]

        p_customer_id = 1
        calculate_credit_score(p_customer_id)

        mock_execute.assert_any_call(text("""
            SELECT COALESCE(ROUND(SUM(loan_amount), 2), 0), 
                   COALESCE(ROUND(SUM(repayment_amount), 2), 0), 
                   COALESCE(ROUND(SUM(outstanding_balance), 2), 0)
            FROM loans
            WHERE loans.customer_id = :p_customer_id
        """), p_customer_id=p_customer_id, return_scalar=True)
        mock_execute.assert_any_call(text("""
            SELECT COALESCE(ROUND(SUM(balance), 2), 0)
            FROM credit_cards
            WHERE credit_cards.customer_id = :p_customer_id
        """), p_customer_id=p_customer_id, return_scalar=True)
        mock_execute.assert_any_call(text("""
            SELECT COUNT(*)
            FROM payments
            WHERE payments.customer_id = :p_customer_id AND status = 'Late'
        """), p_customer_id=p_customer_id, return_scalar=True)
        mock_execute.assert_any_call(text("""
            UPDATE customers
            SET credit_score = ROUND(:v_credit_score, 0)
            WHERE customers.id = :p_customer_id
        """), p_customer_id=p_customer_id, v_credit_score=0, return_scalar=True)
        mock_execute.assert_any_call(text("""
            INSERT INTO credit_score_alerts (customer_id, credit_score, created_at)
            VALUES (:p_customer_id, ROUND(:v_credit_score, 0), NOW())
        """), p_customer_id=p_customer_id, v_credit_score=0, return_scalar=True)

if __name__ == "__main__":
    unittest.main()
