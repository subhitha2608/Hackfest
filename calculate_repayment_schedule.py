
from config import engine
import sqlalchemy as sa
import pandas as pd
import psycopg2

def calculate_repayment_schedule(loan_id):
    # Execute raw SQL query to retrieve loan details
    query = text("SELECT loanamount, interestrate, loanterm, startdate FROM loans WHERE loanid = :loan_id")
    result = engine.execute(query, loan_id=loan_id).fetchone()

    # Convert annual interest rate to monthly interest rate
    interest_rate = result['interestrate'] / 100 / 12

    # Calculate fixed monthly payment
    loan_amount = result['loanamount']
    monthly_payment = (loan_amount * interest_rate) / (1 - pow(1 + interest_rate, -result['loanterm']))

    # Initialize balance to the loan amount and payment date to the start date
    balance = loan_amount
    payment_date = result['startdate']

    # Initialize payment number
    payment_number = 1

    # Initialize empty list to store repayment schedule
    repayment_schedule = []

    # Loop through each month and calculate the repayment schedule
    while payment_number <= result['loanterm']:
        # Calculate interest for the current month
        interest_amount = balance * interest_rate

        # Calculate principal for the current month
        principal_amount = monthly_payment - interest_amount

        # Deduct principal from balance
        balance = balance - principal_amount

        # Insert repayment details into the RepaymentSchedule table
        query = text("INSERT INTO repaymentschedule (loanid, paymentnumber, paymentdate, principalamount, interestamount, totalpayment, balance) VALUES (:loan_id, :payment_number, :payment_date, :principal_amount, :interest_amount, :monthly_payment, :balance)")
        engine.execute(query, loan_id=loan_id, payment_number=payment_number, payment_date=payment_date, principal_amount=principal_amount, interest_amount=interest_amount, monthly_payment=monthly_payment, balance=balance)

        # Move to the next month
        payment_date += pd.Timedelta(days=30)
        payment_number += 1

    return repayment_schedule
