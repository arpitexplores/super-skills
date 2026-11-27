# URL-level SEO and AEO acceptance

Read this complete guide after the full 7.1 audit or 7.2 implementation master. Consult relevant sections for substantial 8.17 SEO content work. It supplements, never replaces, complete workflows and applicable project SEO requirements. Audits remain read-only; implementation, accounts, crawling beyond approved scope and writes require appropriate permission. Apply only relevant criteria.

## Inspect each URL, not only aggregate scores

- Record a stable finding ID, source URL, affected target URL, environment, language, expected behaviour, observed status/body or markup, verification method, confidence and recommended correction. Preserve all affected URLs when a rule has more than one failing target. A single global pass score cannot replace URL-level evidence.
- Respect an explicit request cap, robots policy, permissions and redirect budget. Distinguish initial HTML from browser-rendered content. A static or synthetic fixture is not evidence of live indexing, provider eligibility or production behaviour.

## Applicable criteria and coverage ledger

Identify intended page families and sampled URLs, discovery sources, crawl limits, untested coverage and environment before assessment. Use a compact ledger (criterion, URL or template, expected, observed, evidence method, status, finding ID). Mark every applicable mandatory criterion Pass, Issue, Not assessed/blocked, or justified Not applicable. Group true duplicates by cause but retain each affected URL and its evidence; an unassessed requirement cannot be a pass. Use source and live evidence separately; record redirect hops, actual final response and canonical, intended eligibility versus provider-reported indexed state.

| Area | Applicable checks |
| --- | --- |
| Crawl/index | HTTP status/final URL, redirects, canonical, robots/meta/X-Robots-Tag, sitemap membership, initial/rendered HTML, preview isolation, genuine index evidence if accessible |
| Metadata | Distinct title, description, H1/topic hierarchy, language, canonical; each relevant OG and X/Twitter field including title, description, image, type/card, URL as applicable; verify image response, production origin and intended fallback |
| Content | Keyword counts/density/placement/variants, search intent, missing questions, distinct page value, internal links and evidence for claims |
| Schema | Type, syntax, required properties and visible facts; platform eligibility separate; FAQ questions and answers match |
| Media/performance | Real image content, meaningful alt, decorative/linked image treatment, responsive sizes/loading and lab versus field LCP/INP/CLS |
| Discovery | Required llms.txt, actual crawler access and distinct search/training/user-triggered settings, snippets and effective AI inclusion control; accessible citation/report evidence |
| Conditional | Ecommerce facets/products/offers/shipping and returns, local listings/credentials, international reciprocals, programmatic cohorts, migration, incident or advanced crawl checks |

Before reporting, explicitly account for numerical keyword evidence, required llms.txt and useful FAQ coverage/markup; missing access or data is a limitation, not a defect by itself. Do not use aggregate scores instead of evidence or treat provider-specific non-support as a reason to remove the baseline.

## Required `/llms.txt` and target validation

- Check actual HTTP response, final URL, body and whether a valid intended text/Markdown document was served. HTTP 200 on an HTML fallback or error page is **not** a valid presence pass. Content-Type is useful evidence, not the only determinant.
- Extract the file's linked target URLs. Resolve relative paths against the approved production origin and check each important public target, within the authorised request scope, for staging, localhost, preview, private or invented destinations; redirects; status; indexability; and the intended canonical URL. A syntactically valid link or a 100/100 summary score does not prove its destination.
- Preserve the owner's requirement to maintain `/llms.txt` even when a particular platform ignores it. Record inaccessible target checks as **unverified**, not passed. Do not change site content or external settings during a 7.1 audit.

## Language, canonical and hreflang

- On relevant multilingual URLs, inspect self-canonical and the alternate-language cluster. For each declared `hreflang` language and destination, verify the destination's reciprocal link points back to the **original URL with the correct original language code**, not merely any backlink. Confirm that language codes, canonical URLs and intended locale content are coherent. Handle `x-default` separately.
- A reciprocal edge labelled with the wrong language is a failure even when both links exist. Use version-appropriate standards tooling for complete locale, parser or eligibility checking.

## FAQ and keyword evidence

- On relevant public pages, compare visible helpful FAQ questions **and answers** to FAQPage JSON-LD values, including graph or array structures where applicable. Flag missing visible answers, changed wording or unsupported claims with page-specific evidence. Under standing policy, maintain useful FAQ coverage and matching FAQPage markup, but never claim guaranteed rich results.
- Count primary and relevant supporting phrases/variants in accessible page text before/after authorised corrections. Record URL, initial or rendered extraction, main content versus boilerplate, language/tokenisation, denominator (word count), exact and variant counts, approximate percentage and placement. Define the metric: e.g. 8 exact phrase occurrences / 1,000 words = 0.8% occurrence density; token-weighted density and tool-specific definitions differ. Compare like with like; never fabricate counts. Report a justified page-specific target/range or explain why no defensible target is available.

## Quantitative and practical research

- For meaningful SEO decisions compare current platform documentation, independent studies, credible practitioner results (successes and failures), specialist/community discussions, comparable pages and authorised first-party data. Search across relevant engines, languages, markets and AI discovery platforms. Record evidence date, method/sample, limitations, commercial bias and applicability. Differentiate a technical standard, owner requirement, research-backed technique, industry benchmark, project/competitor target, experiment and unsupported claim. Do not reject evidence solely because a vendor does not prescribe it. Convert it into a recommendation or small authorised experiment.
- Useful starting points, not universal ranking thresholds: [Yoast keyphrase density](https://yoast.com/features/keyphrase-density/) uses 0.5–3% for its free plugin indicator, with phrase-length and sentence matching factors; it is not identical to raw occurrence density. [R032 quality gates](https://github.com/Bhanunamikaze/Agentic-SEO-Skill/blob/445c46c268d947fac25c4b57d38aaf723129fe62/resources/references/quality-gates.md) and [ecommerce template](https://github.com/Bhanunamikaze/Agentic-SEO-Skill/blob/445c46c268d947fac25c4b57d38aaf723129fe62/resources/templates/ecommerce.md) suggest editorial examples such as 500 words for a homepage and 400 for product/category pages; these are practitioner heuristics, not validated ranking minima. Compare actual relevant pages, intent, language, quality and topic coverage before recommending a range. The [Ahrefs cited-page study](https://ahrefs.com/blog/short-vs-long-content-in-ai-overviews/) analysed 174,048 extractable cited pages; 53.4% were under 1,000 words. That sample is not the probability of citation for all pages. Keep useful title/meta/answer length, link and uniqueness guidance with source/context, never pad or stuff.
- [GEO research](https://arxiv.org/abs/2311.09735) reported up to 40% improvement in its experimental visibility metric, varying by domain. Test clear answers, relevant verifiable statistics, primary citations, original evidence and credible quotations. [Ahrefs brand-mention analysis, 3 Nov 2026](https://ahrefs.com/blog/mention-types-ai-visibility/) found Reddit mentions correlated about 0.75 with combined AI brand visibility across 10,000 US brands and 260 million prompts; brand size and selection effects matter, and the vendor sells measurement tools. Explore genuine useful community participation, earned coverage and entity authority; no spam, manufactured claims, correlation-as-causation or fixed citation formula. Verify current findings and other sources as relevant. A transparent content-quality rubric is not a calibrated ranking or citation prediction.

## First-party and AI evidence

Use authorised UI exports or supported least-privilege APIs/connectors when available; no automatic connection. Record property/domain, date windows, dimensions, filters, sample sizes, quotas and data omissions. Search Console Search Analytics returns limited top rows, URL Inspection describes Google's indexed version/selected canonical (not a live fetch), and backlinks need the Links report export or verified provider, not an undocumented API. Bing Webmaster/AI Performance can show citations, grounding queries and topics where available. GA4 measures visits/outcomes under its measurement setup; CrUX field data is not lab data, check URL/origin grain and missing samples. Logs indicate requested routes, statuses and UA strings; verify crawler identity independently when needed. No provider evidence means Not assessed, never invent access.

Check Google Search generative AI inclusion control, including effective inherited property setting, and relevant snippet/crawler settings separately from training access. Verify current provider docs. Compare repeatable queries across relevant Google AI surfaces, Bing, ChatGPT Search, Perplexity or other relevant engines with query, engine, locale, date, settings, brand mentions, cited URLs and competing sources. Use a consistent sample, distinguish no result from failed/unavailable check, and report impressions/citations/visits/business outcomes separately. Do not guarantee future visibility or infer causal impact from one observation.

## Conditional investigation and programme release

- Traffic decline: identify change point and comparable periods; segment pages/templates, queries, devices and markets. Check measurement changes, demand/seasonality, releases, migration map, redirects/canonicals, crawl/index coverage, manual/security issues, competition and content decay. Compare evidence and alternative hypotheses before recommending a scoped remedy. Do not infer causation from a coincident algorithm update. Keep before/after baselines.
- Larger sites: compare sitemap/CMS inventory to reachable link graph; bounded crawls yield orphan candidates, not proof of absence. Cluster normalised exact and near-duplicates with language-aware extraction and bounded comparisons; confirm page purpose before consolidation. Examine deliberate indexable facets versus crawl traps, pagination, content gaps and decay; avoid blanket noindex or page-count rules. Schema diffs, log analysis and competitor samples are evidence leads, not automatic verdicts.
- Local/ecommerce: reconcile business profiles, categories, duplicates, verified credentials, associations, authentic photos, addresses/hours/service areas and visible local schema; identify useful product/service landing pages, comparisons, purchasing, shipping/returns and suitability questions. Do not invent facts, ratings or registrations.
- Programmatic pages: establish demand, data rights, completeness/freshness and meaningful standalone value. Define eligible templates and missing-data exclusions; authorise a small pilot with segmented sitemap, inspect rendering, status/canonical/indexability, internal links, distinct value and matching schema. Agree measurable project-specific stop/expand/rollback criteria, monitor error/index evidence and qualified outcomes, and expand only after approval. Do not use universal uniqueness percentages or location counts as proof of quality. For migrations verify old/new mapping, preserved intent, redirect/canonical/link/sitemap parity and post-launch monitoring.
- For 8.17 map related questions to the page, section, answer format and proof needed: definition, suitability, comparison, steps, cost, purchasing, limitations and evidence. Use observed search/AI results and reader need; retain accurate existing copy and suggest worthwhile new coverage without fabricating facts.

## Small synthetic acceptance fixture

In a fresh Super Skills-only session use harmless fixtures on `.test` domains, not live production calls.

1. An `/llms.txt` response returns HTTP 200 but contains HTML fallback, or Markdown with one link to `preview.example.test`; 7.1 must flag the body or staging target rather than award presence/link validity.
2. Two locale pages, `https://www.example.test/en/info/` and `https://www.example.test/hi/info/`, link to each other, but the Hindi page labels its English backlink `hreflang="hi"` rather than `hreflang="en"`. 7.1 must report the precise affected page and edge.
3. A public FAQ page's visible answer says one thing while FAQPage JSON-LD says another. 7.1 must report the mismatch and both values without inventing eligibility. Include a distinct second URL to verify findings do not collapse into one.
4. 7.2 proposes the smallest authorised fixture corrections, then repeats all checks, showing a per-URL before/after evidence table and approximate keyword counts and denominators. **Do not** edit real sites, accounts or source files as part of this fixture.

5. Include known word/phrase counts, a sourced benchmark and comparable competitor sample; require numerical results, a justified page-specific target, independent/practitioner evidence and explicit correlation versus causation. Include one missing individual social field and two URLs with similar issue labels. Record blocked evidence rather than inventing index/citation results.
6. Add an intentionally indexable facet versus a crawl trap, a small traffic-drop dataset with competing hypotheses, inherited AI setting, and a programmatic pilot with missing data; verify the appropriate conditional decision and stop/expansion criteria. Select representative cases for the changed scope; no forced live calls or exhaustive repeated audits.

Passing these synthetic checks does not prove live search indexing, Search Console/CrUX access, complete robots/JSON-LD standards conformance or rich-result eligibility. Mark inaccessible or unexecuted checks unverified.
