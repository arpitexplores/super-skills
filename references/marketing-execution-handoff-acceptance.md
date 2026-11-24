# Marketing execution handoff and launch acceptance

Read the complete relevant Master workflow first. For an unpublished campaign comprising paid advertising, one landing page and organic social copy, use complete 8.19, 8.13 and 8.20 as appropriate to each distinct deliverable; use complete 6.2 for opted-in email, 8.21 for explicitly approved publication, or 11.1/11.2 for actual rendered creative. Do not infer that drafting permits delivery, account access or expenditure. This reference is an optional synthetic acceptance example, not another tool or compulsory workflow.

## Synthetic campaign and URL integrity

Use a fictional offer with one paid advert, matching landing-page hero and clear CTA, one native social post and one consent-gated email draft. Keep offer claims factual or marked for owner approval. The example destination `https://example.test/offer?ref=partner&utm_source=old&variant=A#details` must retain `ref=partner`, `variant=A` and `#details` while replacing, not appending a duplicate of, the intended `utm_source`, `utm_medium`, `utm_campaign` and optional `utm_content`. Use standard URL parsing, check encoding and destination behaviour, and do not invent live link receipts.

## Lead identity and deduplicated handoff

Fixture has click `C01`, rejected enquiry `L00`, and accepted enquiry `L01` delivered twice as `callback-1` and a retry `callback-2` with the same stable lead/acceptance identity. Result is **one accepted lead**, not two; the rejected enquiry is not accepted. Preserve separate event receipts for audit, but use an idempotent acceptance key and an authoritative lead ledger or CRM state for counted results. Events, clicks, valid enquiries, qualified leads, confirmed orders and revenue are distinct. If the trusted ledger is missing, report source events as unverified, not confirmed business outcomes.

## Consent and release gates

A consent-withdrawal event for `L01` suppresses subsequent marketing sends and relevant optional tracking according to the applicable policy. Record the withdrawal time and decision; do not assume deletion of records that must legally be retained. The email is a draft until opt-in is confirmed and a send is expressly authorised.

Block campaign launch whenever material conditions are missing: approved offer/pricing/capacity and substantiated claims, use rights and channel policy, accessible destination and functioning CTA, attribution and dedup checks, applicable privacy/consent requirements, named approving owner, authorised platform/account access, **approved spend limit**, and a named monitoring/pause owner. Approval for copy is not approval to publish or spend. An unapproved amount, missing cap or absent release owner must yield **BLOCKED**, even if copy and links look valid. Only claim launched, delivered, measured or sold if corresponding real receipts exist.

## Fresh Super Skills-only audit check

Run one clean **untagged** natural-language campaign brief and a separate fresh **explicit Super Skills** invocation; keep briefs and expected deliverables comparable. Record actual coordinator selection, complete prompt reads and whether the expected skill is selected. If the untagged run skips Super Skills, classify that as a routing failure, not proof that campaign content is unavailable. Do not change selection rules just to force a pass.

In the selected Super Skills-only run produce the four fictional assets, demonstrate query-and-fragment-safe UTM replacement, one accepted lead after duplicate callbacks, suppression after withdrawal, and a blocked release without approval or spend cap. Keep synthetic computations in memory and report exact checks run; no application files, temporary artefacts, providers, accounts, messages, published campaigns or legacy skill activation. Offline acceptance does not prove connected GA4/GTM/CRM ingestion, ad platform acceptance, real delivery or commercial lift.
