
import unittest
from unittest.mock import patch, Mock
from your_module import calculate_repayment_schedule

class TestCalculateRepaymentSchedule(unittest.TestCase):

    @patch('your_module.engine.execute')
    @patch('your_module.engine')
    @patch('pandas.to_datetime')
    def test_calculate_repayment_schedule(self, mock_pandas_to_datetime, mock_sqlalchemy_engine, mock_engine_execute):
        loan_id = 1
        loan_amount = 10000
        interest_rate = 5
        loan_term = 60
        start_date = '2020-01-01'

        mock_sqlalchemy_engine.execute.return_value = [(loan_amount, interest_rate, loan_term, start_date)]
        mock_pandas_to_datetime.return_value = start_date
        mock_engine_execute.side_effect = [Mock(return_value=(loan_amount, interest_rate, loan_term, start_date)),
                                            Mock(return_value=None),
                                            Mock(return_value=None),
                                            Mock(return_value=None)]

        result = calculate_repayment_schedule(loan_id)
        self.assertEqual(result, [])

    @patch('your_module.engine.execute')
    @patch('your_module.engine')
    @patch('pandas.to_datetime')
    def test_calculate_repayment_schedule_loanterm_zero(self, mock_pandas_to_datetime, mock_sqlalchemy_engine, mock_engine_execute):
        loan_id = 1
        loan_amount = 10000
        interest_rate = 5
        loan_term = 0
        start_date = '2020-01-01'

        mock_sqlalchemy_engine.execute.return_value = [(loan_amount, interest_rate, loan_term, start_date)]
        mock_pandas_to_datetime.return_value = start_date
        mock_engine_execute.side_effect = [Mock(return_value=(loan_amount, interest_rate, loan_term, start_date)),
                                            Mock(return_value=None),
                                            Mock(return_value=None),
                                            Mock(return_value=None)]

        result = calculate_repayment_schedule(loan_id)
        self.assertEqual(result, [])

    @patch('your_module.engine.execute')
    @patch('your_module.engine')
    @patch('pandas.to_datetime')
    def test_calculate_repayment_schedule_loanterm_negative(self, mock_pandas_to_datetime, mock_sqlalchemy_engine, mock_engine_execute):
        loan_id = 1
        loan_amount = 10000
        interest_rate = 5
        loan_term = -1
        start_date = '2020-01-01'

        mock_sqlalchemy_engine.execute.return_value = [(loan_amount, interest_rate, loan_term, start_date)]
        mock_pandas_to_datetime.return_value = start_date
        mock_engine_execute.side_effect = [Mock(return_value=(loan_amount, interest_rate, loan_term, start_date)),
                                            Mock(return_value=None),
                                            Mock(return_value=None),
                                            Mock(return_value=None)]

        with self.assertRaises(ValueError):
            calculate_repayment_schedule(loan_id)

    @patch('your_module.engine.execute')
    @patch('your_module.engine')
    @patch('pandas.to_datetime')
    def test_calculate_repayment_schedule_interestrate_zero(self, mock_pandas_to_datetime, mock_sqlalchemy_engine, mock_engine_execute):
        loan_id = 1
        loan_amount = 10000
        interest_rate = 0
        loan_term = 60
        start_date = '2020-01-01'

        mock_sqlalchemy_engine.execute.return_value = [(loan_amount, interest_rate, loan_term, start_date)]
        mock_pandas_to_datetime.return_value = start_date
        mock_engine_execute.side_effect = [Mock(return_value=(loan_amount, interest_rate, loan_term, start_date)),
                                            Mock(return_value=None),
                                            Mock(return_value=None),
                                            Mock(return_value=None)]

        result = calculate_repayment_schedule(loan_id)
        self.assertEqual(result, [])

    @patch('your_module.engine.execute')
    @patch('your_module.engine')
    @patch('pandas.to_datetime')
    def test_calculate_repayment_schedule_non_integer_loan_term(self, mock_pandas_to_datetime, mock_sqlalchemy_engine, mock_engine_execute):
        loan_id = 1
        loan_amount = 10000
        interest_rate = 5
        loan_term = 3.5
        start_date = '2020-01-01'

        mock_sqlalchemy_engine.execute.return_value = [(loan_amount, interest_rate, loan_term, start_date)]
        mock_pandas_to_datetime.return_value = start_date
        mock_engine_execute.side_effect = [Mock(return_value=(loan_amount, interest_rate, loan_term, start_date)),
                                            Mock(return_value=None),
                                            Mock(return_value=None),
                                            Mock(return_value=None)]

        with self.assertRaises(ValueError):
            calculate_repayment_schedule(loan_id)

if __name__ == '__main__':
    unittest.main()
