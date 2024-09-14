
import unittest
from unittest.mock import patch
from your_file import calculate_repayment_schedule

class TestCalculateRepaymentSchedule(unittest.TestCase):
    def setUp(self):
        self.engine = None
        self.query = None
        self.create_table_query = None
        self.loan_id = 1
        self.monthly_interest_rate = 0.05
        self.monthly_payment = 1000
        self.loan_term = 60

    def test_calculate_repayment_schedule(self):
        with patch('config.engine.connect') as connection_patch:
            connection_patch.return_value = None
            calculate_repayment_schedule(self.loan_id)
            connection_patch.assert_called_once_with()
            connection_patch.return_value.executing.assert_called_once_with(self.query)

    def test_create_repayment_schedule_table_if_non_existent(self):
        with patch('config.engine.execute') as create_table_patch:
            calculate_repayment_schedule(self.loan_id)
            create_table_patch.assert_called_once_with(self.create_table_query)

    def test_repayment_schedule_query(self):
        expected_query = """
            WITH loan_details AS (
                SELECT loanamount, interestrate, loanterm, startdate
                FROM loans
                WHERE loanid = :loan_id
            ),
            repayment_schedule AS (
                SELECT 
                    1 AS payment_number,
                    startdate AS payment_date,
                    loanamount AS balance,
                    0 AS interest_amount,
                    loanamount AS principal_amount
                FROM loan_details
                UNION ALL
                SELECT 
                    ps.payment_number + 1,
                    ps.payment_date + INTERVAL '1 month',
                    ps.balance - ps.principal_amount AS balance,
                    ps.balance * (:monthly_interest_rate / 100 / 12) AS interest_amount,
                    (:monthly_payment - ps.interest_amount) AS principal_amount
                FROM repayment_schedule AS ps
                WHERE ps.payment_number < :loan_term
            )
            INSERT INTO repaymentschedule (loanid, paymentnumber, paymentdate, principalamount, interestamount, totalpayment, balance)
            SELECT 
                :loan_id,
                payment_number,
                payment_date,
                principal_amount,
                interest_amount,
                :monthly_payment,
                balance
            FROM repayment_schedule;
        """
        self.assertEqual(expected_query, self.query)

    def test_repayment_schedule_query_bindings(self):
        expected_bindings = {
            'loan_id': self.loan_id,
            'monthly_interest_rate': self.monthly_interest_rate,
            'monthly_payment': self.monthly_payment,
            'loan_term': self.loan_term,
        }
        self.assertEqual(expectedbindings, self.queryExecutionContext.binds)

    def test_commit_connection(self):
        with patch('sqlalchemy.engine.Connection.commit') as commit_patch:
            calculate_repayment_schedule(self.loan_id)
            commit_patch.assert_called_once()

    def test_connection_close(self):
        with patch('sqlalchemy.engine.Connection.close') as close_patch:
            calculate_repayment_schedule(self.loan_id)
            close_patch.assert_called_once()

if __name__ == '__main__':
    unittest.main()
