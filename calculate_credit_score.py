
from config import engine
from sqlalchemy import text
import pandas as pd
import psycopg2

def calculate_credit_score(customer_id):
    # Step 1: Calculate the customer's total loan amount, total repayment, and outstanding balance
    query = text("""
        SELECT 
            COALESCE(ROUND(SUM(loan_amount), 2), 0) AS total_loan_amount,
            COALESCE(ROUND(SUM(repayment_amount), 2), 0) AS total_repayment,
            COALESCE(ROUND(SUM(outstanding_balance), 2), 0) AS outstanding_loan_balance
        FROM loans
        WHERE customer_id = :customer_id
    """)
    result = engine.execute(query, {"customer_id": customer_id})
    row = result.fetchone()
    total_loan_amount = row["total_loan_amount"]
    total_repayment = row["total_repayment"]
    outstanding_loan_balance = row["outstanding_loan_balance"]

    # Step 2: Get the current credit card balance
    query = text("""
        SELECT COALESCE(ROUND(SUM(balance), 2), 0) AS credit_card_balance
        FROM credit_cards
        WHERE customer_id = :customer_id
    """)
    result = engine.execute(query, {"customer_id": customer_id})
    row = result.fetchone()
    credit_card_balance = row["credit_card_balance"]

    # Step 3: Count the number of late payments
    query = text("""
        SELECT COUNT(*) AS late_pay_count
        FROM payments
        WHERE customer_id = :customer_id AND status = 'Late'
    """)
    result = engine.execute(query, {"customer_id": customer_id})
    row = result.fetchone()
    late_pay_count = row["late_pay_count"]

    # Step 4: Basic rule-based calculation of the credit score
    v_credit_score = 0
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

    # Update the customer's credit score
    query = text("""
        UPDATE customers
        SET credit_score = :credit_score
        WHERE id = :customer_id
    """)
    engine.execute(query, {"credit_score": round(v_credit_score, 0), "customer_id": customer_id})
    engine.commit()

    # Optionally, log the result or raise an alert for very low scores
    if v_credit_score < 500:
        query = text("""
            INSERT INTO credit_score_alerts (customer_id, credit_score, created_at)
            VALUES (:customer_id, :credit_score, NOW())
        """)
        engine.execute(query, {"customer_id": customer_id, "credit_score": round(v_credit_score, 0)})
        engine.commit()

    return round(v_credit_score, 0)  # Return the final credit score
