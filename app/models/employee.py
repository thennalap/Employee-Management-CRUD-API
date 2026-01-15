from datetime import datetime
from app import db

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    department = db.Column(db.String(100))
    role = db.Column(db.String(50))
    date_joined = db.Column(db.DateTime, default=datetime.now())
    created_on = db.Column(db.DateTime, default=datetime.now())
    updated_on = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())


    def __str__(self):
        return f"Employee(id={self.id}, name={self.name}, email={self.email})"


    def to_dict(self):
        data={
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "department": self.department,
            "role": self.role,
            "date_joined": self.date_joined.strftime("%d-%m-%Y %H:%M:%S")
        }
        return data 
