Python
from config import engine
import pandas as pd

def calculate_repayment_schedule(loan_id):
    from sqlalchemy import text
    conn = engine.connect()

    # Get loan details
    loan_details = pd.read_sql(text("SELECT loanamount, interestrate, loanterm, startdate FROM loans WHERE loanid = :loan_id"), conn, params={'loan_id': loan_id})

    loan_amount = loan_details['loanamount'].values[0]
    interest_rate = loan_details['interestrate'].values[0]
    loan_term = loan_details['loanterm'].values[0]
    start_date = loan_details['startdate'].values[0]

    # Convert annual interest rate to monthly interest rate (divide by 12)
    monthly_interest_rate = (interest_rate / 100) / 12

    # Calculate fixed monthly payment using the amortization formula
    monthly_payment = (loan_amount * monthly_interest_rate) / (1 - pow((1 + monthly_interest_rate), -loan_term))

    # Initialize balance to the loan amount
    balance = loan_amount

    # Initialize payment_date to the start date of the loan
    payment_date = start_date

    # Initialize payment_number to 1
    payment_number = 1

    # Initialize repayment_schedule list
    repayment_schedule = []

    # Loop through each month and calculate the repayment schedule
    while payment_number <= loan_term:
        # Calculate interest for the current month
        interest_amount = balance * monthly_interest_rate

        # Calculate principal for the current month
        principal_amount = monthly_payment - interest_amount

        # Deduct principal from balance
        balance = balance - principal_amount

        # Append repayment details to the repayment_schedule list
        repayment_schedule.append({
            'loan_id': loan_id,
            'payment_number': payment_number,
            'payment_date': payment_date,
            'principal_amount': principal_amount,
            'interest_amount': interest_amount,
            'total_payment': monthly_payment,
            'balance': balance
        })

        # Move to the next month
        payment_date += pd.Timedelta(days=30)
        payment_number += 1

    # Insert repayment details into the RepaymentSchedule table
    conn.execute(text("INSERT INTO repaymentschedule (loanid, paymentnumber, paymentdate, principalamount, interestamount, totalpayment, balance) VALUES :repschedule"), repschedule=[dict(zip(['loanid', 'paymentnumber', 'paymentdate', 'principalamount', 'interestamount', 'totalpayment', 'balance'], values)) for values in [list(row.values()) for row in [dict(**row) for row in repayment_schedule]]])

    conn.commit()

    return repayment_schedule
