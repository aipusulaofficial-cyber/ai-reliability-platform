from reliability_domain import *
def test_slo_math():
 s=SLO("availability",.99,1000);assert sli(990,1000)==.99;assert error_budget(s,990,1000)==0