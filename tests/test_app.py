import pytest
from app import create_app
from config import Config

class TestConfig(Config):
    TESTING=True
    WTF_CSRF_ENABLED=False
    SQLALCHEMY_DATABASE_URI="sqlite:///:memory:"
    SECRET_KEY="test-secret"

@pytest.fixture()
def client():
    app=create_app(TestConfig)
    with app.test_client() as client: yield client

def register(client):
    return client.post("/register",data={"name":"Test User","email":"test@example.com","password":"password123"},follow_redirects=True)

def test_register_and_dashboard(client):
    response=register(client); assert response.status_code==200; assert b"Good to see you" in response.data

def test_login_logout(client):
    client.post("/register",data={"name":"Test User","email":"test@example.com","password":"password123"}); client.post("/logout"); response=client.get("/dashboard",follow_redirects=True); assert b"Sign in" in response.data

def test_income_and_expense(client):
    register(client); response=client.post("/income",data={"source":"Salary","amount":"50000","received_on":"2026-09-01","note":""},follow_redirects=True); assert b"Income recorded" in response.data
    response=client.post("/expenses",data={"category_id":"1","amount":"1000","spent_on":"2026-09-02","merchant":"Test","note":""},follow_redirects=True); assert response.status_code==200
