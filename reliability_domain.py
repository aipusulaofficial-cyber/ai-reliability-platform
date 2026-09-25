from dataclasses import dataclass

@dataclass(frozen=True)
class SLO:
    name:str; target:float; window_requests:int
    def __post_init__(self):
        if not 0<self.target<=1 or self.window_requests<1:raise ValueError("invalid SLO")

def sli(successes:int,total:int)->float:
    if total<1 or successes<0 or successes>total:raise ValueError("invalid measurements")
    return successes/total

def error_budget(slo:SLO,successes:int,total:int)->float:
    return max(0.0,slo.target-sli(successes,total))

def burn_rate(slo:SLO,observed_sli:float)->float:
    if not 0<observed_sli<=1:raise ValueError("invalid SLI")
    return (1-observed_sli)/(1-slo.target)
