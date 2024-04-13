class AnalyticsStatisticsDto:
    def __init__(self,id, name, value):
        self.id = id
        self.name = name
        self.value = value

    def __repr__(self) -> dict[str, int]:
        return {"id":id,"name": self.name, "value": self.value}