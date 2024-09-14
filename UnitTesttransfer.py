
import unittest
from your_module import wallet_transfer

class TestWalletTransfer(unittest.TestCase):

    def test_transfer succeeds(self):
        # Mock the engine to return a successful result
        def mock_engine_execute(sql, params):
            if sql == text("""
                UPDATE accounts
                SET balance = balance - :p_amount
                WHERE id = :p_sender;
            """):
                return pd.DataFrame({'balance': [100 - 100]})
            elif sql == text("""
                UPDATE accounts
                SET balance = balance + :p_amount
                WHERE id = :p_receiver;
            """):
                return pd.DataFrame({'balance': [100 + 100]})
            else:
                raise ValueError("Invalid SQL")

        # Enable mocking for test
        original.execute = engine.execute
        engine.execute = mock_engine_execute

        # Test the function
        result = wallet_transfer(1, 2, 100)
        self.assertEqual(result, "Transfer successful")

        # Disable mocking
        engine.execute = original.execute

    def test_transfer fails(self):
        # Mock the engine to return an error
        def mock_engine_execute(sql, params):
            raise ValueError("Error")

        # Enable mocking for test
        original.execute = engine.execute
        engine.execute = mock_engine_execute

        # Test the function
        result = wallet_transfer(1, 2, 100)
        self.assertEqual(result, "Error")

        # Disable mocking
        engine.execute = original.execute

    def test_sender_id_not_found(self):
        # Mock the engine to return a successful result with a sender_id that does not exist
        def mock_engine_execute(sql, params):
            if sql == text("""
                UPDATE accounts
                SET balance = balance - :p_amount
                WHERE id = :p_sender;
            """):
                return pd.DataFrame({'balance': [100 - 100]})
            elif sql == text("""
                UPDATE accounts
                SET balance = balance + :p_amount
                WHERE id = :p_receiver;
            """):
                raise ValueError("Invalid sender_id")
            else:
                raise ValueError("Invalid SQL")

        # Enable mocking for test
        original.execute = engine.execute
        engine.execute = mock_engine_execute

        # Test the function
        result = wallet_transfer(3, 2, 100)
        self.assertEqual(result, "Invalid sender_id")

        # Disable mocking
        engine.execute = original.execute

    def test_sender_id_invalid_amount(self):
        # Mock the engine to return a successful result with an invalid amount
        def mock_engine_execute(sql, params):
            if sql == text("""
                UPDATE accounts
                SET balance = balance - :p_amount
                WHERE id = :p_sender;
            """):
                raise ValueError("Invalid amount")
            elif sql == text("""
                UPDATE accounts
                SET balance = balance + :p_amount
                WHERE id = :p_receiver;
            """):
                return pd.DataFrame({'balance': [100 + 100]})
            else:
                raise ValueError("Invalid SQL")

        # Enable mocking for test
        original.execute = engine.execute
        engine.execute = mock_engine_execute

        # Test the function
        result = wallet_transfer(1, 2, 1000)
        self.assertEqual(result, "Invalid amount")

        # Disable mocking
        engine.execute = original.execute

if __name__ == '__main__':
    unittest.main()
