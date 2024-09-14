
from config import engine
from sqlalchemy import text
import pandas as pd
import psycopg2

def transfer_funds(p_sender, p_receiver, p_amount):
    try:
        conn = engine.connect()
        log_config = logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        # Subtract the amount from the sender's account
        updateSenderQuery = text("UPDATE accounts SET balance = balance - :p_amount WHERE id = :p_sender")
        resultSender = conn.execute(updateSenderQuery, {"p_sender": p_sender, "p_amount": p_amount})
        logger.info("Updated sender's account balance: %s", resultSender)

        # Add the amount to the receiver's account
        updateReceiverQuery = text("UPDATE accounts SET balance = balance + :p_amount WHERE id = :p_receiver")
        resultReceiver = conn.execute(updateReceiverQuery, {"p_receiver": p_receiver, "p_amount": p_amount})
        logger.info("Updated receiver's account balance: %s", resultReceiver)

        conn.commit()
        logger.info("Transaction completed successfully!")

    except (psycopg2.Error, Exception) as e:
        logger.error("Error while transferring funds: %s", e)

    finally:
        conn.close()

    return None
