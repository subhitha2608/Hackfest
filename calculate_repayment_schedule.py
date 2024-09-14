Python
from config import engine
import pandas as pd

def calculate_repayment_schedule(loan_id):
    conn = engine.connect()
    
    # Get loan details
    loan_details_query = text("""
    SELECT loanamount, interestrate, loanterm, startdate
    FROM loans
    WHERE loanid = :loan_id
    """)
    loan_details = conn.execute(loan_details_query, {'loan_id': loan_id}).fetchone()
    loan_amount, interest_rate, loan_term, start_date = loan_details

    # Convert annual interest rate to monthly interest rate
    monthly_interest_rate = (interest_rate / 100 / 12)

    # Calculate fixed monthly payment
    monthly_payment = (loan_amount * monthly_interest_rate) / (1 - pow(1 + monthly_interest_rate, -loan_term))

    # Initialize balance and payment_date
    balance = loan_amount
    payment_date = start_date

    # Initialize payment_number
    payment_number = 1

    # Create a list to store repayment details
    repayment_schedule = []
    while payment_number <= loan_term:
        # Calculate interest and principal for the current month
        interest_amount = balance * monthly_interest_rate
        principal_amount = monthly_payment - interest_amount

        # Deduct principal from balance
        balance -= principal_amount

        # Add repayment details to the list
        repayment_schedule.append({
            'loanid': loan_id,
            'paymentnumber': payment_number,
            'paymentdate': payment_date.strftime('%Y-%m-%d'),
            'principalamount': principal_amount,
            'interestamount': interest_amount,
            'totalpayment': monthly_payment,
            'balance': balance
        })

        # Move to the next month
        payment_date += pd.Timedelta(days=30)
        payment_number += 1

    # Insert repayment details into the RepaymentSchedule table
    insert_query = text("""
    INSERT INTO repaymentschedule (loanid, paymentnumber, paymentdate, principalamount, interestamount, totalpayment, balance)
    VALUES (:loan_id, :payment_number, :payment_date, :principal_amount, :interest_amount, :monthly_payment, :balance)
    """)
    conn.execute(insert_query, {
        'loan_id': loan_id,
        'payment_number': payment_number,
        'payment_date': payment_date.strftime('%Y-%m-%d'),
        'principal_amount': principal_amount,
        'interest_amount': interest_amount,
        'monthly_payment': monthly_payment,
        'balance': balance
    })
    conn.commit()

    return repayment_schedule
