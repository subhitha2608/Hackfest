
from config import engine
import sqlalchemy as sa
import pandas as pd
import psycopg2

def generate_repayment_schedule(loan_id):
    # Define the query to get loan details
    loan_details_query = sa.text("""
        SELECT loanamount, interestrate, loanterm, startdate
        FROM loans
        WHERE loanid = :loan_id
    """)

    # Execute the query and fetch the loan details
    with engine.connect() as conn:
        result = conn.execute(loan_details_query, {"loan_id": loan_id})
        loan_details = result.fetchone()

    # Extract the loan details
    loan_amount, interest_rate, loan_term, start_date = loan_details

    # Calculate the monthly interest rate
    monthly_interest_rate = interest_rate / 100 / 12

    # Calculate the fixed monthly payment using the amortization formula
    monthly_payment = (loan_amount * monthly_interest_rate) / (1 - pow(1 + monthly_interest_rate, -loan_term))

    # Initialize the balance and payment date
    balance = loan_amount
    payment_date = start_date
    payment_number = 1

    # Create the repayment schedule
    repayment_schedule = []
    while payment_number <= loan_term:
        # Calculate the interest and principal for the current month
        interest_amount = balance * monthly_interest_rate
        principal_amount = monthly_payment - interest_amount

        # Deduct principal from balance
        balance -= principal_amount

        # Create a dictionary to store the repayment details
        repayment_details = {
            "loanid": loan_id,
            "paymentnumber": payment_number,
            "paymentdate": payment_date,
            "principalamount": principal_amount,
            "interestamount": interest_amount,
            "totalpayment": monthly_payment,
            "balance": balance
        }

        # Append the repayment details to the schedule
        repayment_schedule.append(repayment_details)

        # Move to the next month
        payment_date += pd.DateOffset(months=1)
        payment_number += 1

    # Insert the repayment schedule into the RepaymentSchedule table
    insert_query = sa.text("""
        INSERT INTO repaymentschedule (loanid, paymentnumber, paymentdate, principalamount, interestamount, totalpayment, balance)
        VALUES (:loanid, :paymentnumber, :paymentdate, :principalamount, :interestamount, :totalpayment, :balance)
    """)
    with engine.connect() as conn:
        for repayment_details in repayment_schedule:
            conn.execute(insert_query, repayment_details)
        conn.commit()

    # Return the repayment schedule
    return pd.DataFrame(repayment_schedule)
