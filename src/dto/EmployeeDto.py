class EmployeeDto:
    def __init__(self, id, emp_id, name, designation,department_code, department_id, address, contact, supervisor, joined_date, performance_grade, note):
        self.id = id
        self.emp_id = emp_id
        self.name = name
        self.designation = designation
        self.department_code = department_code
        self.department_id=department_id 
        self.address=address
        self.contact=contact
        self.supervisor=supervisor
        self.joined_date=joined_date
        self.performance_grade=performance_grade
        self.note=note
    

    def __repr__(self) -> dict[str, int]:
        return {"id": self.id,"emp_id":self.emp_id, "name": self.name,"designation":self.designation,"department_code":self.department_code,
                "fk_department_id":self.department_id,"address":self.address,"contact":self.contact,"supervisor":self.supervisor,
                "joined_date":self.joined_date,"performance_grade":self.performance_grade,"note":self.note}