class TurnoverDriverWithRateDto:
    def __init__(self,name,rate):
        self.name = name
        self.rate = rate


    def __repr__(self) -> dict[str, int]:
        return { "name": self.name,'rate':self.rate}
