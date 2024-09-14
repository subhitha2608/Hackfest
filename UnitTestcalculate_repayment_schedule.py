
import unittest
import psycopg2

class TestGetUser(unittest.TestCase):
    def setUp(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="test_db",
            user="test_user",
            password="test_password"
        )
        self.cur = self.conn.cursor()
        self.create_table_query = "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, username VARCHAR(50), email VARCHAR(100))"
        self.cur.execute(self.create_table_query)
        self.conn.commit()

    def tearDown(self):
        self.drop_table_query = "DROP TABLE IF EXISTS users"
        self.cur.execute(self.drop_table_query)
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def test_get_user_by_id_valid_input(self):
        self.insert_user_query = "INSERT INTO users (username, email) VALUES (%s, %s) RETURNING id"
        self.cur.execute(self.insert_user_query, ("test_user", "test@example.com"))
        user_id = self.cur.fetchone()[0]
        self.conn.commit()

        from your_module import get_user
        user = get_user(user_id)
        self.assertIsNotNone(user)
        self.assertEqual(user["id"], user_id)
        self.assertEqual(user["username"], "test_user")
        self.assertEqual(user["email"], "test@example.com")
        print(f"User retrieved: {user}")

    def test_get_user_by_id_invalid_input(self):
        from your_module import get_user
        with self.assertRaises(ValueError):
            get_user(-1)
        print("Error: User ID should be a positive integer")

    def test_get_user_by_id_non_existent(self):
        from your_module import get_user
        user = get_user(1000)
        self.assertIsNone(user)
        print("User not found")

    def test_get_user_by_username_valid_input(self):
        self.insert_user_query = "INSERT INTO users (username, email) VALUES (%s, %s)"
        self.cur.execute(self.insert_user_query, ("test_user", "test@example.com"))
        self.conn.commit()

        from your_module import get_user
        user = get_user(username="test_user")
        self.assertIsNotNone(user)
        self.assertEqual(user["username"], "test_user")
        self.assertEqual(user["email"], "test@example.com")
        print(f"User retrieved: {user}")

    def test_get_user_by_username_invalid_input(self):
        from your_module import get_user
        with self.assertRaises(ValueError):
            get_user(username="")
        print("Error: Username should not be empty")

    def test_get_user_by_username_non_existent(self):
        from your_module import get_user
        user = get_user(username="non_existent_user")
        self.assertIsNone(user)
        print("User not found")

if __name__ == "__main__":
    unittest.main()
