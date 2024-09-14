
import unittest
from your_module import calculate_repayment_schedule  # Replace with the actual module name

class TestCalculateRepaymentSchedule(unittest.TestCase):
    def test_calculate_repayment_schedule(self):
        loan_id = 1  # Replace with an existing loan ID in your database
        calculate_repayment_schedule(loan_id)
        # Assuming the repayment schedule is inserted into the RepaymentSchedule table
        connection = engine.connect()
        query = sa.text("SELECT COUNT(*) FROM repaymentschedule WHERE loanid = :loan_id")
        result = connection.execute(query, {"loan_id": loan_id})
        count = result.scalar()
        self.assertEquals(count, 36)  # Replace with the expected number of repayment schedule entries

    def test_loan_not_found(self):
        loan_id = 999  # Replace with a non-existent loan ID in your database
        with self.assertRaises(sa.exc.NoResultFound):
            calculate_repayment_schedule(loan_id)

    def test_invalid_loan_id(self):
        loan_id = "invalid"  # Replace with an invalid loan ID (e.g., not an integer)
        with self.assertRaises(ValueError):
            calculate_repayment_schedule(loan_id)

if __name__ == "__main__":
    unittest.main()
