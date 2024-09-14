
import unittest
from your_module import generate_repayment_schedule  # Replace with the actual module name

class TestGenerateRepaymentSchedule(unittest.TestCase):
    def test_loan_id_1(self):
        result = generate_repayment_schedule(1)
        self.assertEqual(result, 'Repayment schedule generated successfully')

    def test_loan_id_2(self):
        result = generate_repayment_schedule(2)
        self.assertEqual(result, 'Repayment schedule generated successfully')

    def test_invalid_loan_id(self):
        with self.assertRaises(Exception):
            generate_repayment_schedule(99999)  # Replace with a non-existent loan ID

if __name__ == '__main__':
    unittest.main()
