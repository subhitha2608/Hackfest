Python
from config import engine
import pandas as pd

def calculate_credit_score(p_customer_id):
    # Step 1: Calculate the customer's total loan amount, total repayment, and outstanding balance
    query = text("""
        SELECT COALESCE(ROUND(SUM(loan_amount), 2), 0), 
               COALESCE(ROUND(SUM(repayment_amount), 2), 0), 
               COALESCE(ROUND(SUM(outstanding_balance), 2), 0)
        FROM loans
        WHERE loans.customer_id = :customer_id
    """)
    result = engine.execute(query, {"customer_id": p_customer_id}).fetchall()
    total_loan_amount, total_repayment, outstanding_loan_balance = result[0]

    # Step 2: Get the current credit card balance
    query = text("""
        SELECT COALESCE(ROUND(SUM(balance), 2), 0)
        FROM credit_cards
        WHERE credit_cards.customer_id = :customer_id
    """)
    result = engine.execute(query, {"customer_id": p_customer_id}).fetchall()
    credit_card_balance = result[0][0]

    # Step 3: Count the number of late payments
    query = text("""
        SELECT COUNT(*)
        FROM payments
        WHERE payments.customer_id = :customer_id AND status = 'Late'
    """)
    result = engine.execute(query, {"customer_id": p_customer_id}).fetchall()
    late_pay_count = result[0][0]

    # Step 4: Basic rule-based calculation of the credit score
    total_repayment_rate = 0
    if total_loan_amount > 0:
        total_repayment_rate = (total_repayment / total_loan_amount) * 0.4

    credit_utilization = 0
    if credit_card_balance > 0:
        credit_utilization = (1 - (credit_card_balance / 10000)) * 0.3

    credit_score = 0
    credit_score += 400
    if total_repayment_rate > 0:
        credit_score += total_repayment_rate
    credit_score += credit_utilization
    credit_score -= late_pay_count * 50

    credit_score = round(credit_score)
    if credit_score < 300:
        credit_score = 300
    elif credit_score > 850:
        credit_score = 850

    # Step 5: Update the customer’s credit score in the database
    query = text("""
        UPDATE customers
        SET credit_score = :credit_score
        WHERE customers.id = :customer_id
    """)
    engine.execute(query, {"customer_id": p_customer_id, "credit_score": credit_score})

    # Optionally, log the result or raise an alert for very low scores
    if credit_score < 500:
        query = text("""
            INSERT INTO credit_score_alerts (customer_id, credit_score, created_at)
            VALUES (:customer_id, :credit_score, NOW())
        """)
        engine.execute(query, {"customer_id": p_customer_id, "credit_score": credit_score})

    return credit_score
