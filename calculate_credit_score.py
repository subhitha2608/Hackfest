
from config import engine
from sqlalchemy import text
import pandas as pd
import psycopg2

def calculate_credit_score(customer_id):
    # Step 1: Calculate total loan amount, total repayment, and outstanding balance
    query = text("""
        SELECT COALESCE(ROUND(SUM(loan_amount), 2), 0), 
               COALESCE(ROUND(SUM(repayment_amount), 2), 0), 
               COALESCE(ROUND(SUM(outstanding_balance), 2), 0)
        FROM loans
        WHERE customer_id = :customer_id
    """)
    result = engine.connect().execute(query, {'customer_id': customer_id})
    total_loan_amount, total_repayment, outstanding_loan_balance = result.fetchone()

    # Step 2: Get current credit card balance
    query = text("""
        SELECT COALESCE(ROUND(SUM(balance), 2), 0)
        FROM credit_cards
        WHERE customer_id = :customer_id
    """)
    result = engine.connect().execute(query, {'customer_id': customer_id})
    credit_card_balance, = result.fetchone()

    # Step 3: Count late payments
    query = text("""
        SELECT COUNT(*)
        FROM payments
        WHERE customer_id = :customer_id AND status = 'Late'
    """)
    result = engine.connect().execute(query, {'customer_id': customer_id})
    late_pay_count, = result.fetchone()

    # Step 4: Basic rule-based calculation of credit score
    credit_score = 0
    if total_loan_amount > 0:
        credit_score += round((total_repayment / total_loan_amount) * 400, 2)
    else:
        credit_score += 400

    if credit_card_balance > 0:
        credit_score += round((1 - (credit_card_balance / 10000)) * 300, 2)
    else:
        credit_score += 300

    credit_score -= late_pay_count * 50

    # Ensure score stays within reasonable bounds
    credit_score = max(300, min(850, credit_score))

    # Update customer credit score
    query = text("""
        UPDATE customers
        SET credit_score = :credit_score
        WHERE id = :customer_id
    """)
    engine.connect().execute(query, {'credit_score': round(credit_score), 'customer_id': customer_id})
    engine.connect().commit()

    # Optionally, log result or raise alert for low scores
    if credit_score < 500:
        query = text("""
            INSERT INTO credit_score_alerts (customer_id, credit_score, created_at)
            VALUES (:customer_id, :credit_score, NOW())
        """)
        engine.connect().execute(query, {'customer_id': customer_id, 'credit_score': round(credit_score)})
        engine.connect().commit()

    return round(credit_score)
