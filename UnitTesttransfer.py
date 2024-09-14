
import unittest
from unittest.mock import Mock
from your_file import transfermoney, create_table, get_balance

class TestFunction(unittest.TestCase):

    def setUp(self):
        self.engine_mock = Mock()
        self.engine_mock.connect.return_value = self.connection_mock = Mock()
        self.connection_mock.execute.return_value = Mock()
        self.connection_mock(commit).return_value = None

    def test_create_table(self):
        create_table()
        self.engine_mock.connect.assert_called_once()
        self.engine_mock.execute.assert_called_once_with(text("CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, balance INTEGER)"))
        self.connection_mock.commit.assert_called_once()

    def test_transfermoney_no_account(self):
        with self.assertRaises RegisterrionError:
            transfermoney(1, 2, 100)

    def test_transfermoney_invalid_amount(self):
        with self.assertRaises ValueError:
            transfermoney(1, 2, 'a')

    def test_transfermoney_sufficient_funds(self):
        self.connection_mock.execute.return_value = Mock()
        transfermoney(1, 2, 100)
        self.engine_mock.execute.assert_called_with(text("UPDATE accounts SET balance = balance - :p_amount WHERE id = :p_sender"), 
                                                     {"p_sender": 1, "p_amount": 100})
        self.engine_mock.execute.assert_called_with(text("UPDATE accounts SET balance = balance + :p_amount WHERE id = :p_receiver"), 
                                                     {"p_receiver": 2, "p_amount": 100})
        self.connection_mock.commit.assert_called_once()

    def test_transfermoney_insufficient_funds(self):
        self.connection_mock.execute.return_value = Mock()
        self.connection_mock.execute.return_value = Mock()
        self.engine_mock.execute.return_value = Mock()
        self.engine_mock.execute.return_value = Mock()
        self.connection_mock.execute.return_value = Mock()
        transfermoney(1, 2, 200)
        with self.assertRaises Exception:
            self.engine_mock.execute.assert_called_with(text("UPDATE accounts SET balance = balance - :p_amount WHERE id = :p_sender"), 
                                                         {"p_sender": 1, "p_amount": 200})
        self.engine_mock.execute.assert_called_with(text("UPDATE accounts SET balance = balance + :p_amount WHERE id = :p_receiver"), 
                                                         {"p_receiver": 2, "p_amount": 200})
        self.connection_mock.commit.assert_called_once()

    def test_get_balance_no_account(self):
        with self.assertRaises RegisterrionError:
            get_balance(1)

    def test_get_balance(self):
        df = pd.DataFrame({'balance': [100]})
        self.connection_mock.execute.return_value = df
        result = get_balance(1)
        self.assertEqual(result, 100)

if __name__ == '__main__':
    unittest.main()
