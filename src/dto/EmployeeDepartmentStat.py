class EmployeeDepartmentStat:
    def __init__(self, id,name,total_count,predicted_count,percentage):
        self.id = id
        self.name = name
        self.total_count = total_count
        self.predicted_count = predicted_count
        self.percentage = percentage


    def __repr__(self) -> dict[str, int]:
        return {"id": self.id, "name": self.name, "total_count": self.total_count,'predicted_count':self.predicted_count,'percentage':self.percentage}
