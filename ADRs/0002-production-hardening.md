# ADR-0002: Production hardening
Reliability APIs use FastAPI with OpenTelemetry traces. Kubernetes/Helm define probes and bounded resources; Terraform owns infrastructure inputs. Trivy/CycloneDX gate supply-chain and SBOM risk; contract/property tests protect the API; Locust provides load validation.
SLO state and incident records remain domain-owned; production externalizes durable storage, secrets, telemetry and autoscaling.
