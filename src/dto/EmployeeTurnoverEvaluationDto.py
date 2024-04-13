class EmployeeTurnoverEvaluationDto:
    def __init__(self,current_prob,previous_prob,is_prob_increase,prob_rate,current_period,prev_period,is_period_increase,period_rate,is_prev_factors_exists,prev_pred_factors):
        self.current_prob = current_prob
        self.previous_prob = previous_prob
        self.is_prob_increase = is_prob_increase
        self.prob_rate = prob_rate
        self.current_period = current_period
        self.prev_period = prev_period
        self.is_period_increase = is_period_increase
        self.period_rate = period_rate
        self.is_prev_factors_exists = is_prev_factors_exists
        self.prev_pred_factors = prev_pred_factors


    def __repr__(self) -> dict[str, int]:
        return { "current_prob": self.current_prob,'previous_prob':self.previous_prob, "is_prob_increase": self.is_prob_increase, "prob_rate": self.prob_rate,
                'current_period':self.current_period, "prev_period": self.prev_period,'is_period_increase':self.is_period_increase, 'period_rate':self.period_rate,
                "is_prev_factors_exists":self.is_prev_factors_exists,"prev_pred_factors":self.prev_pred_factors}
