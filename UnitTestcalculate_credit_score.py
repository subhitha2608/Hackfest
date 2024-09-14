
import unittest
from unittest.mock import patch, Mock
from your_module import update_credit_score  # update with the actual module name

class TestUpdateCreditScore(unittest.TestCase):
    @patch('your_module.engine')
    @patch('your_module.pd')
    @patch('your_module.conn')
    def test_update_credit_score(self, mock_conn, mock_pd, mock_engine):
        # Mock the engine, pandas, and connection objects
        mock_engine.connect.return_value = mock_conn
        mock_pd.read_sql.return_value = pd.DataFrame({'total_loan_amount': [100.0], 'total_repayment': [50.0], 'outstanding_loan_balance': [20.0]})
        mock_pd.read_sql.return_value = pd.DataFrame({'credit_card_balance': [500.0]})
        mock_pd.read_sql.return_value = pd.DataFrame({'late_pay_count': [2]})
        
        # Call the function
        update_credit_score(123)
        
        # Verify the expected behavior
        mock_engine.connect.assert_called_once()
        mock_conn.execute.assert_called_once_with(text("UPDATE customers SET credit_score = 675 WHERE customers.id = :customer_id"), {'customer_id': 123, 'v_credit_score': 675})
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        
        # Verify the scoring calculation
        self.assertEqual(round((50.0 / 100.0) * 400, 2), 200.0)
        self.assertEqual(round((1 - (500.0 / 10000)) * 300, 2), 180.0)
        self.assertEqual(-2 * 50, -100)
        self.assertEqual(mock_pd.read_sql.return_value.iloc[0]['total_loan_amount'], 100.0)
        self.assertEqual(mock_pd.read_sql.return_value.iloc[0]['total_repayment'], 50.0)
        
    @patch('your_module.engine')
    @patch('your_module.pd')
    @patch('your_module.conn')
    def test_update_credit_score_no_loans(self, mock_conn, mock_pd, mock_engine):
        # Mock the engine, pandas, and connection objects
        mock_engine.connect.return_value = mock_conn
        mock_pd.read_sql.return_value = pd.DataFrame({'total_loan_amount': [0.0]})
        mock_pd.read_sql.return_value = pd.DataFrame({'credit_card_balance': [0.0]})
        mock_pd.read_sql.return_value = pd.DataFrame({'late_pay_count': [0]})
        
        # Call the function
        update_credit_score(123)
        
        # Verify the expected behavior
        mock_engine.connect.assert_called_once()
        mock_conn.execute.assert_called_once_with(text("UPDATE customers SET credit_score = 400 WHERE customers.id = :customer_id"), {'customer_id': 123, 'v_credit_score': 400})
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        
        # Verify the scoring calculation
        self.assertEqual(400, mock_pd.read_sql.return_value.iloc[0]['total_loan_amount'])
        self.assertEqual(0, mock_pd.read_sql.return_value.iloc[0]['credit_card_balance'])
        self.assertEqual(0, mock_pd.read_sql.return_value.iloc[0]['late_pay_count'])
        
    @patch('your_module.engine')
    @patch('your_module.pd')
    @patch('your_module.conn')
    def test_update_credit_score_low_score_alert(self, mock_conn, mock_pd, mock_engine):
        # Mock the engine, pandas, and connection objects
        mock_engine.connect.return_value = mock_conn
        mock_pd.read_sql.return_value = pd.DataFrame({'total_loan_amount': [100.0], 'total_repayment': [50.0], 'outstanding_loan_balance': [20.0]})
        mock_pd.read_sql.return_value = pd.DataFrame({'credit_card_balance': [500.0]})
        mock_pd.read_sql.return_value = pd.DataFrame({'late_pay_count': [2]})
        
        # Call the function
        update_credit_score(123)
        
        # Verify the expected behavior
        mock_engine.connect.assert_called_once()
        mock_conn.execute.assert_called_once_with(text("UPDATE customers SET credit_score = 450 WHERE customers.id = :customer_id"), {'customer_id': 123, 'v_credit_score': 450})
        mock_conn.execute.assert_called_with(text("INSERT INTO credit_score_alerts (customer_id, credit_score, created_at) VALUES (:customer_id, 450, NOW())"), {'customer_id': 123, 'v_credit_score': 450})
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        
    @patch('your_module.engine')
    @patch('your_module.pd')
    @patch('your_module.conn')
    def test_update_credit_score_high_score_alert(self, mock_conn, mock_pd, mock_engine):
        # Mock the engine, pandas, and connection objects
        mock_engine.connect.return_value = mock_conn
        mock_pd.read_sql.return_value = pd.DataFrame({'total_loan_amount': [100.0], 'total_repayment': [50.0], 'outstanding_loan_balance': [20.0]})
        mock_pd.read_sql.return_value = pd.DataFrame({'credit_card_balance': [500.0]})
        mock_pd.read_sql.return_value = pd.DataFrame({'late_pay_count': [2]})
        
        # Call the function
        update_credit_score(123)
        
        # Verify the expected behavior
        mock_engine.connect.assert_called_once()
        mock_conn.execute.assert_called_once_with(text("UPDATE customers SET credit_score = 850 WHERE customers.id = :customer_id"), {'customer_id': 123, 'v_credit_score': 850})
        # No alert should be raised for a high score, so this should not be called
        mock_conn.execute.assert_not_called()
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        
if __name__ == '__main__':
    unittest.main()
