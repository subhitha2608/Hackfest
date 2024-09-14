
from config import engine
from sqlalchemy import text
import pandas as pd
import psycopg2

def calculate_repayment_schedule(loan_id):
    # Define SQL queries as text objects
    get_loan_details_query = text("""
        SELECT loanamount, interestrate, loanterm, startdate
        FROM loans
        WHERE loanid = :loan_id
    """)

    insert_repayment_schedule_query = text("""
        INSERT INTO repaymentschedule (loanid, paymentnumber, paymentdate, principalamount, interestamount, totalpayment, balance)
        VALUES (:loan_id, :payment_number, :payment_date, :principal_amount, :interest_amount, :monthly_payment, :balance)
    """)

    # Execute get loan details query
    with engine.connect() as conn:
        result = conn.execute(get_loan_details_query, {"loan_id": loan_id})
        loan_amount, interest_rate, loan_term, start_date = result.fetchone()

    # Calculate monthly interest rate
    monthly_interest_rate = interest_rate / 100 / 12

    # Calculate fixed monthly payment using the amortization formula
    monthly_payment = (loan_amount * monthly_interest_rate) / (1 - pow(1 + monthly_interest_rate, -loan_term))

    # Initialize variables
    balance = loan_amount
    payment_date = start_date
    payment_number = 1

    # Loop through each month and calculate the repayment schedule
    while payment_number <= loan_term:
        # Calculate interest for the current month
        interest_amount = balance * monthly_interest_rate

        # Calculate principal for the current month
        principal_amount = monthly_payment - interest_amount

        # Deduct principal from balance
        balance -= principal_amount

        # Execute insert repayment schedule query
        with engine.connect() as conn:
            conn.execute(insert_repayment_schedule_query, {
                "loan_id": loan_id,
                "payment_number": payment_number,
                "payment_date": payment_date,
                "principal_amount": principal_amount,
                "interest_amount": interest_amount,
                "monthly_payment": monthly_payment,
                "balance": balance
            })
            conn.commit()

        # Move to the next month
        payment_date += pd.DateOffset(months=1)
        payment_number += 1

    # Return None, as the procedure doesn't return a value
    return None
