class EmployeeSurveyClassificationData:

    def __init__(self, working_hours, promotional_barriers, work_life_balance, status_and_recognition, salary,
                 opportunities, workload, work_environment, training_and_development, relationship_with_colleagues,
                 relationship_with_supervisor, job_satisfaction, distance_from_home, age, gender, marital_status,
                 educational_status, total_years_industry, years_work_current_hotel, number_of_years_current_role,
                 department, last_promotion, hotel_assess_performance):
        self.working_hours = working_hours
        self.promotional_barriers = promotional_barriers
        self.work_life_balance = work_life_balance
        self.status_and_recognition = status_and_recognition
        self.salary = salary
        self.opportunities = opportunities
        self.workload = workload
        self.work_environment = work_environment
        self.training_and_development = training_and_development
        self.relationship_with_colleagues = relationship_with_colleagues
        self.relationship_with_supervisor = relationship_with_supervisor
        self.job_satisfaction = job_satisfaction
        self.distance_from_home = distance_from_home
        self.age = age
        self.gender = gender
        self.marital_status = marital_status
        self.educational_status = educational_status
        self.total_years_industry = total_years_industry
        self.years_work_current_hotel = years_work_current_hotel
        self.number_of_years_current_role = number_of_years_current_role
        self.department = department
        self.last_promotion = last_promotion
        self.hotel_assess_performance = hotel_assess_performance

    def __repr__(self) -> dict[str, int]:
        return {"working_hours": self.working_hours, "promotional_barriers": self.promotional_barriers,
                "work_life_balance": self.work_life_balance, "status_and_recognition": self.status_and_recognition,
                "salary": self.salary, "opportunities": self.opportunities, "workload": self.workload,
                "work_environment": self.work_environment, "training_and_development": self.training_and_development,
                "relationship_with_colleagues": self.relationship_with_colleagues,
                "relationship_with_supervisor": self.relationship_with_supervisor,
                "job_satisfaction": self.job_satisfaction, "distance_from_home": self.distance_from_home,
                "age": self.age, "gender": self.gender,
                "marital_status": self.marital_status, "educational_status": self.educational_status,
                "total_years_industry": self.total_years_industry,
                "years_work_current_hotel": self.years_work_current_hotel,
                "number_of_years_current_role": self.number_of_years_current_role,
                "department": self.department, "last_promotion": self.last_promotion,
                "hotel_assess_performance": self.hotel_assess_performance}
