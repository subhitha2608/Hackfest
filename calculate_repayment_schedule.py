
from config import engine
from sqlalchemy import text
import pandas as pd
import psycopg2

defloan_repayment_schedule(loan_id):
    # Select loan details from loans table
    result = engine.execute(text("SELECT loanamount, interestrate, loanterm, startdate "
                                "FROM loans WHERE loanid = :loan_id"), 
                            {"loan_id": loan_id})
    loan_amount, interest_rate, loan_term, start_date = result.fetchone()

    # Convert annual interest rate to monthly interest rate
    monthly_interest_rate = interest_rate / 100 / 12

    # Calculate fixed monthly payment
    monthly_payment = (loan_amount * monthly_interest_rate) / (1 - pow((1 + monthly_interest_rate), -loan_term))

    # Initialize balance to the loan amount
    balance = loan_amount

    # Initialize payment_date to the start date of the loan
    payment_date = start_date

    # Loop through each month and calculate the repayment schedule
    payment_numbers = []
    payment_dates = []
    principal_amounts = []
    interest_amounts = []
    balances = []
    total_payments = []
    payment_numbers.append(1)
    payment_dates.append(payment_date)
    balance_copy = loan_amount
    for payment_number in range(1, loan_term + 1):
        # Calculate interest for the current month
        interest_amount = balance_copy * monthly_interest_rate

        # Calculate principal for the current month
        principal_amount = monthly_payment - interest_amount

        # Deduct principal from balance
        balance_copy -= principal_amount

        # Insert repayment details into the RepaymentSchedule table
        conn = engine.connect()
        conn.execute(text("INSERT INTO repaymentschedule (loanid, paymentnumber, paymentdate, principalamount, interestamount, totalpayment, balance) "
                          "VALUES (:loan_id, :payment_number, :payment_date, :principal_amount, :interest_amount, :monthly_payment, :balance)"),
                     {"loan_id": loan_id, "payment_number": payment_number, "payment_date": payment_date, "principal_amount": principal_amount,
                      "interest_amount": interest_amount, "monthly_payment": monthly_payment, "balance": balance_copy})
        conn.commit()
        conn.close()

        payment_dates.append(payment_date)
        principal_amounts.append(principal_amount)
        interest_amounts.append(interest_amount)
        balances.append(balance_copy)
        total_payments.append(monthly_payment)

    # Convert records to pandas DataFrame
    df = pd.DataFrame({
        "Payment Number": payment_numbers,
        "Payment Date": payment_dates,
        "Principal Amount": principal_amounts,
        "Interest Amount": interest_amounts,
        "Total Payment": total_payments,
        "Balance": balances
    })

    return df
