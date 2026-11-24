# Release and SLO gate acceptance

Use this narrow reference after reading the complete Super Skills 9.4 for infrastructure and release decisions and 4.3 where backend data or schema compatibility matters. It is acceptance guidance, not a deployment engine, monitoring integration, automatic rollback policy or substitute for real authorised operations.

## Build and start contract

- Identify the approved commit, lockfile and package-manager version, build command, expected generated artefact, actual runtime start command, runtime configuration and environment. Verify the artefact that the production command will run exists and is compatible with that command. Compilation, a source-level check or successful package installation alone does not prove production startup.
- Keep preview and production secrets, data destinations and public URLs distinct. Report unrun smoke checks, missing dependencies and unknown production settings as unverified, not passed.

## Monitoring evidence required for a release gate

- Bind each decision to the expected release ID, service, environment, traffic scope, metric definitions, UTC time window and freshness limit. Reject a sample from an earlier version or a stale window even if its numeric value appears healthy.
- Require present, parseable **finite numeric** measurements. Missing series, empty arrays, malformed values, `NaN`, infinity, unexpected labels, timeouts and partial telemetry cannot produce a green gate. A shell command exiting zero is not evidence the underlying metric is valid.
- Define the numerator, denominator, units, sample window and minimum traffic. For request error ratio, compute `matching_error_requests / matching_total_requests` over the same interval and label set. A counter rate in errors/second is **not** a percentage; compare rates only when both numerator and denominator rates are compatible. Do not divide by zero. A low-traffic window is **insufficient evidence**, not success.
- Validate and aggregate every relevant series for the intended release. Never inspect only the first response series while silently ignoring other instances, regions or status groups. If labels or series are missing, report coverage and block or escalate according to the approved policy.
- Define alert thresholds, duration, minimum observations, owners and an override/hold policy before promotion. A healthy readiness HTTP response alone does not establish error budgets, functional journeys, data compatibility or safe rollback. Avoid automatic rollback on an unqualified generic health check.

## Recovery and rollback contract

- Verify whether the previous application artefact can still read/write the **current** schema, credentials and external contracts. An incompatible migration or destructive data change can make rollback unsafe even when the old image starts.
- Where rollback is unsafe, block it and use an approved forward-fix, compatible restore, tested backup or other recovery plan. Name the decision owner, data-loss/risk conditions, dependencies, RTO/RPO where relevant and what approval is required.
- After an authorised recovery, verify the actual restored release/version, health, safe data state and at least one critical user journey. Report what was inspected versus what was only proposed; do not assert recovery from a plan.

## Small synthetic Super Skills-only fixture

Use mock responses and in-memory data, without contacting a real provider or writing files. Choose a simulated release `release-B`, a known expected build artefact and runtime start command, an error ratio threshold of 1% and a minimum of 100 representative requests over a recent approved interval.

1. Valid `release-B` data with 2 matching errors / 500 matching requests gives 0.4% and may pass the telemetry criterion only if freshness, coverage, artefact and all other required checks pass.
2. Empty results, missing denominator, zero traffic, 20 requests below the minimum, `NaN`, infinite values and a response with one healthy series plus another unhealthy series must **not** pass.
3. Numeric data for `release-A` or outside the allowed freshness window must block promotion of `release-B`. Error-counter rate `2 per second` must not be mistaken for `2%`.
4. A green health response with a missing build artefact or a runtime start command that expects a different output must not pass release acceptance.
5. Simulate a new incompatible schema after `release-B`. Rollback to `release-A` must be blocked until a compatible recovery path and owner are defined. Record the expected restored version, data checks and one critical journey as outstanding verification, not as an executed restore.

Classify each check as passed in the **synthetic fixture**, failed, blocked, not applicable or unverified. Real CI execution, provider telemetry, alert delivery, deployment promotion and recovery/restore remain unverified unless separately authorised and observed.
