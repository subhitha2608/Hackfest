
import unittest
from unittest.mock import patch
from your_module import calculate_repayment_schedule  # Replace with the actual module name

class TestCalculateRepaymentSchedule(unittest.TestCase):
    @patch('your_module.engine')
    @patch('your_module(pd)')
    def test_calculate_repayment_schedule(self, mock_pd, mock_engine):
        # Test with valid data
        loan_id = 123
        loan_details = pd.DataFrame({
            'loanamount': [100000],
            'interestrate': [5],
            'loanterm': [36],
            'startdate': ['2022-01-01']
        })
        mock_pd.read_sql.return_value = loan_details

        # Test with annual interest rate
        interest_rate = loan_details['interestrate'].values[0] / 100
        monthly_interest_rate = interest_rate / 12

        # Test with monthly payment
        monthly_payment = (loan_details['loanamount'].values[0] * monthly_interest_rate) / (1 - pow((1 + monthly_interest_rate), -loan_details['loanterm'].values[0]))

        # Test with repayment schedule
        repayment_schedule = []
        for i in range(1, 37):
            interest_amount = loan_details['loanamount'].values[0] * monthly_interest_rate
            principal_amount = monthly_payment - interest_amount
            balance = loan_details['loanamount'].values[0] - principal_amount
            repayment_schedule.append({
                'loan_id': loan_id,
                'payment_number': i,
                'payment_date': '2022-01-01' + str(i * 30) + ':00',
                'principal_amount': principal_amount,
                'interest_amount': interest_amount,
                'total_payment': monthly_payment,
                'balance': balance
            })

        # Test the function
        with patch.object(mock_engine, 'connect') as mock_conn:
            with patch.object(mock_conn, 'execute') as mock_execute:
                result = calculate_repayment_schedule(loan_id)
                self.assertEqual(result, repayment_schedule)
                self.assertEqual(mock_execute.call_count, 1)

        # Test with invalid data
        loan_id = 999
        loan_details = pd.DataFrame({
            'loanamount': [0],
            'interestrate': [10],
            'loanterm': [0],
            'startdate': ['2030-01-01']
        })
        mock_pd.read_sql.return_value = loan_details

        # Test the function
        with patch.object(mock_engine, 'connect') as mock_conn:
            with patch.object(mock_conn, 'execute') as mock_execute:
                result = calculate_repayment_schedule(loan_id)
                self.assertEqual(result, [])
                self.assertEqual(mock_execute.call_count, 0)

    def test_calculate_repayment_schedule_engine_exception(self):
        # Test with engine exception
        loan_id = 123
        mock_engine = MockEngine()
        mock_engine.connect().execute.side_effect = Exception()
        result = calculate_repayment_schedule(loan_id)
        self.assertEqual(result, [])

    def test_calculate_repayment_schedule_sqlalchemy_text_exception(self):
        # Test with sqlalchemy text exception
        loan_id = 123
        mock_engine = MockEngine()
        mock_engine.connect().execute.side_effect = SQLAlchemyTextException()
        result = calculate_repayment_schedule(loan_id)
        self.assertEqual(result, [])

class MockEngine:
    def connect(self):
        return MockConnection()

class MockConnection:
    def execute(self, text, *args, **kwargs):
        raise Exception()

class MockSQLAlchemyTextException:
    pass
