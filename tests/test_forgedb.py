
import tempfile
import unittest

from engine import ForgeDB


class TestForgeDB(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db = ForgeDB(self.temp_dir.name)
        self.db.execute(
            "CREATE TABLE students (id INT, name TEXT, age INT)"
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_insert_and_select(self):
        self.db.execute(
            "INSERT INTO students VALUES (1, 'Ravi', 20)"
        )
        result = self.db.execute("SELECT * FROM students")

        self.assertEqual(
            result,
            [{"id": 1, "name": "Ravi", "age": 20}]
        )

    def test_where(self):
        self.db.execute(
            "INSERT INTO students VALUES (1, 'Ravi', 20)"
        )
        self.db.execute(
            "INSERT INTO students VALUES (2, 'Priya', 17)"
        )

        result = self.db.execute(
            "SELECT name FROM students WHERE age > 18"
        )

        self.assertEqual(result, [{"name": "Ravi"}])

    def test_update_and_delete(self):
        self.db.execute(
            "INSERT INTO students VALUES (1, 'Ravi', 20)"
        )
        self.db.execute(
            "UPDATE students SET age = 22 WHERE id = 1"
        )
        self.assertEqual(
            self.db.execute("SELECT age FROM students"),
            [{"age": 22}]
        )

        self.db.execute("DELETE FROM students WHERE id = 1")
        self.assertEqual(
            self.db.execute("SELECT * FROM students"), []
        )


if __name__ == "__main__":
    unittest.main()
