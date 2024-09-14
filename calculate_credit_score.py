
from config import engine
from sqlalchemy import text
import pandas as pd
import psycopg2

def calculate_credit_score(customer_id):
    conn = engine.connect()

    # Step 1: Calculate the customer's total loan amount, total repayment, and outstanding balance
    query1 = text("""
        SELECT COALESCE(ROUND(SUM(loan_amount), 2), 0), COALESCE(ROUND(SUM(repayment_amount), 2), 0), COALESCE(ROUND(SUM(outstanding_balance), 2), 0)
        FROM loans
        WHERE loans.customer_id = :customer_id
    """)
    result1 = conn.execute(query1, {'customer_id': customer_id})
    total_loan_amount, total_repayment, outstanding_loan_balance = result1.fetchone()

    # Step 2: Get the current credit card balance
    query2 = text("""
        SELECT COALESCE(ROUND(SUM(balance), 2), 0)
        FROM credit_cards
        WHERE credit_cards.customer_id = :customer_id
    """)
    result2 = conn.execute(query2, {'customer_id': customer_id})
    credit_card_balance, = result2.fetchone()

    # Step 3: Count the number of late payments
    query3 = text("""
        SELECT COUNT(*)
        FROM payments
        WHERE payments.customer_id = :customer_id AND status = 'Late'
    """)
    result3 = conn.execute(query3, {'customer_id': customer_id})
    late_pay_count, = result3.fetchone()

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

    # Ensure the score stays within reasonable bounds (e.g., 300 to 850)
    v_credit_score = max(300, min(v_credit_score, 850))

    # Update the customer's credit score
    query4 = text("""
        UPDATE customers
        SET credit_score = :credit_score
        WHERE customers.id = :customer_id
    """)
    conn.execute(query4, {'credit_score': round(v_credit_score, 0), 'customer_id': customer_id})
    conn.commit()

    # Optionally, log the result or raise an alert for very low scores
    if v_credit_score < 500:
        query5 = text("""
            INSERT INTO credit_score_alerts (customer_id, credit_score, created_at)
            VALUES (:customer_id, :credit_score, NOW())
        """)
        conn.execute(query5, {'customer_id': customer_id, 'credit_score': round(v_credit_score, 0)})
        conn.commit()

    conn.close()
    return round(v_credit_score, 0)
