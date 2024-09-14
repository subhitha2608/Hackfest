Python
import sqlalchemy as sa
from sqlalchemy import text
import pandas as pd

from config import engine

# Define the function to calculate the repayment schedule
def calculate_repayment_schedule(loan_id):
    conn = engine.connect()
    
    # Execute the query to get loan details
    loan_details = conn.execute(text("""
        SELECT loanamount, interestrate, loanterm, startdate
        FROM loans
        WHERE loanid = :loan_id
    """), {'loan_id': loan_id}).fetchone()

    if loan_details:
        loan_amount, interest_rate, loan_term, start_date = loan_details
        monthly_interest_rate = round(interest_rate / 100 / 12, 6)
        monthly_payment = round((loan_amount * monthly_interest_rate) / (1 - pow(1 + monthly_interest_rate, -loan_term)), 2)
        balance = loan_amount
        payment_date = start_date
        payment_number = 1

        # Initialize the repayment schedule DataFrame
        repayment_schedule = []

        while payment_number <= loan_term:
            interest_amount = balance * monthly_interest_rate
            principal_amount = monthly_payment - interest_amount
            balance -= principal_amount
            repayment_schedule.append({
                'loan_id': loan_id,
                'payment_number': payment_number,
                'payment_date': payment_date,
                'principal_amount': principal_amount,
                'interest_amount': interest_amount,
                'total_payment': monthly_payment,
                'balance': balance
            })

            payment_date += pd.Timedelta(days=30)
            payment_number += 1

        # Insert the repayment schedule into the repaymentschedule table
        conn.execute(text("""
            INSERT INTO repaymentschedule (loanid, paymentnumber, paymentdate, principalamount, interestamount, totalpayment, balance)
            VALUES (:loan_id, :payment_number, :payment_date, :principal_amount, :interest_amount, :total_payment, :balance)
        """), repayment_schedule)

        conn.commit()
    else:
        print(f"No loan found for ID {loan_id}")
    finally:
        conn.close()
