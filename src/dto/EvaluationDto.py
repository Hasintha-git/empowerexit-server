class EvaluationDto:
    def __init__(self, factor,rate,is_rate_increased):
        self.factor = factor
        self.rate = rate
        self.is_rate_increased = is_rate_increased


    def __repr__(self) -> dict[str, int]:
        return {"factor": self.factor, "rate": self.rate,'is_rate_increased':self.is_rate_increased}
