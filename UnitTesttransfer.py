
import unittest
from unittest.mock import patch, Mock
from transfer_funds import transfer_funds

class TestTransferFunds(unittest.TestCase):
    @patch('logging.basicConfig')
    @patch('logging.getLogger')
    @patch('logging.Logger.info')
    @patch('psycopg2.Error')
    @patch('psycopg2.connect')
    @patch('sqlalchemy.text')
    @patch('pandas')
    def test_transfer_funds_success(self, pd_mock, text_mock, conn_mock, error_mock, info_mock, getLogger_mock, basicConfig_mock):
        # Arrange
        pd_mock.DataFrame = Mock(return_value=[{'id': 1, 'balance': 100}])
        text_mock = Mock(return_value=text("UPDATE accounts SET balance = balance - :p_amount WHERE id = :p_sender"))
        conn_mock = Mock()
        conn_mock.execute.return_value = 1
        conn_mock.commit.return_value = None
        error_mock = Mock()
        info_mock = Mock()
        getLogger_mock.return_value = Mock(info=info_mock)

        # Act
        transfer_funds(1, 2, 50)

        # Assert
        self.assertEqual(conn_mock.execute.call_count, 2)
        self.assertEqual(conn_mock.commit.call_count, 1)
        self.assertEqual(info_mock.call_count, 3)

    @patch('logging.basicConfig')
    @patch('logging.getLogger')
    @patch('logging.Logger.error')
    @patch('psycopg2.Error')
    @patch('psycopg2.connect')
    @patch('sqlalchemy.text')
    @patch('pandas')
    def test_transfer_funds_error(self, pd_mock, text_mock, conn_mock, error_mock, error_logger_mock, getLogger_mock, basicConfig_mock):
        # Arrange
        pd_mock.DataFrame = Mock(return_value=[{'id': 1, 'balance': 100}])
        text_mock = Mock(return_value=text("UPDATE accounts SET balance = balance - :p_amount WHERE id = :p_sender"))
        conn_mock = Mock()
        conn_mock.execute.return_value = error_mock
        error_mock = Mock()
        error_logger_mock = Mock()
        getLogger_mock.return_value = Mock(error=error_logger_mock)

        # Act
        with self.assertRaises(psycopg2.Error):
            transfer_funds(1, 2, 50)

        # Assert
        self.assertEqual(conn_mock.execute.call_count, 2)
        self.assertEqual(error_logger_mock.call_count, 1)

    @patch('logging.basicConfig')
    @patch('logging.getLogger')
    @patch('logging.Logger.info')
    @patch('psycopg2.Error')
    @patch('psycopg2.connect')
    @patch('sqlalchemy.text')
    @patch('pandas')
    def test_transfer_funds_zero_balance(self, pd_mock, text_mock, conn_mock, error_mock, info_mock, getLogger_mock, basicConfig_mock):
        # Arrange
        pd_mock.DataFrame = Mock(return_value=[{'id': 1, 'balance': 0}])
        text_mock = Mock(return_value=text("UPDATE accounts SET balance = balance - :p_amount WHERE id = :p_sender"))
        conn_mock = Mock()
        conn_mock.execute.return_value = 1
        conn_mock.commit.return_value = None
        error_mock = Mock()
        info_mock = Mock()
        getLogger_mock.return_value = Mock(info=info_mock)

        # Act
        transfer_funds(1, 2, 50)

        # Assert
        self.assertEqual(conn_mock.execute.call_count, 0)

    @patch('logging.basicConfig')
    @patch('logging.getLogger')
    @patch('logging.Logger.info')
    @patch('psycopg2.Error')
    @patch('psycopg2.connect')
    @patch('sqlalchemy.text')
    @patch('pandas')
    def test_transfer_funds_negative_balance(self, pd_mock, text_mock, conn_mock, error_mock, info_mock, getLogger_mock, basicConfig_mock):
        # Arrange
        pd_mock.DataFrame = Mock(return_value=[{'id': 1, 'balance': -100}])
        text_mock = Mock(return_value=text("UPDATE accounts SET balance = balance - :p_amount WHERE id = :p_sender"))
        conn_mock = Mock()
        conn_mock.execute.return_value = 1
        conn_mock.commit.return_value = None
        error_mock = Mock()
        info_mock = Mock()
        getLogger_mock.return_value = Mock(info=info_mock)

        # Act
        transfer_funds(1, 2, 50)

        # Assert
        self.assertEqual(conn_mock.execute.call_count, 0)

    @patch('logging.basicConfig')
    @patch('logging.getLogger')
    @patch('logging.Logger.info')
    @patch('psycopg2.Error')
    @patch('psycopg2.connect')
    @patch('sqlalchemy.text')
    @patch('pandas')
    def test_transfer_funds_invalid_sender(self, pd_mock, text_mock, conn_mock, error_mock, info_mock, getLogger_mock, basicConfig_mock):
        # Arrange
        pd_mock.DataFrame = Mock(return_value=[{'id': 1, 'balance': 100}])
        text_mock = Mock(return_value=text("UPDATE accounts SET balance = balance - :p_amount WHERE id = :p_sender"))
        conn_mock = Mock()
        conn_mock.execute.return_value = error_mock
        error_mock = Mock()
        info_mock = Mock()
        getLogger_mock.return_value = Mock(info=info_mock)

        # Act
        with self.assertRaises(psycopg2.Error):
            transfer_funds(0, 2, 50)

        # Assert
        self.assertEqual(conn_mock.execute.call_count, 0)

    @patch('logging.basicConfig')
    @patch('logging.getLogger')
    @patch('logging.Logger.info')
    @patch('psycopg2.Error')
    @patch('psycopg2.connect')
    @patch('sqlalchemy.text')
    @patch('pandas')
    def test_transfer_funds_invalid_receiver(self, pd_mock, text_mock, conn_mock, error_mock, info_mock, getLogger_mock, basicConfig_mock):
        # Arrange
        pd_mock.DataFrame = Mock(return_value=[{'id': 1, 'balance': 100}])
        text_mock = Mock(return_value=text("UPDATE accounts SET balance = balance - :p_amount WHERE id = :p_sender"))
        conn_mock = Mock()
        conn_mock.execute.return_value = error_mock
        error_mock = Mock()
        info_mock = Mock()
        getLogger_mock.return_value = Mock(info=info_mock)

        # Act
        with self.assertRaises(psycopg2.Error):
            transfer_funds(1, 0, 50)

        # Assert
        self.assertEqual(conn_mock.execute.call_count, 0)

if __name__ == '__main__':
    unittest.main()
