
from sqlalchemy import text, create_engine
import pandas as pd
from config import engine
import psycopg2

def calculate_credit_score(p_customer_id):
    conn = engine.connect()
    
    total_loan_amount = 0
    total_repayment = 0
    outstanding_loan_balance = 0
    credit_card_balance = 0
    late_pay_count = 0
    v_credit_score = 0

    query1 = text("""
        SELECT COALESCE(ROUND(SUM(loan_amount), 2), 0), 
               COALESCE(ROUND(SUM(repayment_amount), 2), 0), 
               COALESCE(ROUND(SUM(outstanding_balance), 2), 0)
        FROM loans
        WHERE loans.customer_id = :p_customer_id
    """)
    result1 = conn.execute(query1, {"p_customer_id": p_customer_id})
    row1 = result1.fetchone()
    if row1:
        total_loan_amount, total_repayment, outstanding_loan_balance = row1

    query2 = text("""
        SELECT COALESCE(ROUND(SUM(balance), 2), 0)
        FROM credit_cards
        WHERE credit_cards.customer_id = :p_customer_id
    """)
    result2 = conn.execute(query2, {"p_customer_id": p_customer_id})
    row2 = result2.fetchone()
    if row2:
        credit_card_balance = row2[0]

    query3 = text("""
        SELECT COUNT(*)
        FROM payments
        WHERE payments.customer_id = :p_customer_id AND status = 'Late'
    """)
    result3 = conn.execute(query3, {"p_customer_id": p_customer_id})
    row3 = result3.fetchone()
    if row3:
        late_pay_count = row3[0]

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

    if v_credit_score < 300:
        v_credit_score = 300
    elif v_credit_score > 850:
        v_credit_score = 850

    query4 = text("""
        UPDATE customers
        SET credit_score = ROUND(:v_credit_score, 0)
        WHERE customers.id = :p_customer_id
    """)
    conn.execute(query4, {"p_customer_id": p_customer_id, "v_credit_score": v_credit_score})

    if v_credit_score < 500:
        query5 = text("""
            INSERT INTO credit_score_alerts (customer_id, credit_score, created_at)
            VALUES (:p_customer_id, ROUND(:v_credit_score, 0), NOW())
        """)
        conn.execute(query5, {"p_customer_id": p_customer_id, "v_credit_score": v_credit_score})

    conn.commit()
    conn.close()
    
    return v_credit_score
