
from config import engine
from sqlalchemy import text, create_engine
import pandas as pd
import psycopg2

def calculate_repayment_schedule(loan_id):
    # Connect to the database
    conn = engine.connect()
    
    # Get loan details
    query = text("""
        SELECT loanamount, interestrate, loanterm, startdate
        FROM loans
        WHERE loanid = :loan_id
    """)
    result = conn.execute(query, loan_id=loan_id)
    loan_amount, interest_rate, loan_term, start_date = result.fetchone()
    
    # Convert annual interest rate to monthly interest rate
    monthly_interest_rate = interest_rate / 100 / 12
    
    # Calculate fixed monthly payment
    monthly_payment = (loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate)**(-loan_term))
    
    # Initialize balance to the loan amount
    balance = loan_amount
    
    # Initialize payment date to the start date of the loan
    payment_date = start_date
    
    # Loop through each month and calculate the repayment schedule
    payment_number = 1
    while payment_number <= loan_term:
        # Calculate interest for the current month
        interest_amount = balance * monthly_interest_rate
        
        # Calculate principal for the current month
        principal_amount = monthly_payment - interest_amount
        
        # Deduct principal from balance
        balance -= principal_amount
        
        # Insert repayment details into the RepaymentSchedule table
        query = text("""
            INSERT INTO repaymentschedule (loanid, paymentnumber, paymentdate, principalamount, interestamount, totalpayment, balance)
            VALUES (:loan_id, :payment_number, :payment_date, :principal_amount, :interest_amount, :monthly_payment, :balance)
        """)
        conn.execute(query, loan_id=loan_id, payment_number=payment_number, payment_date=payment_date, principal_amount=principal_amount, interest_amount=interest_amount, monthly_payment=monthly_payment, balance=balance)
        
        # Move to the next month
        payment_date += pd.Timedelta(days=30)
        payment_number += 1
    
    # Commit changes
    conn.commit()
    
    # Return the final balance
    return balance
