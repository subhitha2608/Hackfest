Python
from unittest import TestCase, mock
from your_module import calculate_repayment_schedule  # Import the module with the function

class TestCalculateRepaymentSchedule(TestCase):
    @mock.patch('your_module.engine')
    @mock.patch('your_module.text')
    @mock.patch('your_module(pd)')
    def test_calculate_repayment_schedule(self, mock_pd, mock_text, mock_engine):
        # Mock the engine for connecting to the database
        mock_conn = mock_engine.connect.return_value
        mock_query = mock_text.return_value
        
        # Mock the fetchone query
        mock_query.execute.return_value = [(1000, 5, 36, '2020-01-01')]  # Mock loan details
        conn = engine.connect()
        
        # Get loan details
        loan_details_query = text("""
        SELECT loanamount, interestrate, loanterm, startdate
        FROM loans
        WHERE loanid = :loan_id
        """)
        loan_details = conn.execute(loan_details_query, {'loan_id': 123}).fetchone()
        loan_amount, interest_rate, loan_term, start_date = loan_details

        # Convert annual interest rate to monthly interest rate
        monthly_interest_rate = (interest_rate / 100 / 12)

        # Calculate fixed monthly payment
        monthly_payment = (loan_amount * monthly_interest_rate) / (1 - pow(1 + monthly_interest_rate, -loan_term))

        # Initialize balance and payment_date
        balance = loan_amount
        payment_date = start_date

        # Initialize payment_number
        payment_number = 1

        # Create a list to store repayment details
        repayment_schedule = []
        while payment_number <= loan_term:
            # Calculate interest and principal for the current month
            interest_amount = balance * monthly_interest_rate
            principal_amount = monthly_payment - interest_amount

            # Deduct principal from balance
            balance -= principal_amount

            # Add repayment details to the list
            repayment_schedule.append({
                'loanid': 123,
                'paymentnumber': payment_number,
                'paymentdate': payment_date.strftime('%Y-%m-%d'),
                'principalamount': principal_amount,
                'interestamount': interest_amount,
                'totalpayment': monthly_payment,
                'balance': balance
            })

            # Move to the next month
            payment_date += pd.Timedelta(days=30)
            payment_number += 1

        # Insert repayment details into the RepaymentSchedule table
        insert_query = text("""
        INSERT INTO repaymentschedule (loanid, paymentnumber, paymentdate, principalamount, interestamount, totalpayment, balance)
        VALUES (:loan_id, :payment_number, :payment_date, :principal_amount, :interest_amount, :monthly_payment, :balance)
        """)
        mock_conn.execute.return_value = None
        conn.commit()
        conn.close()
        
        # Create a pandas Series from the repayment schedule
        result = calculate_repayment_schedule(123)
        result = pd.DataFrame(result)
        # Test
        self.assertEqual(result.shape, (36, 7))
        
        # Test the columns
        self.assertEqual(set(result.columns), {'loanid', 'paymentnumber', 'paymentdate', 'principalamount', 'interestamount', 'totalpayment', 'balance'})


if __name__ == "__main__":
    unittest.main()

    # Test with different inputs to check all edge cases
    test_calculate_repayment_schedule(1)
    test_calculate_repayment_schedule(None)
    test_calculate_repayment_schedule('')
    test_calculate_repayment_schedule(0)

