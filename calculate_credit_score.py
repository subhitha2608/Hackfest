
from config import engine
from sqlalchemy import text
import pandas as pd
import psycopg2

def calculate_credit_score(p_customer_id):
    conn = engine.connect()

    # Step 1: Calculate the customer's total loan amount, total repayment, and outstanding balance
    total_loan_amount_query = text("""
        SELECT COALESCE(ROUND(SUM(loan_amount), 2), 0)
        FROM loans
        WHERE loans.customer_id = :customer_id
    """)
    total_loan_amount = conn.execute(total_loan_amount_query, {"customer_id": p_customer_id}).scalar()
    
    total_repayment_query = text("""
        SELECT COALESCE(ROUND(SUM(repayment_amount), 2), 0)
        FROM loans
        WHERE loans.customer_id = :customer_id
    """)
    total_repayment = conn.execute(total_repayment_query, {"customer_id": p_customer_id}).scalar()

    outstanding_loan_balance_query = text("""
        SELECT COALESCE(ROUND(SUM(outstanding_balance), 2), 0)
        FROM loans
        WHERE loans.customer_id = :customer_id
    """)
    outstanding_loan_balance = conn.execute(outstanding_loan_balance_query, {"customer_id": p_customer_id}).scalar()

    # Step 2: Get the current credit card balance
    credit_card_balance_query = text("""
        SELECT COALESCE(ROUND(SUM(balance), 2), 0)
        FROM credit_cards
        WHERE credit_cards.customer_id = :customer_id
    """)
    credit_card_balance = conn.execute(credit_card_balance_query, {"customer_id": p_customer_id}).scalar()

    # Step 3: Count the number of late payments
    late_pay_count_query = text("""
        SELECT COUNT(*)
        FROM payments
        WHERE payments.customer_id = :customer_id AND status = 'Late'
    """)
    late_pay_count = conn.execute(late_pay_count_query, {"customer_id": p_customer_id}).scalar()

    # Step 4: Calculate the credit score
    v_credit_score = 0
    if total_loan_amount > 0:
        v_credit_score += round((total_repayment / total_loan_amount) * 400, 2)  # 40% weight for loan repayment
    
    if credit_card_balance > 0:
        v_credit_score += round((1 - (credit_card_balance / 10000)) * 300, 2)  # 30% weight for credit card utilization
    
    v_credit_score -= late_pay_count * 50  # Deduct 50 points for each late payment

    v_credit_score = max(300, min(v_credit_score, 850))  # Ensure the score stays within reasonable bounds

    # Step 5: Update the customer's credit score
    update_query = text("""
        UPDATE customers
        SET credit_score = ROUND(:v_credit_score, 0)
        WHERE customers.id = :customer_id
    """)
    conn.execute(update_query, {"customer_id": p_customer_id, "v_credit_score": v_credit_score})

    # Step 6: Log the result or raise an alert for very low scores
    if v_credit_score < 500:
        insert_query = text("""
            INSERT INTO credit_score_alerts (customer_id, credit_score, created_at)
            VALUES (:customer_id, ROUND(:v_credit_score, 0), NOW())
        """)
        conn.execute(insert_query, {"customer_id": p_customer_id, "v_credit_score": v_credit_score})

    conn.commit()
    conn.close()

    return
