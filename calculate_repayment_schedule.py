
from sqlalchemy import text
import pandas as pd
import psycopg2
from config import engine

def calculate_repayment_schedule(loan_id):
    # Get loan details
    query = text("SELECT loanamount, interestrate, loanterm, startdate FROM loans WHERE loanid = :loan_id")
    result = engine.execute(query, {"loan_id": loan_id})
    row = result.fetchone()
    loan_amount = row[0]
    interest_rate = row[1]
    loan_term = row[2]
    start_date = row[3]

    # Convert annual interest rate to monthly interest rate (divide by 12)
    monthly_interest_rate = interest_rate / 100 / 12

    # Calculate fixed monthly payment using the amortization formula
    monthly_payment = (loan_amount * monthly_interest_rate) / (1 - pow(1 + monthly_interest_rate, -loan_term))

    # Initialize balance to the loan amount
    balance = loan_amount

    # Initialize payment_date to the start date of the loan
    payment_date = start_date

    # Initialize payment number
    payment_number = 1

    # Loop through each month and calculate the repayment schedule
    while payment_number <= loan_term:
        # Calculate interest for the current month
        interest_amount = balance * monthly_interest_rate

        # Calculate principal for the current month
        principal_amount = monthly_payment - interest_amount

        # Deduct principal from balance
        balance -= principal_amount

        # Insert repayment details into the RepaymentSchedule table
        query = text("INSERT INTO repaymentschedule (loanid, paymentnumber, paymentdate, principalamount, interestamount, totalpayment, balance) VALUES (:loan_id, :payment_number, :payment_date, :principal_amount, :interest_amount, :monthly_payment, :balance)")
        engine.execute(query, {
            "loan_id": loan_id,
            "payment_number": payment_number,
            "payment_date": payment_date,
            "principal_amount": principal_amount,
            "interest_amount": interest_amount,
            "monthly_payment": monthly_payment,
            "balance": balance
        })
        engine.commit()

        # Move to the next month
        payment_date += pd.Timedelta(days=30)
        payment_number += 1

    # Return the repayment schedule
    query = text("SELECT * FROM repaymentschedule WHERE loanid = :loan_id")
    result = engine.execute(query, {"loan_id": loan_id})
    repayment_schedule = pd.DataFrame(result.fetchall(), columns=[desc[0] for desc in result.cursor.description])
    return repayment_schedule
