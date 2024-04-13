class TurnoverRateWithMonthDto:
    def __init__(self,date,rate):
        self.date = date
        self.rate = rate


    def __repr__(self) -> dict[str, int]:
        return { "date": self.date,'rate':self.rate}
