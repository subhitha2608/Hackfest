
from config import engine
import pandas as pd
from sqlalchemy import text
import psycopg2

def generate_repayment_schedule(loan_id):
    # Get loan details
    query = text("""SELECT loanamount, interestrate, loanterm, startdate
                    FROM loans
                    WHERE loanid = :loan_id""")
    with engine.connect() as connection:
        result = connection.execute(query, {'loan_id': loan_id})
        loan_amount, interest_rate, loan_term, start_date = result.fetchone()

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

    # Create a list to store repayment schedule
    repayment_schedule = []

    # Loop through each month and calculate the repayment schedule
    while payment_number <= loan_term:
        # Calculate interest for the current month
        interest_amount = balance * monthly_interest_rate

        # Calculate principal for the current month
        principal_amount = monthly_payment - interest_amount

        # Deduct principal from balance
        balance -= principal_amount

        # Store repayment details
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
        payment_date += pd.Timedelta('1 month')
        payment_number += 1

    # Insert repayment schedule into the RepaymentSchedule table
    query = text("""INSERT INTO repaymentschedule (loanid, paymentnumber, paymentdate, principalamount, interestamount, totalpayment, balance)
                    VALUES (:loan_id, :payment_number, :payment_date, :principal_amount, :interest_amount, :total_payment, :balance)""")
    with engine.connect() as connection:
        for repayment in repayment_schedule:
            connection.execute(query, repayment)
        connection.commit()

    # Return the repayment schedule
    return pd.DataFrame(repayment_schedule)
