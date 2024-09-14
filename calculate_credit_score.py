
from config import engine
from sqlalchemy import text
import pandas as pd
import psycopg2

def calculate_credit_score(p_customer_id):
    # Query to calculate total loan amount, total repayment, and outstanding balance
    query = text("""
        SELECT COALESCE(ROUND(SUM(loan_amount), 2), 0), 
               COALESCE(ROUND(SUM(repayment_amount), 2), 0), 
               COALESCE(ROUND(SUM(outstanding_balance), 2), 0)
        FROM loans
        WHERE loans.customer_id = :p_customer_id
    """)
    result = engine.execute(query, p_customer_id=p_customer_id).fetchone()
    total_loan_amount, total_repayment, outstanding_loan_balance = result

    # Query to get current credit card balance
    query = text("""
        SELECT COALESCE(ROUND(SUM(balance), 2), 0)
        FROM credit_cards
        WHERE credit_cards.customer_id = :p_customer_id
    """)
    result = engine.execute(query, p_customer_id=p_customer_id).fetchone()
    credit_card_balance = result[0]

    # Query to count number of late payments
    query = text("""
        SELECT COUNT(*)
        FROM payments
        WHERE payments.customer_id = :p_customer_id AND status = 'Late'
    """)
    result = engine.execute(query, p_customer_id=p_customer_id).fetchone()
    late_pay_count = result[0]

    # Calculate credit score
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

    # Ensure score stays within reasonable bounds
    if v_credit_score < 300:
        v_credit_score = 300
    elif v_credit_score > 850:
        v_credit_score = 850

    # Update customer's credit score in the database
    query = text("""
        UPDATE customers
        SET credit_score = ROUND(:v_credit_score, 0)
        WHERE customers.id = :p_customer_id
    """)
    engine.execute(query, p_customer_id=p_customer_id, v_credit_score=v_credit_score)

    # Optionally log the result or raise an alert for very low scores
    if v_credit_score < 500:
        query = text("""
            INSERT INTO credit_score_alerts (customer_id, credit_score, created_at)
            VALUES (:p_customer_id, ROUND(:v_credit_score, 0), NOW())
        """)
        engine.execute(query, p_customer_id=p_customer_id, v_credit_score=v_credit_score)
