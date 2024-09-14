
from config import engine
import sqlalchemy as sa
import pandas as pd
import psycopg2

def generate_repayment_schedule(loan_id):
    # Define the query to get loan details
    loan_query = sa.text("""
        SELECT loanamount, interestrate, loanterm, startdate
        FROM loans
        WHERE loanid = :loan_id
    """)

    # Execute the query and fetch the results
    with engine.connect() as conn:
        result = conn.execute(loan_query, {"loan_id": loan_id}).fetchone()

    # Extract the loan details
    loan_amount, interest_rate, loan_term, start_date = result

    # Convert annual interest rate to monthly interest rate (divide by 12)
    monthly_interest_rate = interest_rate / 100 / 12

    # Calculate fixed monthly payment using the amortization formula
    monthly_payment = (loan_amount * monthly_interest_rate) / (1 - pow(1 + monthly_interest_rate, -loan_term))

    # Initialize balance to the loan amount
    balance = loan_amount

    # Initialize payment_date to the start date of the loan
    payment_date = start_date

    # Initialize payment number to 1
    payment_number = 1

    # Create a list to store the repayment schedule
    repayment_schedule = []

    # Loop through each month and calculate the repayment schedule
    while payment_number <= loan_term:
        # Calculate interest for the current month
        interest_amount = balance * monthly_interest_rate

        # Calculate principal for the current month
        principal_amount = monthly_payment - interest_amount

        # Deduct principal from balance
        balance -= principal_amount

        # Create a dictionary to store the repayment details
        repayment_details = {
            "loan_id": loan_id,
            "payment_number": payment_number,
            "payment_date": payment_date,
            "principal_amount": principal_amount,
            "interest_amount": interest_amount,
            "total_payment": monthly_payment,
            "balance": balance
        }

        # Append the repayment details to the list
        repayment_schedule.append(repayment_details)

        # Move to the next month
        payment_date += pd.Timedelta('1 month')
        payment_number += 1

    # Create an INSERT query to insert the repayment schedule into the RepaymentSchedule table
    insert_query = sa.text("""
        INSERT INTO repaymentschedule (loanid, paymentnumber, paymentdate, principalamount, interestamount, totalpayment, balance)
        VALUES (:loan_id, :payment_number, :payment_date, :principal_amount, :interest_amount, :total_payment, :balance)
    """)

    # Execute the INSERT query for each repayment detail
    with engine.connect() as conn:
        for detail in repayment_schedule:
            conn.execute(insert_query, detail)
        conn.commit()

    # Return the repayment schedule
    return repayment_schedule
