
import pytest
import pandas as pd
from your_module import transfer_amount

@pytest.fixture
def engine_mock(mocker):
    return mocker.Mock()

@pytest.fixture
def conn_mock(mocker):
    return mocker.Mock()

@pytest.fixture
def result_mock(mocker):
    return mocker.Mock(return_value=None)

@pytest.mark.usefixtures("engine_mock", "conn_mock", "result_mock")
class TestTransferAmount:
    def test_zero_amount(self, engine_mock, conn_mock, result_mock):
        sender_id = "1"
        receiver_id = "2"
        amount = 0
        result = transfer_amount(sender_id, receiver_id, amount)
        assert result == []
        engine_mock.execute.assert_called_once()
        result_mock.reset_mock()
        result_mock.fetchall.return_value = []
        result_mock.reset_mock()
        result_mock.return_value = None
        conn_mock.commit.assert_called()

    def test_sender_id_not_found(self, engine_mock, conn_mock, result_mock):
        sender_id = "999"
        receiver_id = "2"
        amount = 100
        result = transfer_amount(sender_id, receiver_id, amount)
        assert result == []
        engine_mock.execute.assert_called_once()
        result_mock.reset_mock()
        result_mock.fetchall.return_value = []
        result_mock.reset_mock()
        result_mock.return_value = None
        conn_mock.commit.assert_called()

    def test_receiver_id_not_found(self, engine_mock, conn_mock, result_mock):
        sender_id = "1"
        receiver_id = "999"
        amount = 100
        result = transfer_amount(sender_id, receiver_id, amount)
        assert result == []
        engine_mock.execute.assert_called_once()
        result_mock.reset_mock()
        result_mock.fetchall.return_value = []
        result_mock.reset_mock()
        result_mock.return_value = None
        conn_mock.commit.assert_called()

    def test_amount_is_zero(self, engine_mock, conn_mock, result_mock):
        sender_id = "1"
        receiver_id = "2"
        amount = 0
        result = transfer_amount(sender_id, receiver_id, amount)
        assert result == []
        engine_mock.execute.assert_called_once()
        result_mock.reset_mock()
        result_mock.fetchall.return_value = []
        result_mock.reset_mock()
        result_mock.return_value = None
        conn_mock.commit.assert_called()

    def test_sender_balance_empty(self, engine_mock, conn_mock, result_mock):
        sender_id = "1"
        receiver_id = "2"
        amount = 100
        engine.execute.return_value.fetchall.return_value = []
        result = transfer_amount(sender_id, receiver_id, amount)
        assert result == []
        engine_mock.execute.assert_called_once()
        result_mock.reset_mock()
        result_mock.fetchall.return_value = []
        result_mock.reset_mock()
        result_mock.return_value = None
        conn_mock.commit.assert_called()

    def test_receiver_balance_empty(self, engine_mock, conn_mock, result_mock):
        sender_id = "1"
        receiver_id = "2"
        amount = 100
        update_receiver = text("UPDATE accounts SET balance = balance + :amount WHERE id = :receiver_id")
        result = engine.execute(update_receiver, {"receiver_id": receiver_id, "amount": 0})
        conn.commit()
        result_mock.reset_mock()
        result_mock.fetchall.return_value = []
        result_mock.reset_mock()
        result_mock.return_value = None
        conn_mock.commit.assert_called()
