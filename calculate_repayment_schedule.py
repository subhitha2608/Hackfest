Python
from config import engine
from sqlalchemy import text
import pandas as pd

def calculate_repayment_schedule(loan_id):
    # Step 1: Retrieve loan details
    result = engine.execute(text("SELECT loanamount, interestrate, loanterm, startdate FROM loans WHERE loanid = :loan_id"), 
                            {"loan_id": loan_id})
    loan_amount, interest_rate, loan_term, start_date = result.fetchone()

    # Step 2: Convert annual interest rate to monthly interest rate
    monthly_interest_rate = interest_rate / 100 / 12

    # Step 3: Calculate fixed monthly payment using the amortization formula
    monthly_payment = (loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate)**(-loan_term))

    # Step 4: Initialize balance to the loan amount
    balance = loan_amount

    # Step 5: Initialize payment_date to the start date of the loan
    payment_date = start_date

    # Step 6: Loop through each month and calculate the repayment schedule
    repayment_schedule = []
    payment_number = 1
    while payment_number <= loan_term:
        # Step 6.1: Calculate interest for the current month
        interest_amount = balance * monthly_interest_rate

        # Step 6.2: Calculate principal for the current month
        principal_amount = monthly_payment - interest_amount

        # Step 6.3: Deduct principal from balance
        balance = balance - principal_amount

        # Step 6.4: Insert repayment details into the RepaymentSchedule table
        engine.execute(text("INSERT INTO repaymentschedule (loanid, paymentnumber, paymentdate, principalamount, interestamount, totalpayment, balance) VALUES (:loan_id, :payment_number, :payment_date, :principal_amount, :interest_amount, :monthly_payment, :balance)"), 
                       {"loan_id": loan_id, 
                        "payment_number": payment_number, 
                        "payment_date": payment_date, 
                        "principal_amount": principal_amount, 
                        "interest_amount": interest_amount, 
                        "monthly_payment": monthly_payment, 
                        "balance": balance})

        # Step 6.5: Move to the next month
        payment_date = pd.to_datetime(payment_date) + pd.DateOffset(months=1)
        payment_number += 1

    # Step 7: Return the repayment schedule
    return repayment_schedule

# Example usage:
repayment_schedule = calculate_repayment_schedule(1)
