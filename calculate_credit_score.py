
from sqlalchemy import create_engine, text
from sqlalchemy.engine import connection
import pandas as pd
from config import engine

def update_credit_score(p_customer_id):
    with engine.connect() as conn:
        with conn.begin() as transaction:
            total_loan_amount = 0
            total_repayment = 0
            outstanding_loan_balance = 0
            credit_card_balance = 0
            late_pay_count = 0
            v_credit_score = 0

            # Step 1: Calculate the customer's total loan amount, total repayment, and outstanding balance
            result = conn.execute(text("SELECT COALESCE(ROUND(SUM(loan_amount), 2), 0) FROM loans WHERE loans.customer_id = :customer_id"), {"customer_id": p_customer_id})
            row = result.fetchone()
            total_loan_amount = row[0]
            result = conn.execute(text("SELECT COALESCE(ROUND(SUM(repayment_amount), 2), 0) FROM loans WHERE loans.customer_id = :customer_id"), {"customer_id": p_customer_id})
            row = result.fetchone()
            total_repayment = row[0]
            result = conn.execute(text("SELECT COALESCE(ROUND(SUM(outstanding_balance), 2), 0) FROM loans WHERE loans.customer_id = :customer_id"), {"customer_id": p_customer_id})
            row = result.fetchone()
            outstanding_loan_balance = row[0]

            # Step 2: Get the current credit card balance
            result = conn.execute(text("SELECT COALESCE(ROUND(SUM(balance), 2), 0) FROM credit_cards WHERE credit_cards.customer_id = :customer_id"), {"customer_id": p_customer_id})
            row = result.fetchone()
            credit_card_balance = row[0]

            # Step 3: Count the number of late payments
            result = conn.execute(text("SELECT COUNT(*) FROM payments WHERE payments.customer_id = :customer_id AND status = 'Late'"), {"customer_id": p_customer_id})
            row = result.fetchone()
            late_pay_count = row[0]

            # Step 4: Basic rule-based calculation of the credit score
            # Factor 1: Repayment rate (higher is better)
            if total_loan_amount > 0:
                v_credit_score += round((total_repayment / total_loan_amount) * 400, 2)  # 40% weight for loan repayment
            else:
                v_credit_score += 400  # If no loans, give average score for this factor

            # Factor 2: Credit utilization (lower is better)
            if credit_card_balance > 0:
                v_credit_score += round((1 - (credit_card_balance / 10000)) * 300, 2)  # 30% weight for credit card utilization
            else:
                v_credit_score += 300

            # Factor 3: Late payments (fewer is better)
            v_credit_score -= late_pay_count * 50  # Deduct 50 points for each late payment

            # Ensure the score stays within reasonable bounds (e.g., 300 to 850)
            if v_credit_score < 300:
                v_credit_score = 300
            elif v_credit_score > 850:
                v_credit_score = 850

            # Step 5: Update the customer’s credit score in the database
            conn.execute(text("UPDATE customers SET credit_score = ROUND(:v_credit_score, 0) WHERE customers.id = :customer_id"), {"v_credit_score": v_credit_score, "customer_id": p_customer_id})

            # Optionally, log the result or raise an alert for very low scores
            if v_credit_score < 500:
                conn.execute(text("INSERT INTO credit_score_alerts (customer_id, credit_score, created_at) VALUES (:customer_id, ROUND(:v_credit_score, 0), NOW())"), {"customer_id": p_customer_id, "v_credit_score": v_credit_score})
            transaction.commit()
