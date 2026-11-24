# Routing boundaries

Use the descriptions in `references/routes.json` to select a plausible owner, then apply these distinctions. The decisive factor is what the user **wants delivered**, not a platform or library name that happens to appear in the request.

## Selection checks

- Identify the end product. Distinguish advice, a finished draft, an editable asset, implemented code, independent verification and a completed external action.
- Observe negative requirements. “Give me hooks, **not footage**” routes to concepts, even though “footage” occurs in the text.
- Separate the requested result from inputs. “Create UGC clips **from these scripts**” requests video production, not merely script writing.
- If the user requests one task, choose one primary ID and read its complete file. An approved prompt may support modest adjacent work without making another workflow compulsory.
- When the request has several independently complete deliverables, use multiple owners sequentially or with a deliberate handoff, preserving an approval gate for each action.
- A brief or unpublished request with meaningful deliverables that fit this catalogue remains eligible for its matching master workflow. Judge by the requested outcome, not length or whether the result will be published. Trivial or unrelated requests need no forced skill invocation.
- If even the final deliverable cannot be identified, ask one targeted question. Do not load many complete prompts just to compensate for ambiguity.
- If the request is outside the catalogue, use available ordinary capabilities without pretending a matching master exists.

## High-risk overlaps

| Requested outcome | Primary | Do not confuse with |
| --- | --- | --- |
| UI screen, working website, accessible interactive carousel | 3.1 | 11.1 static graphic design |
| Visual preferences, reusable interface design tokens | 3.2 | 3.1 implementation |
| Single generated brand image or edit | 8.5 | 11.1 composed graphic |
| Finished editable social carousel, posters, static advertising graphics | 11.1 | 8.20 captions and slide copy; 8.5 standalone image |
| UGC hooks, concepts, scripts or storyboard, **no finished footage** | 8.3 | 8.4 UGC footage |
| Actual talking-head or creator-style UGC clips, even if a script is provided | 8.4 | 8.3 concept creation |
| Non-UGC product launch film, demo or motion graphic | 11.2 | 8.4 creator-style UGC |
| Brand promise, company tagline, positioning | 8.6 | 8.8 company LinkedIn post |
| Personal LinkedIn post or carousel text outline | 8.7 | 8.20 general social writing; 11.1 rendered cards |
| Finished LinkedIn company-page post | 8.8 | 8.6 positioning |
| Organic Reddit community research or replies | 8.1 | 8.20 other social channels |
| Reddit-specific paid advert | 8.2 | 8.19 general paid media |
| General Instagram, TikTok, Threads or multi-channel organic copy | 8.20 | 8.21 live publishing |
| Actual queued, scheduled or published organic posts | 8.21 | 8.20 content creation |
| Multi-platform paid media budget, audience, measurement | 8.19 | 8.21 organic publishing |
| Business-wide marketing plan and roadmap | 8.18 | 8.10 one funnel or 8.20 finished social copy |
| Multi-page finished website copy | 8.17 | 8.13 standalone conversion landing page |
| One finished conversion landing page | 8.13 | 8.17 whole-site content |
| One website article | 8.14 | 8.15 Medium-specific editorial work |
| Technical SEO/AEO diagnosis, no edits | 7.1 | 7.2 approved implementation |
| Authorised implementation of SEO/AEO fixes | 7.2 | 7.1 audit |
| SPF, DKIM, DMARC, MX, DNS or sender-domain configuration | 9.3 | 6.2 email content, compliance and lifecycle |
| Transactional or marketing email content, consent, unsubscribes | 6.2 | 9.3 domain authentication |
| Autonomous agent that can call tools | 4.1 | 4.6 non-agent AI/RAG |
| Model-backed search, retrieval, grounded Q&A without autonomous tools | 4.6 | 4.1 agent execution |
| Independent model evals, judge bias, regression and LLM operations | 4.8 | 4.6 building the AI application; 5.1 general QA |
| General ETL/ELT, data warehouse, business intelligence | 4.7 | 2.3 product activation analytics |
| Product cohorts, adoption, first value and retention | 2.3 | 4.7 data pipelines |
| Backend-only API, database, internal background job or webhook | 4.3 | 4.5 cross-layer feature; 12.1 standalone cross-app workflow |
| Full-stack feature spanning UI, APIs, persistence and tests | 4.5 | 4.3 backend-only work |
| Payments, subscription entitlements, financial provider webhooks | 4.4 | 4.3 generic backend integration |
| Persistent cross-application scheduling and retries | 12.1 | 4.3 internal job; 4.7 data pipeline |
| Cloud infrastructure design, IAM, IaC and CI/CD engineering | 9.4 | 9.1 release readiness; 10.1 cost optimisation |
| Approve and verify production launch | 9.1 | 9.4 infrastructure building |
| Compare infrastructure bills, save costs | 10.1 | 9.4 provisioning |
| Diagnose live incidents and ongoing support | 10.2 | 9.1 launch verification |
| Application authentication, threat modelling, tenant isolation | 4.2 | 9.4 cloud provider configuration |
| Independent website/application acceptance tests | 5.1 | 3.1 design and repair |

For actual rendered UI, accessibility, responsive design or interaction QA, the selected complete master prompt remains primary and the internal `references/design-quality-acceptance.md` adds the required state/keyboard/focus/contrast evidence checklist. This is not a separate skill or a replacement for 5.1 or 3.1.



For a scoped release, CI/CD acceptance, SLO gate or rollback compatibility task, read complete 9.4 and complete 4.3 when backend or schema constraints apply, then consult `references/release-slo-gate-acceptance.md` for build artefact/start-contract, fresh finite telemetry, denominator, minimum traffic, every expected series, stale release and schema rollback safety. This is a source-level acceptance reference, not a tool or live release authorisation.

For technical SEO and AEO URL checks, read complete 7.1 for auditing or 7.2 for authorised implementation, then consult `references/seo-url-acceptance.md` where `llms.txt` targets, multilingual hreflang, page FAQs or per-URL keyword evidence require a concrete acceptance check. This reference supports the SEO/AEO requirements in the complete workflows and does not permit live crawling or edits without approval.
For an approved recurring **incremental polling** workflow, select and read complete 12.1 first, then consult the narrowly scoped `references/automation-polling-reliability.md` for equal timestamps, late arrivals, stable cursors, daylight-saving schedules and ambiguous downstream acknowledgements. It adds an illustrative acceptance fixture, not a required external platform or another master prompt.

For business-wide marketing strategy, read **complete 8.18** first. When customer records are repeated, evidence conflicts, marketing outcomes are double-attributed or pilot traffic is too low for causal claims, consult `references/marketing-evidence-experiment-acceptance.md`. It gives an optional small synthetic acceptance example, not a mandatory framework or account access.

For an unpublished campaign that combines advertising, landing-page copy, social content and opt-in email, read the complete selected 8.19, 8.13, 8.20 and 6.2 workflows as relevant to genuinely distinct deliverables. Where tagged URL integrity, lead-event deduplication, consent withdrawal or launch approval is material, consult `references/marketing-execution-handoff-acceptance.md` for a small synthetic acceptance fixture. This is not permission to send, publish or spend.

## Explicit non-owners

Sound-only production and mobile App Store creative are deferred specialist areas. Do not reactivate them from the source research without approval. Use only the workflows actually listed in this package. Prompt availability is not proof of external tool access.

Repository evaluation, skill maintenance, global skill installation and routing audits are **coordinator tasks** rather than separate business master prompts. A request to install a massive unreviewed catalogue is not approval to run arbitrary scripts or tools.

## What to record in a routing test

Record the user request, the selected ID (or a justified multi-workflow or no-owner decision), why the chosen deliverable owns it, whether the whole Markdown file was opened, and which actions actually happened. Keep proposed and observed results distinct.
