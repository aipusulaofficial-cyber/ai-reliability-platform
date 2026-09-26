# Principal Engineering Evidence

## Scope
AI reliability platform covering reliability signals, health endpoints, observability, and resilience-oriented runtime behavior.

## Enforced controls
- [x] GitHub Actions least-privilege permissions
- [x] Third-party Actions pinned to immutable commit SHAs
- [x] Checkout credentials disabled
- [x] Workflow timeouts
- [x] Automated unit and HTTP production tests
- [x] Dependency and filesystem security scan
- [x] CycloneDX SBOM generation
- [x] Kubernetes non-root UID/GID 10001
- [x] RuntimeDefault seccomp
- [x] Privilege escalation disabled
- [x] Read-only root filesystem
- [x] All Linux capabilities dropped
- [x] Resource requests/limits and health probes
- [x] Immutable application image version 0.1.0
- [x] Helm autoscaling configured

## Evidence boundary
GREEN means the configured CI, production-test, and dependency-audit gates pass on the current main commit. It is repository-level engineering evidence, not an environment-independent production certification.
