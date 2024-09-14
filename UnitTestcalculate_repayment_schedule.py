
import unittest
from unittest.mock import Mock, patch
from your_module import loan_repayment_schedule  # Import the function you want to test

class TestLoanRepaymentSchedule(unittest.TestCase):

    @patch('your_module.engine')
    @patch('psycopg2')
    def test_loan_repayment_schedule(self, mock_psycopg2, mock_engine):
        # Setup
        loan_id = 1
        expected_df = pd.DataFrame({
            "Payment Number": [1],
            "Payment Date": ["2022-01-01"],
            "Principal Amount": [100],
            "Interest Amount": [10],
            "Total Payment": [110],
            "Balance": [900]
        })

        # Mock the database operations
        mock_result = Mock()
        mock_result.fetchone.return_value = (1000, 10, 12, "2022-01-01")
        mock_engine.execute.return_value = mock_result

        # Call the function
        result = loan_repayment_schedule(loan_id)

        # Assert
        self.assertEqual(result.equals(expected_df), True)

    @patch('your_module.engine')
    @patch('psycopg2')
    def test_loan_repayment_schedule_invalid_loan_id(self, mock_psycopg2, mock_engine):
        # Setup
        loan_id = 1000

        # Mock the database operations
        mock_result = Mock()
        mock_result.fetchone.return_value = None
        mock_engine.execute.return_value = mock_result

        # Call the function
        with self.assertRaises(KeyError):
            loan_repayment_schedule(loan_id)

    @patch('your_module.engine')
    @patch('psycopg2')
    def test_loan_repayment_schedule_non Numeric_loan_id(self, mock_psycopg2, mock_engine):
        # Setup
        loan_id = "test"

        # Mock the database operations
        mock_result = Mock()
        mock_engine.execute.side_effect = [psycopg2.ProgrammingError("Cannot convert type 'str' to int")]
        mock_result.fetchone.return_value = None
        mock_engine.execute.return_value = mock_result

        # Call the function
        with self.assertRaises(psycopg2.ProgrammingError):
            loan_repayment_schedule(loan_id)

    @patch('your_module.engine')
    @patch('psycopg2')
    def test_loan_repayment_schedule_zero_loan_amount(self, mock_psycopg2, mock_engine):
        # Setup
        loan_id = 1
        expected_df = pd.DataFrame({
            "Payment Number": [1],
            "Payment Date": ["2022-01-01"],
            "Principal Amount": [0],
            "Interest Amount": [0],
            "Total Payment": [0],
            "Balance": [0]
        })

        # Mock the database operations
        mock_result = Mock()
        mock_result.fetchone.return_value = (0, 10, 12, "2022-01-01")
        mock_engine.execute.return_value = mock_result

        # Call the function
        result = loan_repayment_schedule(loan_id)

        # Assert
        self.assertEqual(result.equals(expected_df), True)

    @patch('your_module.engine')
    @patch('psycopg2')
    def test_loan_repayment_schedule_zero_interest_rate(self, mock_psycopg2, mock_engine):
        # Setup
        loan_id = 1
        expected_df = pd.DataFrame({
            "Payment Number": [1],
            "Payment Date": ["2022-01-01"],
            "Principal Amount": [1000],
            "Interest Amount": [0],
            "Total Payment": [1000],
            "Balance": [0]
        })

        # Mock the database operations
        mock_result = Mock()
        mock_result.fetchone.return_value = (1000, 0, 12, "2022-01-01")
        mock_engine.execute.return_value = mock_result

        # Call the function
        result = loan_repayment_schedule(loan_id)

        # Assert
        self.assertEqual(result.equals(expected_df), True)

    @patch('your_module.engine')
    @patch('psycopg2')
    def test_loan_repayment_schedule_zero_loan_term(self, mock_psycopg2, mock_engine):
        # Setup
        loan_id = 1
        expected_df = pd.DataFrame({
            "Payment Number": [1],
            "Payment Date": ["2022-01-01"],
            "Principal Amount": [1000],
            "Interest Amount": [0],
            "Total Payment": [1000],
            "Balance": [0]
        })

        # Mock the database operations
        mock_result = Mock()
        mock_result.fetchone.return_value = (1000, 10, 0, "2022-01-01")
        mock_engine.execute.return_value = mock_result

        # Call the function
        result = loan_repayment_schedule(loan_id)

        # Assert
        self.assertEqual(result.equals(expected_df), True)

    @patch('your_module.engine')
    @patch('psycopg2')
    def test_loan_repayment_schedule_loan_term_greater_thanZero(self, mock_psycopg2, mock_engine):
        # Setup
        loan_id = 1
        expected_df = pd.DataFrame({
            "Payment Number": [1],
            "Payment Date": ["2022-01-01"],
            "Principal Amount": [1000],
            "Interest Amount": [0],
            "Total Payment": [1000],
            "Balance": [0]
        })

        # Mock the database operations
        mock_result = Mock()
        mock_result.fetchone.return_value = (1000, 10, 12, "2022-01-01")
        mock_engine.execute.return_value = mock_result

        # Call the function
        result = loan_repayment_schedule(loan_id)

        # Assert
        self.assertEqual(result.equals(expected_df), True)

if __name__ == '__main__':
    unittest.main()
