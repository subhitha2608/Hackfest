Python
from config import engine
from sqlalchemy import text

def update_customer_credit_score(customer_id):
    # Step 1: Calculate the customer's total loan amount, total repayment, and outstanding balance
    total_loan_amount_data = text("""
        SELECT COALESCE(ROUND(SUM(loan_amount), 2), 0)
        FROM loans
        WHERE loans.customer_id = :customer_id
    """)
    total_repayment_data = text("""
        SELECT COALESCE(ROUND(SUM(repayment_amount), 2), 0)
        FROM loans
        WHERE loans.customer_id = :customer_id
    """)
    outstanding_loan_balance_data = text("""
        SELECT COALESCE(ROUND(SUM(outstanding_balance), 2), 0)
        FROM loans
        WHERE loans.customer_id = :customer_id
    """)
    total_loan_amount = engine.execute(total_loan_amount_data, customer_id=customer_id).scalar()
    total_repayment = engine.execute(total_repayment_data, customer_id=customer_id).scalar()
    outstanding_loan_balance = engine.execute(outstanding_loan_balance_data, customer_id=customer_id).scalar()

    # Step 2: Get the current credit card balance
    credit_card_balance_data = text("""
        SELECT COALESCE(ROUND(SUM(balance), 2), 0)
        FROM credit_cards
        WHERE credit_cards.customer_id = :customer_id
    """)
    credit_card_balance = engine.execute(credit_card_balance_data, customer_id=customer_id).scalar()

    # Step 3: Count the number of late payments
    late_pay_count_data = text("""
        SELECT COUNT(status)
        FROM payments
        WHERE payments.customer_id = :customer_id AND status = 'Late'
    """)
    late_pay_count = engine.execute(late_pay_count_data, customer_id=customer_id).scalar()

    # Step 4: Basic rule-based calculation of the credit score
    credit_score = 0
    if total_loan_amount > 0:
        credit_score += round((total_repayment / total_loan_amount) * 400, 2)  # 40% weight for loan repayment
    else:
        credit_score += 400  # If no loans, give average score for this factor

    if credit_card_balance > 0:
        credit_score += round((1 - (credit_card_balance / 10000)) * 300, 2)  # 30% weight for credit card utilization
    else:
        credit_score += 300

    credit_score -= late_pay_count * 50  # Deduct 50 points for each late payment

    # Ensure the score stays within reasonable bounds (e.g., 300 to 850)
    if credit_score < 300:
        credit_score = 300
    elif credit_score > 850:
        credit_score = 850

    # Step 5: Update the customer’s credit score in the database
    update_credit_score_data = text("""
        UPDATE customers
        SET credit_score = ROUND(:credit_score, 0)  # Round the final credit score to the nearest whole number
        WHERE customers.id = :customer_id
    """)
    engine.execute(update_credit_score_data, customer_id=customer_id, credit_score=credit_score)

    # Optionally, log the result or raise an alert for very low scores
    if credit_score < 500:
        log_credit_score_data = text("""
            INSERT INTO credit_score_alerts (customer_id, credit_score, created_at)
            VALUES (:customer_id, ROUND(:credit_score, 0), NOW())
        """)
        engine.execute(log_credit_score_data, customer_id=customer_id, credit_score=credit_score)

    return credit_score
