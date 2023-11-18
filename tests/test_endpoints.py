from app.main import app
from fastapi.testclient import TestClient
import string
from app.core.logic import Strongness

client = TestClient(app)


def test_homepage_not_found():
    response = client.get("/")
    assert response.status_code == 404


def test_generate_password():
    response = client.get("/passgen/generate")
    response_data = response.json()
    password = response_data["password"]

    assert any(c.isdigit() for c in password)
    assert any(c.islower() for c in password)
    assert any(c.isupper() for c in password)
    assert any(c in string.punctuation for c in password)
    assert len(password) == Strongness.STRONG.value[1]
    assert response_data["strongness"] == "Strong"
    assert response.status_code == 200


def test_generate_password_no_digits():
    response = client.get("/passgen/generate?digits=false")
    response_data = response.json()
    password = response_data["password"]

    assert not any(c.isdigit() for c in password)
    assert response.status_code == 200


def test_generate_password_no_upper():
    response = client.get("/passgen/generate?uppercase=false")
    response_data = response.json()
    password = response_data["password"]

    assert not any(c.isupper() for c in password)
    assert response.status_code == 200


def test_generate_password_no_lower():
    response = client.get("/passgen/generate?lowercase=false")
    response_data = response.json()
    password = response_data["password"]

    assert not any(c.islower() for c in password)
    assert response.status_code == 200


def test_generate_password_no_special():
    response = client.get("/passgen/generate?special_char=false")
    response_data = response.json()
    password = response_data["password"]

    assert not any(c in string.punctuation for c in password)
    assert response.status_code == 200


def test_generate_password_no_chars():
    response = client.get(
        "/passgen/generate?special_char=false&lowercase=false&uppercase=false&digits=false")
    assert response.status_code == 400


def test_generate_password_custom_length():
    test_length = 10
    response = client.get(f"passgen/generate?length={test_length}")
    response_data = response.json()
    password = response_data["password"]

    assert len(password) == test_length
    assert response.status_code == 200


def test_generate_password_false_length():
    test_length = 3
    response = client.get(f"passgen/generate?length={test_length}")

    assert response.status_code == 400


def test_password_check():
    test_password = "12345678"
    response = client.get(f"passgen/check?password={test_password}")
    assert response.status_code == 200


def test_password_check_strong():
    test_password = "tT3st_pAssw0rd!"
    response = client.get(f"passgen/check?password={test_password}")

    assert response.json()["strongness"] == Strongness.STRONG.value[0]
    assert response.status_code == 200


def test_password_check_moderate():
    test_password_small_length = "tT3st_pAss!"
    response = client.get(
        f"passgen/check?password={test_password_small_length}")

    assert response.json()["strongness"] == Strongness.MODERATE.value[0]
    assert response.status_code == 200

    test_password_upercase_digit = "tT3stpAssword"
    response = client.get(
        f"passgen/check?password={test_password_upercase_digit}")

    assert response.json()["strongness"] == Strongness.MODERATE.value[0]
    assert response.status_code == 200

    test_pass_special = "testpassword!"
    response = client.get(
        f"passgen/check?password={test_pass_special}")

    assert response.json()["strongness"] == Strongness.MODERATE.value[0]
    assert response.status_code == 200


def test_password_weak():
    test_password = "testPassword"
    response = client.get(
        f"passgen/check?password={test_password}")

    assert response.json()["strongness"] == Strongness.WEAK.value[0]
    assert response.status_code == 200
