class EmployeeSurveyRegressionData:

    def __init__(self, age, gender, marital_status,educational_status, total_years_industry, years_work_current_hotel, 
                number_of_years_current_role,department,salary,opportunities,workload):
        self.age = age
        self.gender = gender
        self.marital_status = marital_status
        self.educational_status = educational_status
        self.total_years_industry = total_years_industry
        self.years_work_current_hotel = years_work_current_hotel
        self.number_of_years_current_role = number_of_years_current_role
        self.department = department
        self.salary=salary
        self.opportunities=opportunities
        self.workload=workload

    def __repr__(self) -> dict[str, int]:
        return {"age": self.age, "gender": self.gender,
                "marital_status": self.marital_status, "educational_status": self.educational_status,
                "total_years_industry": self.total_years_industry,
                "years_work_current_hotel": self.years_work_current_hotel,
                "number_of_years_current_role": self.number_of_years_current_role,
                "department": self.department,"salary":self.salary,
                  "opportunities":self.opportunities,"workload": self.workload}
