
from config import engine
from sqlalchemy.sql import text
import pandas as pd

def update_credit_score(p_customer_id):
    conn = engine.connect()

    # Step 1: Calculate the customer's total loan amount, total repayment, and outstanding balance
    total_loan_amount = pd.read_sql(text("SELECT ROUND(SUM(loan_amount), 2) AS total_loan_amount FROM loans WHERE loans.customer_id = :customer_id"), conn, parameters={'customer_id': p_customer_id}).iloc[0]['total_loan_amount'] if total_loan_amount > 0 else 0
    total_repayment = pd.read_sql(text("SELECT ROUND(SUM(repayment_amount), 2) AS total_repayment FROM payments WHERE payments.customer_id = :customer_id"), conn, parameters={'customer_id': p_customer_id}).iloc[0]['total_repayment'] if total_repayment > 0 else 0
    outstanding_loan_balance = pd.read_sql(text("SELECT ROUND(SUM(outstanding_balance), 2) AS outstanding_loan_balance FROM loans WHERE loans.customer_id = :customer_id"), conn, parameters={'customer_id': p_customer_id}).iloc[0]['outstanding_loan_balance'] if outstanding_loan_balance > 0 else 0

    # Step 2: Get the current credit card balance
    credit_card_balance = pd.read_sql(text("SELECT ROUND(SUM(balance), 2) AS credit_card_balance FROM credit_cards WHERE credit_cards.customer_id = :customer_id"), conn, parameters={'customer_id': p_customer_id}).iloc[0]['credit_card_balance'] if credit_card_balance > 0 else 0

    # Step 3: Count the number of late payments
    late_pay_count = pd.read_sql(text("SELECT COUNT(*) AS late_pay_count FROM payments WHERE payments.customer_id = :customer_id AND status = 'Late'"), conn, parameters={'customer_id': p_customer_id}).iloc[0]['late_pay_count']

    # Step 4: Basic rule-based calculation of the credit score
    v_credit_score = 0
    if total_loan_amount > 0:
        v_credit_score += round((total_repayment / total_loan_amount) * 400, 2)
    else:
        v_credit_score += 400

    if credit_card_balance > 0:
        v_credit_score += round((1 - (credit_card_balance / 10000)) * 300, 2)
    else:
        v_credit_score += 300

    v_credit_score -= late_pay_count * 50

    # Ensure the score stays within reasonable bounds
    if v_credit_score < 300:
        v_credit_score = 300
    elif v_credit_score > 850:
        v_credit_score = 850

    # Step 5: Update the customer’s credit score in the database
    conn.execute(text("UPDATE customers SET credit_score = ROUND(:v_credit_score, 0) WHERE customers.id = :customer_id"), {'customer_id': p_customer_id, 'v_credit_score': v_credit_score})

    # Optionally, log the result or raise an alert for very low scores
    if v_credit_score < 500:
        conn.execute(text("INSERT INTO credit_score_alerts (customer_id, credit_score, created_at) VALUES (:customer_id, ROUND(:v_credit_score, 0), NOW())"), {'customer_id': p_customer_id, 'v_credit_score': v_credit_score})

    conn.commit()
    conn.close()
