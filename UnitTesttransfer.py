
import unittest
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from your_module import get_user_data, create_user, delete_user  # Import the functions to be tested

class TestUserData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conn = psycopg2.connect(
            host="localhost",
            database="test_db",
            user="test_user",
            password="test_password"
        )
        cls.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cls.cursor = cls.conn.cursor()

        # Create a test table
        cls.cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name VARCHAR(50), email VARCHAR(100))")

    @classmethod
    def tearDownClass(cls):
        # Drop the test table
        cls.cursor.execute("DROP TABLE IF EXISTS users")
        cls.conn.close()

    def test_get_user_data_valid_input(self):
        # Create a test user
        create_user("John Doe", "john@example.com")
        self.cursor.execute("SELECT * FROM users WHERE name='John Doe'")
        user_data = self.cursor.fetchone()

        # Test get_user_data function
        result = get_user_data(user_data[0])
        print("Result:", result)
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "John Doe")
        self.assertEqual(result["email"], "john@example.com")

    def test_get_user_data_invalid_input(self):
        # Test with non-existent user ID
        result = get_user_data(999)
        print("Result:", result)
        self.assertIsNone(result)

    def test_create_user_valid_input(self):
        # Test create_user function
        create_user("Jane Doe", "jane@example.com")
        self.cursor.execute("SELECT * FROM users WHERE name='Jane Doe'")
        user_data = self.cursor.fetchone()
        print("Result:", user_data)
        self.assertIsNotNone(user_data)
        self.assertEqual(user_data[1], "Jane Doe")
        self.assertEqual(user_data[2], "jane@example.com")

    def test_create_user_invalid_input(self):
        # Test with invalid email
        with self.assertRaises(psycopg2.Error):
            create_user("Invalid User", "invalid_email")
        print("Error caught!")

        # Test with existing user
        with self.assertRaises(psycopg2.Error):
            create_user("John Doe", "john@example.com")
        print("Error caught!")

    def test_delete_user_valid_input(self):
        # Create a test user
        create_user("Test User", "test@example.com")

        # Test delete_user function
        delete_user(1)  # Assuming ID 1 is the test user
        self.cursor.execute("SELECT * FROM users WHERE name='Test User'")
        user_data = self.cursor.fetchone()
        print("Result:", user_data)
        self.assertIsNone(user_data)

    def test_delete_user_invalid_input(self):
        # Test with non-existent user ID
        with self.assertRaises(psycopg2.Error):
            delete_user(999)
        print("Error caught!")

if __name__ == "__main__":
    unittest.main()
