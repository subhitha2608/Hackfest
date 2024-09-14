Python
from config import engine
import pandas as pd

def calculate_credit_score(p_customer_id):
    total_loan_amount = 0
    total_repayment = 0
    outstanding_loan_balance = 0
    credit_card_balance = 0
    late_pay_count = 0
    v_credit_score = 0

    # Step 1: Calculate the customer's total loan amount, total repayment, and outstanding balance
    query = """
        SELECT COALESCE(ROUND(SUM(loan_amount), 2), 0), 
               COALESCE(ROUND(SUM(repayment_amount), 2), 0), 
               COALESCE(ROUND(SUM(outstanding_balance), 2), 0)
        FROM loans
        WHERE loans.customer_id = %s
    """
    result = engine.execute(text(query), (p_customer_id,)).fetchone()
    if result:
        total_loan_amount, total_repayment, outstanding_loan_balance = map(float, result)

    # Step 2: Get the current credit card balance
    query = """
        SELECT COALESCE(ROUND(SUM(balance), 2), 0)
        FROM credit_cards
        WHERE credit_cards.customer_id = %s
    """
    result = engine.execute(text(query), (p_customer_id,)).fetchone()
    if result:
        credit_card_balance = float(result[0])

    # Step 3: Count the number of late payments
    query = """
        SELECT COUNT(*)
        FROM payments
        WHERE payments.customer_id = %s AND status = 'Late'
    """
    result = engine.execute(text(query), (p_customer_id,)).fetchone()
    if result:
        late_pay_count = int(result[0])

    # Credit score calculation
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

    # Step 5: Update the customer’s credit score in the database
    query = """
        UPDATE customers
        SET credit_score = ROUND(%s, 0)
        WHERE customers.id = %s
    """
    engine.execute(text(query), (v_credit_score, p_customer_id))
    engine.commit()

    # Optionally, log the result or raise an alert for very low scores
    if v_credit_score < 500:
        query = """
            INSERT INTO credit_score_alerts (customer_id, credit_score, created_at)
            VALUES (%s, ROUND(%s, 0), NOW())
        """
        engine.execute(text(query), (p_customer_id, v_credit_score))
        engine.commit()
