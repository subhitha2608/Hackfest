
from config import engine
from sqlalchemy import text
import pandas as pd
import psycopg2

def calculate_repayment_schedule(loan_id):
    # Define the query to retrieve loan details
    loan_details_query = text("""
        SELECT loanamount, interestrate, loanterm, startdate
        FROM loans
        WHERE loanid = :loan_id
    """)

    # Execute the query and retrieve loan details
    with engine.connect() as conn:
        result = conn.execute(loan_details_query, {'loan_id': loan_id})
        loan_details = result.fetchone()

    if loan_details is None:
        raise ValueError("Loan ID not found")

    loan_amount, interest_rate, loan_term, start_date = loan_details

    # Convert annual interest rate to monthly interest rate
    monthly_interest_rate = interest_rate / 100 / 12

    # Calculate fixed monthly payment using the amortization formula
    monthly_payment = (loan_amount * monthly_interest_rate) / (1 - pow(1 + monthly_interest_rate, -loan_term))

    # Initialize balance to the loan amount
    balance = loan_amount

    # Initialize payment_date to the start date of the loan
    payment_date = start_date

    # Initialize payment number
    payment_number = 1

    # Create a list to store repayment schedule details
    repayment_schedule = []

    # Loop through each month and calculate the repayment schedule
    while payment_number <= loan_term:
        # Calculate interest for the current month
        interest_amount = balance * monthly_interest_rate

        # Calculate principal for the current month
        principal_amount = monthly_payment - interest_amount

        # Deduct principal from balance
        balance -= principal_amount

        # Create a dictionary to store repayment details
        repayment_details = {
            'loanid': loan_id,
            'paymentnumber': payment_number,
            'paymentdate': payment_date,
            'principalamount': principal_amount,
            'interestamount': interest_amount,
            'totalpayment': monthly_payment,
            'balance': balance
        }

        # Append repayment details to the list
        repayment_schedule.append(repayment_details)

        # Move to the next month
        payment_date += pd.Timedelta(days=30)
        payment_number += 1

    # Insert repayment schedule into the RepaymentSchedule table
    insertion_query = text("""
        INSERT INTO repaymentschedule (loanid, paymentnumber, paymentdate, principalamount, interestamount, totalpayment, balance)
        VALUES (:loanid, :paymentnumber, :paymentdate, :principalamount, :interestamount, :totalpayment, :balance)
    """)

    with engine.connect() as conn:
        for repayment_details in repayment_schedule:
            conn.execute(insertion_query, repayment_details)
        conn.commit()

    return repayment_schedule
