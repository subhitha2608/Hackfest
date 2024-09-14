
from config import engine
from sqlalchemy import text
import pandas as pd

def calculate_repayment_schedule(loan_id):
    # Get loan details
    query = text("""
        SELECT loanamount, interestrate, loanterm, startdate 
        FROM loans 
        WHERE loanid = :loan_id""")
    loan_amount, interest_rate, loan_term, start_date = engine.execute(query, loan_id=loan_id).fetchone()

    # Convert annual interest rate to monthly interest rate (divide by 12)
    monthly_interest_rate = interest_rate / 100 / 12

    # Calculate fixed monthly payment using the amortization formula
    monthly_payment = (loan_amount * monthly_interest_rate) / (1 - pow(1 + monthly_interest_rate, -loan_term))
    balance = loan_amount
    payment_date = start_date
    payment_number = 1

    # Loop through each month and calculate the repayment schedule
    repayment_schedule = []
    while payment_number <= loan_term:
        # Calculate interest for the current month
        interest_amount = balance * monthly_interest_rate

        # Calculate principal for the current month
        principal_amount = monthly_payment - interest_amount

        # Deduct principal from balance
        balance -= principal_amount

        # Insert repayment details into the RepaymentSchedule table
        repayment_schedule.append({
            'loanid': loan_id,
            'paymentnumber': payment_number,
            'paymentdate': payment_date,
            'principalamount': principal_amount,
            'interestamount': interest_amount,
            'totalpayment': monthly_payment,
            'balance': balance
        })

        # Move to the next month
        payment_date += pd.Timedelta(days=30)
        payment_number += 1

    # Insert the repayment schedule into the database
    insert_query = text("""
        INSERT INTO repaymentschedule (loanid, paymentnumber, paymentdate, principalamount, interestamount, totalpayment, balance) 
        VALUES (:loan_id, :payment_number, :payment_date, :principal_amount, :interest_amount, :total_payment, :balance)""")
    for row in repayment_schedule:
        engine.execute(insert_query, row)

    return repayment_schedule
