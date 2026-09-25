from dataclasses import dataclass
@dataclass
class SLO:
 target:float
 def evaluate(self,good,total):
  if total<0 or good<0 or good>total: raise ValueError("invalid counts")
  rate=good/total if total else 1.0
  return {"availability":rate,"error_budget":max(0.0,rate-self.target),"within_slo":rate>=self.target}
class Incident:
 def __init__(self): self.state="closed";self.events=[]
 def open(self,reason): self.state="open";self.events.append("opened:"+reason)
 def resolve(self): self.state="closed";self.events.append("resolved")
