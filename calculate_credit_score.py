
from config import engine
from sqlalchemy import text
import pandas as pd
import psycopg2

def calculate_credit_score(p_customer_id):
    # Step 1: Calculate the customer's total loan amount, total repayment, and outstanding balance
    total_loan_amount = round(sum(engine.execute(text("SELECT SUM(loan_amount) FROM loans WHERE customer_id = :p_customer_id"), p_customer_id=p_customer_id).fetchone()[0], 2) or 0, 2)
    total_repayment = round(sum(engine.execute(text("SELECT SUM(repayment_amount) FROM loans WHERE customer_id = :p_customer_id"), p_customer_id=p_customer_id).fetchone()[0], 2) or 0, 2)
    outstanding_loan_balance = round(sum(engine.execute(text("SELECT SUM(outstanding_balance) FROM loans WHERE customer_id = :p_customer_id"), p_customer_id=p_customer_id).fetchone()[0], 2) or 0, 2)

    # Step 2: Get the current credit card balance
    credit_card_balance = round(sum(engine.execute(text("SELECT SUM(balance) FROM credit_cards WHERE customer_id = :p_customer_id"), p_customer_id=p_customer_id).fetchone()[0], 2) or 0, 2)

    # Step 3: Count the number of late payments
    late_pay_count = engine.execute(text("SELECT COUNT(*) FROM payments WHERE customer_id = :p_customer_id AND status = 'Late'"), p_customer_id=p_customer_id).fetchone()[0]

    # Step 4: Basic rule-based calculation of the credit score
    v_credit_score = 0
    if total_loan_amount > 0:
        v_credit_score += round((total_repayment / total_loan_amount) * 400, 2)  # 40% weight for loan repayment
    else:
        v_credit_score += 400  # If no loans, give average score for this factor

    if credit_card_balance > 0:
        v_credit_score += round((1 - (credit_card_balance / 10000)) * 300, 2)  # 30% weight for credit card utilization
    else:
        v_credit_score += 300

    v_credit_score -= late_pay_count * 50  # Deduct 50 points for each late payment

    # Ensure the score stays within reasonable bounds (e.g., 300 to 850)
    if v_credit_score < 300:
        v_credit_score = 300
    elif v_credit_score > 850:
        v_credit_score = 850

    # Update the customer's credit score
    engine.execute(text("UPDATE customers SET credit_score = ROUND(:v_credit_score, 0) WHERE id = :p_customer_id"), p_customer_id=p_customer_id, v_credit_score=v_credit_score)

    # Optionally, log the result or raise an alert for very low scores
    if v_credit_score < 500:
        engine.execute(text("INSERT INTO credit_score_alerts (customer_id, credit_score, created_at) VALUES (:p_customer_id, ROUND(:v_credit_score, 0), NOW())"), p_customer_id=p_customer_id, v_credit_score=v_credit_score)

    return v_credit_score
