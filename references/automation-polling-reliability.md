# Incremental polling and ambiguous-effect recovery

Use this narrow example with the complete Super Skills workflow 12.1 when an approved workflow polls a changeable external source. It is guidance, not an installed scheduler, connector or claim of live execution.

## Polling contract

1. Define the source's actual ordering, timestamp precision, immutable event ID, page/cursor semantics, retention limit and maximum expected delivery delay. If stable IDs or bounded late-arrival guarantees are absent, say what cannot be guaranteed.
2. Represent event timestamps as UTC instants. Record the scheduler's named timezone separately, plus explicit behaviour for skipped and repeated local times at daylight-saving changes. Never treat a local clock display as a unique event ID.
3. Where supported, page through a stable provider cursor or snapshot. Otherwise order deterministically by `(updated_at_utc, stable_id)` and use the provider's documented tie-break and filter semantics. A timestamp-only `updated_at > last_timestamp` checkpoint can skip distinct records sharing that timestamp. Offset pagination against a changing collection can skip or duplicate rows.
4. Store the poll cursor or high-water mark durably **only after** the covered page or batch is safely processed or its events are durably queued. Resume from the last committed checkpoint after missed runs or worker restarts. Use stable event keys and durable deduplication for overlapping fetches.
5. A composite cursor handles equal timestamps, **not late-arriving events with older timestamps**. Use an appropriately bounded inclusive look-back window with deduplication and periodic reconciliation, or the provider's ingestion/sequence cursor if it reliably captures late arrivals. Document remaining gaps from unbounded delay, expired source retention or unreliable sorting.

## Side effects, approvals and recovery

- Before customer-facing, financial or otherwise consequential writes, bind approval to an immutable operation ID, preview or payload digest, approver, scope and expiry. Reject expired or stale approval when relevant inputs change.
- For a downstream write, persist the operation ID and recovery state before dispatch. Use the destination's idempotency key where supported; otherwise check for an existing durable effect before a retry. A timeout or lost acknowledgement does **not** mean the write failed.
- If the destination cannot be queried and a repeated action risks a duplicate, quarantine the operation, alert the named operator and require reconciliation rather than blindly retrying. Record correlation IDs, attempt limits and what can actually be verified. Do not claim exactly-once delivery without the end-to-end guarantees.

## Small synthetic acceptance fixture

Use harmless, in-memory records and a mock destination. The two source events `(2026-11-01T05:30:00Z, a)` and `(2026-11-01T05:30:00Z, b)` must both be processed despite equal timestamps. `2026-11-01T05:30:00Z` and `2026-11-01T06:30:00Z` both display 01:30 in `America/Toronto` during the autumn clock change, but are different instants. Include one event that arrives late with a timestamp before the committed high-water mark, one missed polling interval, and duplicate page delivery.

Then simulate a worker restart after one mock downstream write succeeded but its acknowledgement was lost. The system must reconcile to **one durable effect**, reject a stale approval, and surface an operator alert if reconciliation cannot establish the outcome. Report which checks actually executed. This fixture is not proof of real provider storage, permissions, scheduling or delivered alerts.
