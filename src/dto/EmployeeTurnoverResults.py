class EmployeeTurnoverResults:

    def __init__(self, is_leaving, score, factors):
        self.is_leaving = is_leaving
        self.score = score
        self.factors = factors

    def __repr__(self) -> dict[str, int]:
        return {"is_leaving": self.is_leaving, "score": self.score, "factors": self.factors}
