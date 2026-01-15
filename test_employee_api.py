import pytest
from app import create_app, db
from app.models import Employee
from flask_jwt_extended import create_access_token
import base64

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/employee_management'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def get_token(client, username, password):
    """
    Logs in to the API with provided username/password
    and returns the JWT access token.
    """
    # Create the Basic Auth header
    auth_str = f"{username}:{password}"
    auth_header = "Basic " + base64.b64encode(auth_str.encode()).decode()

    # Send login request
    response = client.post('/api/login', headers={"Authorization": auth_header})
    
    if response.status_code != 200:
        return None  # Login failed    
    return response.get_json()['access_token']


def test_login_success(client):
    token = get_token(client, "admin", "admin123")
    assert token is not None

def test_login_fail_wrong_password(client):
    token = get_token(client, "admin", "wrongpass")
    assert token is None

def test_login_fail_wrong_username(client):
    token = get_token(client, "user", "admin123")
    assert token is None

def test_create_employee_success(client):
    # Get JWT token
    token = get_token(client, "admin", "admin123")
    headers = {"Authorization": f"Bearer {token}"}

    # Send POST request to create employee
    response = client.post('/api/employees', json={
        "name": "Alice",
        "email": "alice2@example.com",
        "department": "IT",
        "role": "Developer"
    }, headers=headers)

    data = response.get_json()

    # Assertions
    assert response.status_code == 201
    assert data['message'] == "Employee created successfully"


def test_create_employee_missing_fields(client):
    token = get_token(client, "admin", "admin123")
    headers = {"Authorization": f"Bearer {token}"}

    # Missing name
    response = client.post('/api/employees', json={"email":"bob@example.com"}, headers=headers)
    assert response.status_code == 400

    # Missing email
    response = client.post('/api/employees', json={"name":"Bob"}, headers=headers)
    assert response.status_code == 400


def test_create_employee_duplicate_email(client):
    token = get_token(client, "admin", "admin123")
    headers = {"Authorization": f"Bearer {token}"}

    # Create employee first time
    client.post('/api/employees', json={"name":"John","email":"john@example.com"}, headers=headers)

    # Try to create with same email
    response = client.post('/api/employees', json={"name":"John2","email":"john@example.com"}, headers=headers)
    assert response.status_code == 400


def test_get_employee_success(client):
    # Get JWT token
    token = get_token(client, "admin", "admin123")
    headers = {"Authorization": f"Bearer {token}"}
  

    # Now, get the employee by ID
    response = client.get('/api/employees/1', headers=headers)
    data = response.get_json()

    # Assertions
    assert response.status_code == 200
    assert data['message'] == "Employee fetched successfully"


def test_get_employee_not_found(client):
    token = get_token(client, "admin", "admin123")
    headers = {"Authorization": f"Bearer {token}"}

    # Try to get a non-existent employee
    response = client.get('/api/employees/999', headers=headers)
    data = response.get_json()

    assert response.status_code == 404
    assert data['error'] == "Employee not found"


def test_get_employee_unauthorized(client):
    # Access without JWT token
    response = client.get('/api/employees/1')
    assert response.status_code == 401





