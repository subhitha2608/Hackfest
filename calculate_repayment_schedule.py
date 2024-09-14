Python
from config import engine
from sqlalchemy import text
import pandas as pd
import psycopg2

def calculate_repayment_schedule(loan_id):
    conn = engine.connect()
    try:
        # Get loan details
        result = conn.execute(text("SELECT loanamount, interestrate, loanterm, startdate FROM loans WHERE loanid = :loan_id"), {"loan_id": loan_id})
        loan_amount, interest_rate, loan_term, start_date = result.fetchone()

        # Convert annual interest rate to monthly interest rate (divide by 12)
        monthly_interest_rate = interest_rate / 100 / 12

        # Calculate fixed monthly payment using the amortization formula
        monthly_payment = (loan_amount * monthly_interest_rate) / (1 - pow(1 + monthly_interest_rate, -loan_term))

        # Initialize balance to the loan amount
        balance = loan_amount

        # Initialize payment_date to the start date of the loan
        payment_date = start_date

        # Initialize payment_number to 1
        payment_number = 1

        while payment_number <= loan_term:
            # Calculate interest for the current month
            interest_amount = balance * monthly_interest_rate

            # Calculate principal for the current month
            principal_amount = monthly_payment - interest_amount

            # Deduct principal from balance
            balance = balance - principal_amount

            # Insert repayment details into the RepaymentSchedule table
            conn.execute(text("INSERT INTO repaymentschedule (loanid, paymentnumber, paymentdate, principalamount, interestamount, totalpayment, balance) VALUES (:loan_id, :payment_number, :payment_date, :principal_amount, :interest_amount, :monthly_payment, :balance)"),
                          {"loan_id": loan_id, "payment_number": payment_number, "payment_date": payment_date, "principal_amount": principal_amount, "interest_amount": interest_amount, "monthly_payment": monthly_payment, "balance": balance})

            # Move to the next month
            payment_date = payment_date + pd.Timedelta(days=30)
            payment_number = payment_number + 1

        conn.commit()

        # Return the final balance
        result = conn.execute(text("SELECT balance FROM repaymentschedule WHERE loanid = :loan_id AND paymentnumber = :loan_term"), {"loan_id": loan_id, "loan_term": loan_term})
        return result.fetchone()[0]

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn:
            conn.close()
