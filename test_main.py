from fastapi.testclient import TestClient
from main import app
from db_connection import get_connection

client = TestClient(app)


def setup_module(module):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM grades")

    conn.commit()
    cur.close()
    conn.close()


def test_upload_grades():
    csv_content = (
        "full_name,subject,grade\n"
        "Иванов Иван,Math,2\n"
        "Иванов Иван,Physics,2\n"
        "Иванов Иван,Chemistry,2\n"
        "Иванов Иван,Biology,2\n"
        "Иванов Иван,PE,2\n"
        "Иванов Иван,CS,5\n"
        "Петров Пётр,Math,2\n"
        "Петров Пётр,Physics,2\n"
        "Петров Пётр,Chemistry,5\n"
        "Петров Пётр,Biology,3\n"
        ",Math,5\n"
        "Попов Андрей,Physics,9\n"
        "Попов Андрей,  ,3\n"
        "Попов Андрей   ,PE,   \n"
    )

    response = client.post(
        "/upload-grades",
        files={"file": ("test.csv", csv_content, "text/csv")}
    )

    assert response.status_code == 200

    data = response.json()

    assert data == {
        "status": "ok",
        "records_loaded": 10,
        "students": 2
    }


def test_more_than_3_twos():
    response = client.get("/students/more-than-3-twos")

    assert response.status_code == 200

    data = response.json()

    assert {
        "full_name": "Иванов Иван",
        "count_twos": 5
    } in data

    assert all(item["count_twos"] > 3 for item in data)


def test_less_than_5_twos():
    response = client.get("/students/less-than-5-twos")

    assert response.status_code == 200

    data = response.json()

    assert {
        "full_name": "Петров Пётр",
        "count_twos": 2
    } in data

    assert all(item["count_twos"] < 5 for item in data)