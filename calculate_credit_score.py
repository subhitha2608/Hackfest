
from config import engine
from sqlalchemy import text
import pandas as pd

def calculate_credit_score(p_customer_id):
    # Step 1: Calculate total loan amount and repayment
    query = text("""
        SELECT COALESCE(ROUND(SUM(loan_amount), 2), 0) AS total_loan_amount,
               COALESCE(ROUND(SUM(repayment_amount), 2), 0) AS total_repayment,
               COALESCE(ROUND(SUM(outstanding_balance), 2), 0) AS outstanding_loan_balance
        FROM loans
        WHERE loans.customer_id = :customer_id
    """)
    result = engine.execute(query, customer_id=p_customer_id)
    total_loan_amount = result.fetchone()[0]
    total_repayment = result.fetchone()[1]
    outstanding_loan_balance = result.fetchone()[2]

    # Step 2: Get credit card balance
    query = text("""
        SELECT COALESCE(ROUND(SUM(balance), 2), 0) AS credit_card_balance
        FROM credit_cards
        WHERE credit_cards.customer_id = :customer_id
    """)
    result = engine.execute(query, customer_id=p_customer_id)
    credit_card_balance = result.fetchone()[0]

    # Step 3: Count late payments
    query = text("""
        SELECT COUNT(*)
        FROM payments
        WHERE payments.customer_id = :customer_id AND status = 'Late'
    """)
    result = engine.execute(query, customer_id=p_customer_id)
    late_pay_count = result.fetchone()[0]

    # Step 4: Calculate credit score
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

    # Ensure the score stays within reasonable bounds
    if credit_score < 300:
        credit_score = 300
    elif credit_score > 850:
        credit_score = 850

    # Step 5: Update customer credit score
    query = text("""
        UPDATE customers
        SET credit_score = ROUND(:credit_score, 0)
        WHERE customers.id = :customer_id
    """)
    engine.execute(query, customer_id=p_customer_id, credit_score=credit_score)

    # Step 6: Log credit score alerts
    if credit_score < 500:
        query = text("""
            INSERT INTO credit_score_alerts (customer_id, credit_score, created_at)
            VALUES (:customer_id, ROUND(:credit_score, 0), NOW())
        """)
        engine.execute(query, customer_id=p_customer_id, credit_score=credit_score)

    return credit_score
