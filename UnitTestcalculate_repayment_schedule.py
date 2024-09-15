
import unittest
from your_module import calculate_repayment_schedule  # Replace with the actual module name

class TestCalculateRepaymentSchedule(unittest.TestCase):
    def test_repayment_schedule_calculated_successfully(self):
        loan_id = 1  # Replace with an existing loan ID
        result = calculate_repayment_schedule(loan_id)
        self.assertEquals(result, "Repayment schedule calculated successfully")

    def test_non_existent_loan_id(self):
        loan_id = 9999  # Replace with a non-existent loan ID
        result = calculate_repayment_schedule(loan_id)
        self.assertEquals(result, "Repayment schedule calculated successfully")  # This should still return successfully, as the function doesn't check for loan existence

    def test_invalid_loan_id(self):
        loan_id = " invalid"  # Replace with an invalid loan ID
        with self.assertRaises(psycopg2.Error):
            calculate_repayment_schedule(loan_id)

if __name__ == "__main__":
    unittest.main()
