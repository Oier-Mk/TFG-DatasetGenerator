from user_management.sessions import SessionData

def test_session_data():
    session_data = SessionData(username="test")
    assert session_data.username == "test"
