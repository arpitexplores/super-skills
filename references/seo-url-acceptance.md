# URL-level SEO and AEO acceptance

Use this short checklist after reading the full 7.1 audit or 7.2 implementation master, when the task involves URLs, multilingual links, FAQs or required `llms.txt`. It supplements, never replaces, those complete prompts. Audits remain read-only; implementation requires separate approved scope.

## Inspect each URL, not only aggregate scores

- Record a stable finding ID, source URL, affected target URL, environment, language, expected behaviour, observed status/body or markup, verification method, confidence and recommended correction. Preserve all affected URLs when a rule has more than one failing target. A single global pass score cannot replace URL-level evidence.
- Respect an explicit request cap, robots policy, permissions and redirect budget. Distinguish initial HTML from browser-rendered content. A static or synthetic fixture is not evidence of live indexing, provider eligibility or production behaviour.

## Required `/llms.txt` and target validation

- Check actual HTTP response, final URL, body and whether a valid intended text/Markdown document was served. HTTP 200 on an HTML fallback or error page is **not** a valid presence pass. Content-Type is useful evidence, not the only determinant.
- Extract the file's linked target URLs. Resolve relative paths against the approved production origin and check each important public target, within the authorised request scope, for staging, localhost, preview, private or invented destinations; redirects; status; indexability; and the intended canonical URL. A syntactically valid link or a 100/100 summary score does not prove its destination.
- Preserve the owner's requirement to maintain `/llms.txt` even when a particular platform ignores it. Record inaccessible target checks as **unverified**, not passed. Do not change site content or external settings during a 7.1 audit.

## Language, canonical and hreflang

- On relevant multilingual URLs, inspect self-canonical and the alternate-language cluster. For each declared `hreflang` language and destination, verify the destination's reciprocal link points back to the **original URL with the correct original language code**, not merely any backlink. Confirm that language codes, canonical URLs and intended locale content are coherent. Handle `x-default` separately.
- A reciprocal edge labelled with the wrong language is a failure even when both links exist. Use version-appropriate standards tooling for complete locale, parser or eligibility checking.

## FAQ and keyword evidence

- On relevant public pages, compare visible helpful FAQ questions **and answers** to FAQPage JSON-LD values, including graph or array structures where applicable. Flag missing visible answers, changed wording or unsupported claims with page-specific evidence. Under standing policy, maintain useful FAQ coverage and matching FAQPage markup, but never claim guaranteed rich results.
- Count primary and relevant supporting keyword phrases and variants in the actual accessible page text before and after authorised corrections. Record extraction scope (initial HTML or rendered), denominator, counts, approximate percentage and placement for **each affected URL**, without imposing a universal target density or fabricated performance benefit.

## Small synthetic acceptance fixture

In a fresh Super Skills-only session use harmless fixtures on `.test` domains, not live production calls.

1. An `/llms.txt` response returns HTTP 200 but contains HTML fallback, or Markdown with one link to `preview.example.test`; 7.1 must flag the body or staging target rather than award presence/link validity.
2. Two locale pages, `https://www.example.test/en/info/` and `https://www.example.test/hi/info/`, link to each other, but the Hindi page labels its English backlink `hreflang="hi"` rather than `hreflang="en"`. 7.1 must report the precise affected page and edge.
3. A public FAQ page's visible answer says one thing while FAQPage JSON-LD says another. 7.1 must report the mismatch and both values without inventing eligibility. Include a distinct second URL to verify findings do not collapse into one.
4. 7.2 proposes the smallest authorised fixture corrections, then repeats all checks, showing a per-URL before/after evidence table and approximate keyword counts and denominators. **Do not** edit real sites, accounts or source files as part of this fixture.

Passing these synthetic checks does not prove live search indexing, Search Console/CrUX access, complete robots/JSON-LD standards conformance or rich-result eligibility. Mark inaccessible or unexecuted checks unverified.
