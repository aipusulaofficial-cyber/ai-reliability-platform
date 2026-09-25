from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from opentelemetry import trace
from reliability_domain import *
try:
 from opentelemetry.sdk.resources import Resource
 from opentelemetry.sdk.trace import TracerProvider
 from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
 p=TracerProvider(resource=Resource.create({"service.name":"ai-reliability-platform"}));p.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()));trace.set_tracer_provider(p)
except Exception: pass
app=FastAPI(title="ai-reliability-platform",version="1.0.0");tracer=trace.get_tracer("ai-reliability-platform")
class Request(BaseModel): key:str; payload:dict={}
@app.get("/health/live")
def live(): return {"status":"ok"}
@app.get("/health/ready")
def ready(): return {"status":"ready"}
@app.post("/v1/reliability")
def handle(r:Request):
 with tracer.start_as_current_span("reliability.evaluate"):
  try:
   s=SLO(r.key,float(r.payload.get("target",.99)),int(r.payload.get("window_requests",1000)))
   total=int(r.payload.get("total",0));success=int(r.payload.get("successes",0));observed=sli(success,total)
   return {"slo":s.name,"sli":observed,"error_budget":error_budget(s,success,total),"burn_rate":burn_rate(s,observed)}
  except (ValueError,KeyError) as e: raise HTTPException(status_code=400,detail=str(e)) from e
