
import unittest
import psycopg2

class TestGetUserDetails(unittest.TestCase):
    def setUp(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="mydatabase",
            user="myuser",
            password="mypassword"
        )
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name VARCHAR(50), email VARCHAR(100))")
        self.conn.commit()

    def tearDown(self):
        self.cursor.execute("DROP TABLE users")
        self.conn.commit()
        self.conn.close()

    def test_get_user_details_valid_input(self):
        self.cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", ("John Doe", "johndoe@example.com"))
        self.conn.commit()
        user_id = self.cursor.fetchone()[0]
        from mymodule import get_user_details
        result = get_user_details(user_id)
        print(f"Result: {result}")
        self.assertEqual(result, {"id": user_id, "name": "John Doe", "email": "johndoe@example.com"})

    def test_get_user_details_invalid_input(self):
        from mymodule import get_user_details
        with self.assertRaises(TypeError):
            get_user_details("not an integer")

    def test_get_user_details_non_existent_user(self):
        from mymodule import get_user_details
        with self.assertRaises(ValueError):
            get_user_details(999)

    def test_get_user_details_database_error(self):
        self.conn.close()
        from mymodule import get_user_details
        with self.assertRaises(psycopg2.Error):
            get_user_details(1)

if __name__ == "__main__":
    unittest.main()
