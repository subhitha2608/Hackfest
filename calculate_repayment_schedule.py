
from config import engine
from sqlalchemy import text
import pandas as pd

def calculate_repayment_schedule(loan_id):
    conn = engine.connect()
    
    # Get loan details
    loan_details = conn.execute(text("SELECT loanamount, interestrate, loanterm, startdate FROM loans WHERE loanid = :loan_id"), 
                                 {'loan_id': loan_id}).fetchall()
    loan_amount, interest_rate, loan_term, start_date = loan_details[0]
    
    # Convert annual interest rate to monthly interest rate
    monthly_interest_rate = interest_rate / 100 / 12
    
    # Calculate fixed monthly payment
    monthly_payment = (loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate)**(-loan_term))
    
    # Initialize balance and payment_date
    balance = loan_amount
    payment_date = start_date
    payment_number = 1

    while payment_number <= loan_term:
        # Calculate interest for the current month
        interest_amount = balance * monthly_interest_rate
        
        # Calculate principal for the current month
        principal_amount = monthly_payment - interest_amount
        
        # Deduct principal from balance
        balance -= principal_amount
        
        # Insert repayment details into the repaymentschedule table
        conn.execute(text("INSERT INTO repaymentschedule (loanid, paymentnumber, paymentdate, principalamount, interestamount, totalpayment, balance) "
                          "VALUES (:loan_id, :payment_number, :payment_date, :principal_amount, :interest_amount, :monthly_payment, :balance)"),
                      {'loan_id': loan_id, 
                       'payment_number': payment_number, 
                       'payment_date': payment_date, 
                       'principal_amount': principal_amount, 
                       'interest_amount': interest_amount, 
                       'monthly_payment': monthly_payment, 
                       'balance': balance})

        # Move to the next month
        payment_date += pd.Timedelta(days=30)
        payment_number += 1

    conn.commit()
    conn.close()
