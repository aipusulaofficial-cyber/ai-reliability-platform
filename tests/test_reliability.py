from reliability import *
import pytest
def test_slo(): assert SLO(.99).evaluate(990,1000)["within_slo"]
def test_counts(): 
 with pytest.raises(ValueError): SLO(.9).evaluate(11,10)
def test_incident(): 
 i=Incident();i.open("latency");i.resolve();assert i.events==["opened:latency","resolved"]
