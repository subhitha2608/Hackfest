
import unittest
from unittest.mock import patch, Mock
from your_module import calculate_credit_score

class TestCalculateCreditScore(unittest.TestCase):

    @patch('your_module.engine')
    def test_calculate_credit_score(self, mock_engine):
        mock_connection = mock_engine.connect.return_value
        mock_connection.execute.return_value.fetchone.side_effect = [
            (1000, 500, 300), 
            (200,), 
            (2,), 
        ]
        
        self.assertEqual(calculate_credit_score(1), 740)
        
        mock_connection.execute.assert_any_call(text("""
            UPDATE customers
            SET credit_score = ?
            WHERE customers.id = ?
        """), {'credit_score': 740, 'customer_id': 1})
        
        mock_connection.execute.assert_any_call(text("""
            INSERT INTO credit_score_alerts (customer_id, credit_score, created_at)
            VALUES (?, ?, NOW())
        """), {'customer_id': 1, 'credit_score': 740})
        
    @patch('your_module.engine')
    def test_calculate_credit_score_no_loans(self, mock_engine):
        mock_connection = mock_engine.connect.return_value
        mock_connection.execute.return_value.fetchone.side_effect = [
            (0, 0, 0), 
            (200,), 
            (2,), 
        ]
        
        self.assertEqual(calculate_credit_score(1), 600)
        
        mock_connection.execute.assert_any_call(text("""
            UPDATE customers
            SET credit_score = ?
            WHERE customers.id = ?
        """), {'credit_score': 600, 'customer_id': 1})
        
        mock_connection.execute.assert_any_call(text("""
            INSERT INTO credit_score_alerts (customer_id, credit_score, created_at)
            VALUES (?, ?, NOW())
        """), {'customer_id': 1, 'credit_score': 600})
        
    @patch('your_module.engine')
    def test_calculate_credit_score_no_credit_card(self, mock_engine):
        mock_connection = mock_engine.connect.return_value
        mock_connection.execute.return_value.fetchone.side_effect = [
            (1000, 500, 300), 
            (0,), 
            (2,), 
        ]
        
        self.assertEqual(calculate_credit_score(1), 740)
        
        mock_connection.execute.assert_any_call(text("""
            UPDATE customers
            SET credit_score = ?
            WHERE customers.id = ?
        """), {'credit_score': 740, 'customer_id': 1})
        
        mock_connection.execute.assert_any_call(text("""
            INSERT INTO credit_score_alerts (customer_id, credit_score, created_at)
            VALUES (?, ?, NOW())
        """), {'customer_id': 1, 'credit_score': 740})
        
    @patch('your_module.engine')
    def test_calculate_credit_score_no_late_payments(self, mock_engine):
        mock_connection = mock_engine.connect.return_value
        mock_connection.execute.return_value.fetchone.side_effect = [
            (1000, 500, 300), 
            (200,), 
            (0,), 
        ]
        
        self.assertEqual(calculate_credit_score(1), 790)
        
        mock_connection.execute.assert_any_call(text("""
            UPDATE customers
            SET credit_score = ?
            WHERE customers.id = ?
        """), {'credit_score': 790, 'customer_id': 1})
        
        mock_connection.execute.assert_not_called()
        
if __name__ == '__main__':
    unittest.main()
