from flask import request, jsonify
from app.api import bp
from app import db
from app.models import Employee
from sqlalchemy import desc
from flask_jwt_extended import jwt_required, create_access_token

# Login API.. Hardcoded credentials...username=admin, password=admin123
@bp.route('/login', methods=['POST'])
def login():
    auth=request.authorization
    if not auth:
        return jsonify({"error": "Authorization header missing"}), 401
    username = auth.username
    password = auth.password

    if not username:
        return jsonify({"error": "Username Missing"}), 401
    
    
    if not password:
        return jsonify({"error": "Password Missing"}), 401


    if username != "admin" or password != "admin123":
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity="admin")
    return jsonify({"access_token":access_token}), 200



# Create an Employee
@bp.route('/employees', methods=['POST'])
@jwt_required()
def create_employee():
    
        data=request.json

        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400
        
        if not data.get("name"):
            return jsonify({"error": "Name is required"}), 400

        if not data.get("email"):
            return jsonify({"error": "Email is required"}), 400
        
        if Employee.query.filter(Employee.email==data['email']).first():
            return jsonify({"error": "Email already exists"}), 400 
        try:
            employee = Employee(name=data["name"],email=data["email"],department=data.get("department"),role=data.get("role"))
            db.session.add(employee)
            db.session.commit()           
            return jsonify( {"message": "Employee created successfully","employee": employee.to_dict()}), 201    
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Internal server error", "details": str(e)}), 500
    
#List all the employees
@bp.route('/employees/', methods=['GET'])
@jwt_required()
def list_employees():
    try:
        page = request.args.get("page", 1, type=int)
        per_page=10
        department = request.args.get("department")
        role=request.args.get("role")

        query = Employee.query
        
        if department:
            query = query.filter_by(department=request.args["department"])

        if role:
            query = query.filter_by(role=request.args["role"])

        query = query.order_by(desc(Employee.id))
        pagination = query.paginate(page=page, per_page=per_page,error_out=False)

        return jsonify({
            "employees": [e.to_dict() for e in pagination.items],
            "total_items": pagination.total,
            "page":page,
            "per_page":per_page,
            "total_pages": pagination.pages
        }), 200
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

# Get an employee details using ID
@bp.route('/employees/<int:id>', methods=['GET'])
@jwt_required()
def get_employee(id):
    try:
        employee=Employee.query.get(id)
        if not employee:
            return jsonify({"error": "Employee not found"}), 404
        
        return jsonify({"message": "Employee fetched successfully","data": employee.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
    
#Update an employee using ID
@bp.route('employees/<int:id>',methods=['PUT'])
@jwt_required()
def update_employee(id):
    employee = Employee.query.get(id)
    if not employee:
        return jsonify({"error": "Employee not found"}), 404
    
    data=request.json
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    
    if "email" in data and data['email']:
        existing_email = Employee.query.filter(Employee.email == data["email"], Employee.id != id).first()
        if existing_email:
            return jsonify({"error": "Email already exists for another employee"}), 400        
        employee.email = data["email"]

    if "name" in data:
        employee.name=data['name']

    if "deoartment" in data:
        employee.department=data['department']

    if "role" in data:
        employee.role=data['role']
    db.session.commit()       
    return jsonify({'message':'Employee updated successfully'}),200

# delete an employee
@bp.route('/employees/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_employee(id):
    try:
        employee = Employee.query.get(id)
        if not employee:
            return jsonify({"error": "Employee not found"}), 404

        db.session.delete(employee)
        db.session.commit()
        return jsonify({"message": "Employee deleted successfully"}), 204

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
