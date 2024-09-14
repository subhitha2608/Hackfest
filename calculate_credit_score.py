Python
import pandas as pd
from sqlalchemy import text
import psycopg2
from config import engine

def calculate_credit_score(p_customer_id):
    conn = engine.connect()

    total_loan_amount = 0
    total_repayment = 0
    outstanding_loan_balance = 0
    credit_card_balance = 0
    late_pay_count = 0
    v_credit_score = 0

    # Step 1: Calculate the customer's total loan amount, total repayment, and outstanding balance
    result = conn.execute(text("SELECT COALESCE(ROUND(SUM(loan_amount), 2), 0) FROM loans WHERE loans.customer_id = :p_customer_id"),
                          {"p_customer_id": p_customer_id})
    if result.rowcount > 0:
        total_loan_amount = result.fetchone()[0]

    result = conn.execute(text("SELECT COALESCE(ROUND(SUM(repayment_amount), 2), 0) FROM payments WHERE payments.customer_id = :p_customer_id"),
                          {"p_customer_id": p_customer_id})
    if result.rowcount > 0:
        total_repayment = result.fetchone()[0]

    result = conn.execute(text("SELECT COALESCE(ROUND(SUM(outstanding_balance), 2), 0) FROM loans WHERE loans.customer_id = :p_customer_id"),
                          {"p_customer_id": p_customer_id})
    if result.rowcount > 0:
        outstanding_loan_balance = result.fetchone()[0]

    # Step 2: Get the current credit card balance
    result = conn.execute(text("SELECT COALESCE(ROUND(SUM(balance), 2), 0) FROM credit_cards WHERE credit_cards.customer_id = :p_customer_id"),
                          {"p_customer_id": p_customer_id})
    if result.rowcount > 0:
        credit_card_balance = result.fetchone()[0]

    # Step 3: Count the number of late payments
    result = conn.execute(text("SELECT COUNT(*) FROM payments WHERE payments.customer_id = :p_customer_id AND status = 'Late'"),
                          {"p_customer_id": p_customer_id})
    if result.rowcount > 0:
        late_pay_count = result.fetchone()[0]

    # Step 4: Basic rule-based calculation of the credit score
    if total_loan_amount > 0:
        v_credit_score += round((total_repayment / total_loan_amount) * 400, 2)  # 40% weight for loan repayment
    else:
        v_credit_score += 400  # If no loans, give average score for this factor

    if credit_card_balance > 0:
        v_credit_score += round((1 - (credit_card_balance / 10000)) * 300, 2)  # 30% weight for credit card utilization
    else:
        v_credit_score += 300

    v_credit_score -= late_pay_count * 50  # Deduct 50 points for each late payment

    # Ensure the score stays within reasonable bounds (e.g., 300 to 850)
    if v_credit_score < 300:
        v_credit_score = 300
    elif v_credit_score > 850:
        v_credit_score = 850

    # Step 5: Update the customer’s credit score in the database
    conn.execute(text("UPDATE customers SET credit_score = ROUND(:v_credit_score, 0) WHERE customers.id = :p_customer_id"),
                 {"p_customer_id": p_customer_id, "v_credit_score": v_credit_score})

    # Optionally, log the result or raise an alert for very low scores
    if v_credit_score < 500:
        conn.execute(text("INSERT INTO credit_score_alerts (customer_id, credit_score, created_at) VALUES (:p_customer_id, ROUND(:v_credit_score, 0), NOW())"),
                     {"p_customer_id": p_customer_id, "v_credit_score": v_credit_score})

    conn.commit()
    conn.close()

    return v_credit_score
