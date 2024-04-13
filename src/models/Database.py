from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __repr__(self) -> str:
        return 'User>>> {self.first_name}'


class Employee(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    emp_id = db.Column(db.String(45), unique=False, nullable=False)
    name = db.Column(db.String(45), unique=False, nullable=False)
    designation = db.Column(db.String(45), unique=False, nullable=False)
    fk_department_id = db.Column(db.Integer, unique=False, nullable=False)
    address = db.Column(db.String(45), unique=False, nullable=False)
    contact = db.Column(db.String(45), unique=False, nullable=False)
    supervisor = db.Column(db.String(45), unique=False, nullable=False)
    joined_date = db.Column(db.DateTime, unique=False, nullable=False)
    performance_grade = db.Column(db.String(45), unique=False, nullable=False)
    note = db.Column(db.String(1000), unique=False, nullable=True)
    is_leaving = db.Column(db.Boolean, unique=False, nullable=True)
    latest_turnover_rate = db.Column(db.String(20), unique=False, nullable=True)
    latest_months_to_leave=db.Column(db.String(20), unique=False, nullable=True)
    created_timestamp = db.Column(db.DateTime, unique=False, nullable=False)
    updated_timestamp = db.Column(db.DateTime, unique=False, nullable=True)

    def __repr__(self) -> dict[str, int]:
        return {"id": self.id, "emp_id": self.emp_id, "name": self.name, "designation": self.designation,
                "fk_department_id": self.fk_department_id, "address": self.address, "contact": self.contact,
                "supervisor": self.supervisor, "joined_date": self.joined_date,
                "performance_grade": self.performance_grade,
                "note": self.note, 
                "is_leaving": self.is_leaving, 
                "latest_turnover_rate": self.latest_turnover_rate,
                "latest_days_to_leave":self.latest_months_to_leave, 
                "created_timestamp": self.created_timestamp,
                "updated_timestamp": self.updated_timestamp}
    

class Department(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(45), unique=False, nullable=False)
    created_timestamp = db.Column(db.DateTime, unique=False, nullable=False)

    def __repr__(self) -> dict[str, int]:
        return {"id": self.id, "name": self.name, "created_timestamp": self.created_timestamp}
    
class Prediction(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fk_emp_id = db.Column(db.Integer, unique=False, nullable=False)
    is_leaving = db.Column(db.Boolean, unique=False, nullable=False)
    turnover_rate = db.Column(db.String(20), unique=False, nullable=False)
    month_to_leave=db.Column(db.Integer, unique=False, nullable=True)
    created_timestamp = db.Column(db.DateTime, unique=False, nullable=False)
    updated_timestamp = db.Column(db.DateTime, unique=False, nullable=True)

    def __repr__(self) -> dict[str, int]:
        return {"id": self.id, "fk_emp_id": self.fk_emp_id, "is_leaving": self.is_leaving, "turnover_rate": self.turnover_rate,
                 "days_to_leave":self.days_to_leave,"created_timestamp": self.created_timestamp,"updated_timestamp":self.updated_timestamp}
    
class TurnoverFactor(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    factor = db.Column(db.String(45), unique=False, nullable=False)
    display_name = db.Column(db.String(45), unique=False, nullable=True)
    measure = db.Column(db.String(500), unique=False, nullable=True)
    created_timestamp = db.Column(db.DateTime, unique=False, nullable=False)

    def __repr__(self) -> dict[str, int]:
        return {"id": self.id, "factor": self.factor,"display_name": self.display_name,"measure": self.measure,"created_timestamp": self.created_timestamp}
    
class PredictionFactorMapping(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fk_prediction_id = db.Column(db.Integer, unique=False, nullable=False)
    fk_factor_id = db.Column(db.Integer, unique=False, nullable=False)
    score = db.Column(db.String(20), unique=False, nullable=False)
    created_timestamp = db.Column(db.DateTime, unique=False, nullable=False)
    updated_timestamp = db.Column(db.DateTime, unique=False, nullable=True)

    def __repr__(self) -> dict[str, int]:
        return {"id": self.id, "fk_prediction_id": self.fk_prediction_id, "fk_factor_id": self.fk_factor_id, "score": self.score,
                 "created_timestamp": self.created_timestamp,"updated_timestamp":self.updated_timestamp}
