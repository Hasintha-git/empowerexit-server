class HighPerformanceEmpStat:
    def __init__(self, id,name,rate):
        self.id = id
        self.name = name
        self.rate = rate


    def __repr__(self) -> dict[str, int]:
        return {"id": self.id, "name": self.name,'rate':self.rate}
