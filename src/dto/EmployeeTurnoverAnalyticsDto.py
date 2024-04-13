class EmployeeTurnoverAnalyticsDto:
    def __init__(self,probability,period,is_drivers_exists,drivers,measures):

        self.probability = probability
        self.period = period
        self.is_drivers_exists = is_drivers_exists
        self.drivers = drivers
        self.measures = measures


    def __repr__(self) -> dict[str, int]:
        return { "probability": self.probability,'period':self.period,"is_drivers_exists":self.is_drivers_exists,"drivers": self.drivers,'measures':self.measures}
