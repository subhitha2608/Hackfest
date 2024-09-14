
import unittest
from datetime import datetime, timedelta
from pandas.tseries.offsets import MonthEnd
from your_module import calculate_repayment_schedule  # import the function

class TestCalculateRepaymentSchedule(unittest.TestCase):

    def test_calculate_repayment_schedule(self):
        loan_id = 123
        loan_amount = 100000
        interest_rate = 5
        loan_term = 60

        # create a response similar to engine.execute(query, loan_id=loan_id).fetchone()
        loan_details = (loan_amount, interest_rate/100/12, loan_term, '2020-01-01')

        # mock engine.execute to simulate database operation
        def mock_execute(query, loan_id):
            if query == text("""
                SELECT loanamount, interestrate, loanterm, startdate 
                FROM loans 
                WHERE loanid = :loan_id"""),
            return [loan_details]
            elif query == text("""
                INSERT INTO repaymentschedule (loanid, paymentnumber, paymentdate, principalamount, interestamount, totalpayment, balance) 
                VALUES (:loan_id, :payment_number, :payment_date, :principal_amount, :interest_amount, :total_payment, :balance)"""),
                    return None

        # Test for valid data
        result = calculate_repayment_schedule(loan_id)
        self.assertIsNotNone(result)

        # Test for invalid data
        loan_id_invalid = 555
        result_invalid = calculate_repayment_schedule(loan_id_invalid)
        self.assertIsNone(result_invalid)

    def test_calculate_repayment_schedule_error(self):
        loan_id = 123
        loan_amount = 100000
        interest_rate = 5
        loan_term = 1

        loan_details = (loan_amount, interest_rate/100/12, loan_term, '2020-01-01')
        repayment_schedule = []

        monthly_payment = (loan_amount * interest_rate/100/12) / (1 - pow(1 + interest_rate/100/12, -loan_term))
        payment_date = datetime.strptime('2020-01-01', '%Y-%m-%d')
        payment_number = 1
        balance = loan_amount

        while payment_number <= loan_term:
            interest_amount = balance * interest_rate/100/12
            principal_amount = monthly_payment - interest_amount
            balance -= principal_amount
            repayment_schedule.append({
                'loanid': loan_id,
                'paymentnumber': payment_number,
                'paymentdate': payment_date,
                'principalamount': principal_amount,
                'interestamount': interest_amount,
                'totalpayment': monthly_payment,
                'balance': balance
            })
            payment_date += timedelta(days=30)
            payment_number += 1

        # Test Case 1: Empty Repayment Schedule
        self.assertEqual(len(repayment_schedule), loan_term)

        # Test Case 2: Last Payment with 0 Principal Amount
        self.assertEqual(repayment_schedule[-1]['principalamount'], 0)

        # Test Case 3: Last Payment with 0 Balance
        self.assertEqual(repayment_schedule[-1]['balance'], 0)

if __name__ == '__main__':
    unittest.main()
