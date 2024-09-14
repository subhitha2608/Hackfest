
from config import engine
from sqlalchemy import text
import pandas
import psycopg2

def calculate_credit_score(customer_id):
    # Step 1: Calculate the customer's total loan amount, total repayment, and outstanding balance
    query = text("""
        SELECT COALESCE(ROUND(SUM(loan_amount), 2), 0), 
               COALESCE(ROUND(SUM(repayment_amount), 2), 0), 
               COALESCE(ROUND(SUM(outstanding_balance), 2), 0)
        FROM loans
        WHERE loans.customer_id = :customer_id
    """)
    result = engine.execute(query, {'customer_id': customer_id})
    total_loan_amount, total_repayment, outstanding_loan_balance = result.fetchone()

    # Step 2: Get the current credit card balance
    query = text("""
        SELECT COALESCE(ROUND(SUM(balance), 2), 0)
        FROM credit_cards
        WHERE credit_cards.customer_id = :customer_id
    """)
    result = engine.execute(query, {'customer_id': customer_id})
    credit_card_balance, = result.fetchone()

    # Step 3: Count the number of late payments
    query = text("""
        SELECT COUNT(*)
        FROM payments
        WHERE payments.customer_id = :customer_id AND status = 'Late'
    """)
    result = engine.execute(query, {'customer_id': customer_id})
    late_pay_count, = result.fetchone()

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

    v_credit_score -= (late_pay_count * 50)

    # Ensure the score stays within reasonable bounds (e.g., 300 to 850)
    if v_credit_score < 300:
        v_credit_score = 300
    elif v_credit_score > 850:
        v_credit_score = 850

    # Update the customer's credit score
    query = text("""
        UPDATE customers
        SET credit_score = :credit_score
        WHERE customers.id = :customer_id
    """)
    engine.execute(query, {'credit_score': round(v_credit_score, 0), 'customer_id': customer_id})
    conn = engine.raw_connection()
    conn.commit()

    # Optionally, log the result or raise an alert for very low scores
    if v_credit_score < 500:
        query = text("""
            INSERT INTO credit_score_alerts (customer_id, credit_score, created_at)
            VALUES (:customer_id, :credit_score, NOW())
        """)
        engine.execute(query, {'customer_id': customer_id, 'credit_score': round(v_credit_score, 0)})
        conn.commit()

    return v_credit_score
