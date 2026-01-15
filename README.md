# Employee-Management-CRUD-API
A RESTful API built using Flask to manage employee records in a company. This project demonstrates CRUD operations for employees with proper validation, error handling, and token-based authentication using JWT.

**Tech Stack**
Backend: Python, Flask
Database: MySQL (SQLAlchemy ORM)
Authentication: JWT (Flask-JWT-Extended)
Migrations: Flask-Migrate

**Features**
JWT Authentication for secure access.
Create, Read, Update, and Delete employees
Pagination and filtering by department and role
Validation for unique email addresses
Detailed error handling
JSON responses for all endpoints

**Installation**

Clone the repository:
git clone https://github.com/thennalap/Employee-Management-CRUD-API.git
cd Employee-Management-CRUD-API


Create and activate a virtual environment:
python -m venv venv **# Windows**
venv\Scripts\activate


Install dependencies:
pip install -r requirements.txt


Create the database in MySQL:
CREATE DATABASE employee_management;

**Configuration**
Update your config.py with your database connection:

SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/employee_management'
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = 'your_jwt_secret_key'
SECRET_KEY = 'your_secret_key'

**Running the Application**
Initialize the database:
flask db init
flask db migrate -m "Initial migration"
flask db upgrade


Run the Flask server:
flask run or python run.py


The API will be available at http://127.0.0.1:5000/api/.
