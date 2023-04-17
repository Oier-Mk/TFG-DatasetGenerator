# test_database.py

from database.database import load_database, insert_user, get_user, user_exists, get_password, print_users

def test_load_database():
    env = '/Users/mentxaka/Github/TFG-DatasetGenerator/Server/.envDDBB'
    db = load_database(env)
    assert db.is_connected()
    db.close()

def test_insert_user():
    env = '/Users/mentxaka/Github/TFG-DatasetGenerator/Server/.envDDBB'
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

    assert result[0] == name

    try:
        mycursor.execute("DELETE from Users WHERE mail = %s", (mail, ))
        result = mycursor.fetchone()
    except:
        AssertionError
    db.close()

def test_get_user():
    env = '/Users/mentxaka/Github/TFG-DatasetGenerator/Server/.envDDBB'
    user = get_user(env, "oime3564@gmail.com")
    assert user == 'asdf'

def test_user_exists():
    env = '/Users/mentxaka/Github/TFG-DatasetGenerator/Server/.envDDBB'
    user = user_exists(env, "oime3564@gmail.com")
    assert user == True

def test_get_password():
    env = '/Users/mentxaka/Github/TFG-DatasetGenerator/Server/.envDDBB'
    user = get_password(env, "oime3564@gmail.com")
    assert user == 'asdf'

def test_print_users(capsys):
    env = '/Users/mentxaka/Github/TFG-DatasetGenerator/Server/.envDDBB'
    print_users(env)
    captured = capsys.readouterr()
    assert "Users" in captured.out
