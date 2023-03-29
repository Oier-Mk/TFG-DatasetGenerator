import unittest
from database import *

class TestDatabase(unittest.TestCase):
    def test_load_database(self):
        env = '.envDDBB'
        db = load_database(env)
        self.assertTrue(db.is_connected())
        db.close()

    def test_insert_user(self):
        env = '.envDDBB'
        mail = 'test'
        name = 'test'
        password = 'test'
        insert_user(env, mail, name, password)
        db = load_database(env)
        mycursor = db.cursor()
        try:
            mycursor.execute("SELECT name FROM Users WHERE mail = %s", (mail, ))
            result = mycursor.fetchone()
        except:
            AssertionError

        self.assertEqual(result[0], name)

        try:
            mycursor.execute("DELETE from Users WHERE mail = %s", (mail, ))
            result = mycursor.fetchone()
        except:
            AssertionError
        db.close()

    def test_get_user(self):
        env = '.envDDBB'
        user = get_user(env, "oime3564@gmail.com")
        self.assertEqual('asdf', user)

    def test_user_exists(self):
        env = '.envDDBB'
        user = user_exists(env, "oime3564@gmail.com")
        self.assertTrue(user)
    
    def test_get_password(self):
        env = '.envDDBB'
        user = get_password(env, "oime3564@gmail.com")
        self.assertEqual('asdf', user)

    def test_print_users(self):
        env = '.envDDBB'
        print_users(env)


if __name__ == '__main__':
    unittest.main()