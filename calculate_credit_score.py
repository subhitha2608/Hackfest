
from sqlalchemy import create_engine, text
from config import engine
import pandas as pd

def calculate_credit_score(p_customer_id):
    # Step 1: Calculate the customer's total loan amount, total repayment, and outstanding balance
    query = text("""
        SELECT COALESCE(ROUND(SUM(loan_amount), 2), 0), 
               COALESCE(ROUND(SUM(repayment_amount), 2), 0), 
               COALESCE(ROUND(SUM(outstanding_balance), 2), 0)
        FROM loans
        WHERE loans.customer_id = :p_customer_id
    """)
    total_loan_amount, total_repayment, outstanding_loan_balance = engine.execute(query, p_customer_id=p_customer_id).fetchone()

    # Step 2: Get the current credit card balance
    query = text("""
        SELECT COALESce(ROUND(SUM(balance), 2), 0)
        FROM credit_cards
        WHERE credit_cards.customer_id = :p_customer_id
    """)
    credit_card_balance = engine.execute(query, p_customer_id=p_customer_id).fetchone()[0]

    # Step 3: Count the number of late payments
    query = text("""
        SELECT COUNT(*)
        FROM payments
        WHERE payments.customer_id = :p_customer_id AND status = 'Late'
    """)
    late_pay_count = engine.execute(query, p_customer_id=p_customer_id).fetchone()[0]

    # Step 4: Calculate the credit score
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

    credit_score = min(max(credit_score, 300), 850)

    # Step 5: Update the customer's credit score in the database
    query = text("""
        UPDATE customers
        SET credit_score = ROUND(:credit_score, 0)
        WHERE customers.id = :p_customer_id
    """)
    engine.execute(query, p_customer_id=p_customer_id, credit_score=credit_score)

    # Optionally, log the result or raise an alert for very low scores
    if credit_score < 500:
        query = text("""
            INSERT INTO credit_score_alerts (customer_id, credit_score, created_at)
            VALUES (:p_customer_id, ROUND(:credit_score, 0), NOW())
        """)
        engine.execute(query, p_customer_id=p_customer_id, credit_score=credit_score)

    return credit_score
