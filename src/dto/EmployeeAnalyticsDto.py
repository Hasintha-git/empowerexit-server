class EmployeeAnalyticsDto:

    def __init__(self, id,emp_id,name,department,performance,probability,period ):
        self.id = id
        self.emp_id = emp_id
        self.name = name
        self.department = department
        self.performance = performance
        self.probability = probability
        self.period = period

    def __repr__(self) -> dict[str, int]:
        return {"id": self.id,"emp_id":self.emp_id, "name": self.name,'department':self.department,'performance':self.performance,'probability':self.probability,'period':self.period}