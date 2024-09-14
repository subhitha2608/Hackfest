
from config import engine
from sqlalchemy import text
import pandas as pd

def calculate_repayment_schedule(loan_id):
    # Execute a DDL command to create the RepaymentsSchedule table if it doesn't exist
    create_table_query = """
        CREATE TABLE IF NOT EXISTS repaymentschedule (
            id SERIAL PRIMARY KEY,
            loanid INTEGER,
            paymentnumber INTEGER,
            paymentdate DATE,
            principalamount DECIMAL(15, 2),
            interestamount DECIMAL(15, 2),
            totalpayment DECIMAL(15, 2),
            balance DECIMAL(15, 2)
        );
    """
    engine.execute(text(create_table_query))

    # Execute the stored procedure equivalent query
    query = """
        WITH loan_details AS (
            SELECT loanamount, interestrate, loanterm, startdate
            FROM loans
            WHERE loanid = :loan_id
        ),
        repayment_schedule AS (
            SELECT 
                1 AS payment_number,
                startdate AS payment_date,
                loanamount AS balance,
                0 AS interest_amount,
                loanamount AS principal_amount
            FROM loan_details
            UNION ALL
            SELECT 
                ps.payment_number + 1,
                ps.payment_date + INTERVAL '1 month',
                ps.balance - ps.principal_amount AS balance,
                ps.balance * (:monthly_interest_rate / 100 / 12) AS interest_amount,
                (:monthly_payment - ps.interest_amount) AS principal_amount
            FROM repayment_schedule AS ps
            WHERE ps.payment_number < :loan_term
        )
        INSERT INTO repaymentschedule (loanid, paymentnumber, paymentdate, principalamount, interestamount, totalpayment, balance)
        SELECT 
            :loan_id,
            payment_number,
            payment_date,
            principal_amount,
            interest_amount,
            :monthly_payment,
            balance
        FROM repayment_schedule;
    """
    connection = engine.connect()
    connection.execute(text(query), 
                       loan_id=loan_id, 
                       monthly_interest_rate=0, 
                       monthly_payment=0, 
                       loan_term=0)
    connection.commit()
