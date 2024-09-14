
from config import engine
from sqlalchemy import text
import pandas as pd
import psycopg2

def calculate_repayment_schedule(loan_id):
    with engine.connect() as conn:
        loan_amount = pd.read_sql_query(text("SELECT loanamount FROM loans WHERE loanid = :loan_id"), conn, params={'loan_id': loan_id}).iloc[0]['loanamount']
        interest_rate = pd.read_sql_query(text("SELECT interestrate FROM loans WHERE loanid = :loan_id"), conn, params={'loan_id': loan_id}).iloc[0]['interestrate']
        loan_term = pd.read_sql_query(text("SELECT loanterm FROM loans WHERE loanid = :loan_id"), conn, params={'loan_id': loan_id}).iloc[0]['loanterm']
        start_date = pd.read_sql_query(text("SELECT startdate FROM loans WHERE loanid = :loan_id"), conn, params={'loan_id': loan_id}).iloc[0]['startdate']
        
        monthly_interest_rate = interest_rate / 100 / 12
        monthly_payment = (loan_amount * monthly_interest_rate) / (1 - pow(1 + monthly_interest_rate, -loan_term))
        
        balance = loan_amount
        payment_date = start_date
        payment_number = 1
        
        repayments = []
        
        while payment_number <= loan_term:
            interest_amount = balance * monthly_interest_rate
            principal_amount = monthly_payment - interest_amount
            balance = balance - principal_amount
            
            conn.execute(text("""
                INSERT INTO repaymentschedule (loanid, paymentnumber, paymentdate, principalamount, interestamount, totalpayment, balance)
                VALUES (:loan_id, :payment_number, :payment_date, :principal_amount, :interest_amount, :monthly_payment, :balance)
            """), 
                         {'loan_id': loan_id, 
                          'payment_number': payment_number, 
                          'payment_date': payment_date, 
                          'principal_amount': principal_amount, 
                          'interest_amount': interest_amount, 
                          'monthly_payment': monthly_payment, 
                          'balance': balance})
            conn.commit()
            
            payment_date = payment_date + timedelta(days=30)
            payment_number += 1
        
        conn.close()
