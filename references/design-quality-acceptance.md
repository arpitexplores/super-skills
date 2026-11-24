# Rendered interface and accessibility acceptance

Internal supporting guidance for Super Skills. This is part of the one coordinator skill, **not another globally discoverable skill** or a substitute for complete master prompt 5.1, 3.1 or the project's accepted design requirements.

## When to load

Read this entire file after the complete primary master prompt whenever the requested task includes rendered web/app interface QA, visual regression review, responsive or interaction acceptance, accessibility testing or sign-off for a UI change. Relevant primary prompts often include 5.1 for independent tests and 3.1 for implementation; use 9.1 only when the release decision actually includes interface acceptance. For unrelated backend, marketing, documents or simple conceptual replies, do not load it. Apply the relevant checks proportionately and record untested criteria.

## Evidence first

1. Identify actual routes, user journeys, states, target browsers, accessibility level if supplied, viewport widths **and heights**, and permission boundaries. Prioritise real defects over checking every possible rule.
2. Prefer existing, authorised browser tooling such as Chromium DevTools Protocol, Playwright and axe when **already available**. Verify versions and capabilities; never presume access, install dependencies or connect providers without permission.
3. Observe the **rendered** page and interactions. Static source inspection, a successful build, an accessibility tree, a passed axe scan, and screenshots alone are not substitutes for actual visual and keyboard testing. If rendered access is unavailable, report that coverage as unverified.
4. Under a strict no-write instruction, do not create screenshots, traces, recordings, test reports, temporary fixtures, caches, browser profiles, generated assets, build outputs or logs. Check the tools' **launch mechanisms as well as test actions** for default side effects before invoking them. On some shells, here-documents or browser launch wrappers can create transient files before the sandbox or test runner starts. Choose a demonstrated no-write stdin/process approach or skip and disclose; a clean final Git tree does not erase earlier temporary writes. Use in-memory fixtures and intercepted external destinations only where those operations are authorised and genuinely no-write; otherwise skip and disclose.
5. Keep source/live/fixture conditions explicit. Controlled feeds, broken images, fallback fonts, simulated devices and intercepted links do not establish production pricing, actual messaging, screen-reader speech or physical-device outcomes.

## Visual and responsive matrix

- Test user-specified widths; when not specified choose representative narrow/mobile, tablet and desktop widths. Include **short mobile viewport heights**, intermediate breakpoints and landscape/orientation where relevant. Inspect the full page, not just initial document width.
- Check content clipping, horizontal scrolling, sticky/fixed overlays, text wrapping, card grids, navigation drawers, scroll targets, safe-area and zoom/reflow, font loading, text expansion, content variations and empty/loading/error states.
- For every important image-backed heading or button, test image failure/fallback. Check text remains readable on the actual fallback pixels, including gradients, changing image regions and hover/focus states. Inspect sample points rather than relying on one computed foreground/background value.
- Check typography hierarchy, spacing, alignment, hit targets, icon quality, missing assets and consistency with approved design tokens. Note where full-page image or pixel-diff comparison was not possible.
- Check hover, active, selected, expanded, disabled, loading, error and success states wherever applicable. Do not stop after default-state axe or a single desktop screenshot.
- **Reduced motion and high contrast.** When animation or visual themes apply, exercise `prefers-reduced-motion: reduce`, `forced-colors: active` and any supported user contrast preference. Confirm essential information and keyboard focus remain visible, animations respect the setting without removing necessary feedback, and borders/icons/text do not disappear in forced-colour modes. Only claim a real system-level test if the system setting and observed behaviour were actually exercised. Use already available browser emulation where appropriate, without installing tools. See [MDN reduced motion](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Media_queries/Using_for_accessibility) and [MDN forced colours](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/%40media/forced-colors).

## Keyboard, focus and interactions

- Follow a complete **forward and reverse Tab** path on key journeys. Confirm logical order, visible focus, keyboard activation with Enter/Space where appropriate and skip-link destination.
- With sticky/fixed headers and overlays, test **focus not obscured** when tabbing backwards after scroll, opening/closing mobile menus, following in-page links and scrolling to controls. Specifically reproduce short viewport heights. Assess WCAG 2.4.11 when a focused component is entirely hidden.
- Test modals, menus, popovers and dialogs for appropriate focus movement, Escape handling, focus restoration, background interaction and pointer/touch occlusion. Confirm floating chat, cookie banners and help widgets do not intercept navigation or action hit targets.
- Inspect visible focus indication against adjacent light/dark backgrounds, including focus ring clipping. Refer to applicable focus and non-text contrast criteria; do **not** label every numeric ring ratio a confirmed WCAG failure without checking the exact criterion and conditions.
- Check buttons, links, forms, errors, loading, submit and confirmation behaviour; use intercepted destinations where authorised. Never submit payments, send WhatsApp/email, trigger production analytics or contact users merely to complete a read-only audit.
- **Authentication and paste.** Where account login or verification exists, check that username/password/one-time-code inputs support browser or password-manager autofill as appropriate and permit copy/paste; scripts must not defeat those mechanisms. Validate on a controlled test state or permitted test account, never by exposing passwords or authenticating without authority. See [WCAG 2.2 3.3.8 Accessible Authentication](https://www.w3.org/WAI/WCAG22/Understanding/accessible-authentication-minimum.html).
- **Multiple form errors.** Where a form uses a linked error summary, create at least two validation errors in a safe in-memory/stubbed submission. Verify focus or announcement brings the summary to attention as designed, each link reaches the associated field, inline errors match and are programmatically connected to inputs, and the user can correct errors without losing values. A linked summary is a useful pattern, **not an unconditional requirement for every form**. Follow the product's actual form semantics; see [GOV.UK error summary pattern](https://design-system.service.gov.uk/components/error-summary/). Do not submit live data just to exercise this case.

## Accessible semantics and contrast

- Run automated rules such as axe when available **and** manual checks. For comparable before/after or independent runs, record version, rule settings, DOM state, route, breakpoint and fixture; conflicting zero/one violation counts require reconciliation rather than an assumed pass.
- Check heading hierarchy, landmarks, labelled controls, visible link/button text in accessible names (WCAG 2.5.3), image alternative text, decorative SVG exposure, current-page cues and the actual accessibility tree. Unnecessary named decorative graphics are an improvement opportunity, not automatically a standards violation.
- Check normal text contrast **4.5:1**, large text **3:1** under WCAG 1.4.3, with applicable exceptions. Include footer links, hover/visited states, image fallbacks and variable overlays. Check interactive component/indicator contrast under applicable non-text criteria. Measure the actual rendered colours/pixels and state; do not claim exact WCAG conformance from rough image averages.
- Where genuinely available and authorised, test with a real screen reader on a supported platform. An accessibility tree or axe scan is not evidence of spoken announcements. Check error and dynamic status announcements.
- Map an asserted WCAG failure to its specific criterion, tested state and observed barrier; avoid calling missing preferred enhancements failures unless a requirement supports that claim. WCAG 2.2 AA is not a blanket claim from a six-viewport sample.

## Reporting and release decision

For each substantive issue give route/state, viewport width **and height**, steps to reproduce, actual effect, affected user, severity, source or browser evidence, applicable criterion where supported, proposed fix and exact re-test. Separate **observed browser**, **automated**, **source-only**, **simulated** and **unverified**.

Priority follows actual user blockage, accessibility impact, reproducibility and business risk, not solely a scan score. A scan with zero violations is not a clean bill of health. Record negative evidence, false positives, untested conditions and permission refusals. Do not declare launch-ready or visually approved while mandatory tested behaviours fail.

This reference is standalone supporting guidance; it neither requires nor invokes any legacy package, module or script.
