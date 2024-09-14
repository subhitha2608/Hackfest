
from config import engine
import sqlalchemy as sa
import pandas as pd
import psycopg2

def calculate_credit_score(customer_id):
    # Create a connection object
    conn = engine.connect()

    # Step 1: Calculate total loan amount, total repayment, and outstanding balance
    query = sa.text("""
        SELECT COALESCE(ROUND(SUM(loan_amount), 2), 0), 
               COALESCE(ROUND(SUM(repayment_amount), 2), 0), 
               COALESCE(ROUND(SUM(outstanding_balance), 2), 0)
        FROM loans
        WHERE loans.customer_id = :customer_id
    """)
    result = conn.execute(query, {'customer_id': customer_id})
    total_loan_amount, total_repayment, outstanding_loan_balance = result.fetchone()

    # Step 2: Get current credit card balance
    query = sa.text("""
        SELECT COALESCE(ROUND(SUM(balance), 2), 0)
        FROM credit_cards
        WHERE credit_cards.customer_id = :customer_id
    """)
    result = conn.execute(query, {'customer_id': customer_id})
    credit_card_balance, = result.fetchone()

    # Step 3: Count late payments
    query = sa.text("""
        SELECT COUNT(*)
        FROM payments
        WHERE payments.customer_id = :customer_id AND status = 'Late'
    """)
    result = conn.execute(query, {'customer_id': customer_id})
    late_pay_count, = result.fetchone()

    # Step 4: Basic rule-based calculation of credit score
    v_credit_score = 0
    if total_loan_amount > 0:
        v_credit_score += round((total_repayment / total_loan_amount) * 400, 2)
    else:
        v_credit_score += 400

    if credit_card_balance > 0:
        v_credit_score += round((1 - (credit_card_balance / 10000)) * 300, 2)
    else:
        v_credit_score += 300

    v_credit_score -= (late_pay_count * 50)

    # Ensure the score stays within reasonable bounds
    if v_credit_score < 300:
        v_credit_score = 300
    elif v_credit_score > 850:
        v_credit_score = 850

    # Update customer credit score
    query = sa.text("""
        UPDATE customers
        SET credit_score = :credit_score
        WHERE customers.id = :customer_id
    """)
    conn.execute(query, {'credit_score': round(v_credit_score, 0), 'customer_id': customer_id})
    conn.commit()

    # Optionally, log the result or raise an alert for very low scores
    if v_credit_score < 500:
        query = sa.text("""
            INSERT INTO credit_score_alerts (customer_id, credit_score, created_at)
            VALUES (:customer_id, :credit_score, NOW())
        """)
        conn.execute(query, {'customer_id': customer_id, 'credit_score': round(v_credit_score, 0)})
        conn.commit()

    # Return the final credit score
    return round(v_credit_score, 0)
