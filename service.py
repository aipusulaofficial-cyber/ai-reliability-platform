from fastapi import FastAPI, HTTPException
from opentelemetry import trace
from pydantic import BaseModel

from reliability_domain import SLO, burn_rate, error_budget, sli

try:
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

    provider = TracerProvider(
        resource=Resource.create({"service.name": "ai-reliability-platform"})
    )
    provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)
except (ImportError, RuntimeError):
    pass

app = FastAPI(title="ai-reliability-platform", version="1.0.0")
tracer = trace.get_tracer("ai-reliability-platform")


class Request(BaseModel):
    key: str
    payload: dict = {}


@app.get("/health/live")
def live() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/ready")
def ready() -> dict[str, str]:
    return {"status": "ready"}


@app.post("/v1/reliability")
def handle(r: Request) -> dict[str, float | str]:
    with tracer.start_as_current_span("reliability.evaluate"):
        try:
            slo = SLO(
                r.key,
                float(r.payload.get("target", 0.99)),
                int(r.payload.get("window_requests", 1000)),
            )
            total = int(r.payload.get("total", 0))
            success = int(r.payload.get("successes", 0))
            observed = sli(success, total)
            return {
                "slo": slo.name,
                "sli": observed,
                "error_budget": error_budget(slo, success, total),
                "burn_rate": burn_rate(slo, observed),
            }
        except (ValueError, KeyError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
