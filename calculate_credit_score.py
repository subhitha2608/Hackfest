
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
    result = engine.execute(query, {"p_customer_id": p_customer_id}).fetchone()
    total_loan_amount, total_repayment, outstanding_loan_balance = result

    # Step 2: Get the current credit card balance
    query = text("""
        SELECT COALESCE(ROUND(SUM(balance), 2), 0)
        FROM credit_cards
        WHERE credit_cards.customer_id = :p_customer_id
    """)
    result = engine.execute(query, {"p_customer_id": p_customer_id}).fetchone()
    credit_card_balance = result[0]

    # Step 3: Count the number of late payments
    query = text("""
        SELECT COUNT(*) as late_pay_count
        FROM payments
        WHERE payments.customer_id = :p_customer_id AND status = 'Late'
    """)
    result = engine.execute(query, {"p_customer_id": p_customer_id}).fetchone()
    late_pay_count = result[0]

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
    query = text("""
        UPDATE customers
        SET credit_score = ROUND(:v_credit_score, 0)
        WHERE customers.id = :p_customer_id
    """)
    engine.execute(query, {"p_customer_id": p_customer_id, "v_credit_score": v_credit_score})

    # Optionally, log the result or raise an alert for very low scores
    if v_credit_score < 500:
        query = text("""
            INSERT INTO credit_score_alerts (customer_id, credit_score, created_at)
            VALUES (:p_customer_id, ROUND(:v_credit_score, 0), NOW())
        """)
        engine.execute(query, {"p_customer_id": p_customer_id, "v_credit_score": v_credit_score})

    return v_credit_score
