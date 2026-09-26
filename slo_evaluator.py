from dataclasses import dataclass


@dataclass(frozen=True)
class BurnRateWindow:
    good_events:int
    total_events:int
    target:float
    def value(self)->float:
        if self.total_events<1 or not 0<self.target<1: raise ValueError("invalid SLO window")
        error_rate=1-self.good_events/self.total_events
        return error_rate/(1-self.target)
    def breaching(self,threshold:float=1.0)->bool:
        return self.value()>threshold
