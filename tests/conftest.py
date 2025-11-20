import pytest
import mysql.connector

@pytest.fixture(scope="session")
def db_connection():
    """Connect to MySQL running in Docker for the test session.

    Adjust host/port/credentials if your Docker setup differs.
    """
    conn = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="tttuser",
        password="tttpass",
        database="tictactoe",
    )
    yield conn
    conn.close()

@pytest.fixture(autouse=True)
def clean_results(db_connection):
    """Clear the `results` table before each test to ensure isolation."""
    cursor = db_connection.cursor()
    cursor.execute("DELETE FROM results;")
    db_connection.commit()
    cursor.close()
    yield
