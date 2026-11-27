# Super Skills

![Licence: MIT](https://img.shields.io/badge/licence-MIT-green) ![Release](https://img.shields.io/github/v/release/arpitexplores/super-skills)

**One skill. Complete workflows. Practical guidance across your projects.**

Super Skills is an open source Agent Skill for AI coding, product development, design, AI search visibility, marketing and business operations. Install it once rather than managing separate skills for every task.

Describe what you want to accomplish. Super Skills is designed to select the relevant complete workflow and apply its instructions to your project, from planning and research through implementation, testing and optimisation.

## What you can do

- Build websites, SaaS products, full stack applications and reliable APIs.
- Plan products, validate ideas and design user experiences.
- Develop AI applications, agents, RAG systems and data pipelines.
- Improve SEO, AEO, content, marketing campaigns and growth strategies.
- Review security, accessibility, performance and release readiness.
- Manage cloud infrastructure, costs, creative production and automation.

The core skill works with the tools your agent already has. No additional skills, subscriptions or connected accounts are required to use the included guidance. Optional integrations depend on the task and your available tools.

[Install](#installation) · [Example requests](#example-requests) · [Updates and rollback](#updates-and-rollback) · [Workflow catalogue](CATALOGUE.md) · [Release history](CHANGELOG.md)

## Get started

Ask your AI agent:

> Install Super Skills from https://github.com/arpitexplores/super-skills using the latest stable release. Confirm its exact tag and commit, verify the complete package and my agent's skills directory, and ask before installing or replacing anything. Install the complete folder as super-skills and verify discovery in a fresh session. Do not install additional tools or remove other skills.

The core skill needs no extra dependencies or connected accounts. Python and Git are optional maintenance tools.

## Example requests

- Audit my website's technical SEO and AI search visibility without changing files.
- Create a reusable design system for my SaaS dashboard.
- Plan a full-stack feature across the UI, API and database.
- Review my application's authentication and security.
- Prepare a marketing launch plan with measurable goals.
- Design a reliable automation with retries and approval gates.

Describe the outcome naturally, or explicitly select the skill when your agent supports it. Browse the [full workflow catalogue](CATALOGUE.md).

## Installation

Download the [latest stable release](https://github.com/arpitexplores/super-skills/releases/latest) for the recommended installation. Keep the complete folder together, named `super-skills`. The steps below explain how to verify and register it with your agent.

| Agent | User level | Project level |
| --- | --- | --- |
| Codex | `~/.agents/skills/super-skills/` | `.agents/skills/super-skills/` |
| Antigravity | `~/.gemini/config/skills/super-skills/` | `.agents/skills/super-skills/` |

See the official [Codex](https://developers.openai.com/api/reference/cli) and [Antigravity](https://antigravity.google/docs/skills) instructions. Verify the actual client, configured directories, OS home path and reload requirements. User-level installation is suitable for shared use. For project-level use, open the containing project as the active workspace.

### Install from ZIP

1. Choose a stable release tag and confirm its exact commit.
2. Download its source ZIP and extract it in a fresh folder.
3. Review the contents, manifest and complete workflow files. If Python 3.9+ is available, run `python3 -B scripts/validate_super_skills.py --json` from the extracted folder. Stop on mismatch. The manifest checks consistency, not publisher identity.
4. Check existing registrations. With approval, copy the entire folder into the chosen discovery location under the name `super-skills`. Do not merge or overwrite existing folders.
5. Start a fresh session and test natural selection and explicit invocation.

### Git installation

For the optional updater, use a new checkout of the official public repository. Fetch public main and the approved stable tag. Verify the exact peeled tag commit is on public main and set the new local main to that commit. Validate before registering one folder or approved directory link.

## Compatibility and troubleshooting

Super Skills uses the portable Agent Skills format. Installation guidance is available for Codex and Antigravity. Discovery and sampled workflow selection were tested in Codex for v2.1.0; earlier releases included sampled Antigravity discovery and routing checks. Client support, available tools and selection behaviour can vary. See the [release notes](https://github.com/arpitexplores/super-skills/releases) for version-specific compatibility details.

Start a new session and describe your task naturally. You can also use `$super-skills` in Codex or `/super-skills` in Antigravity where supported. If selection differs from what you expect, check the active skills directory and any competing project instructions. Change conflicting preferences only with approval, then retest natural selection and an unrelated question.

### Upgrading from standalone skills

The complete workflows are included in one package; earlier standalone skills are not required. If migrating from an older installation, check any additional tools or integrations you rely on before retiring it. Keep a verified recovery copy and obtain separate approval before removing older or unrelated skills. See the [v2.0.0 release history](https://github.com/arpitexplores/super-skills/releases/tag/v2.0.0) for consolidation details.

## Updates and rollback

For Git installations, the optional updater needs Git and Python 3.9+. It defaults to a local check and never updates automatically. See the [update policy](references/update-policy.md) for exact tag and commit updates, refusal cases and rollback. Changed workflow pins require separate approval.

For ZIP or copied installations, verify a staged replacement first and preserve the prior complete folder outside discovery. Restore it if the update fails. Never merge versions or discard user modifications.

Keep the package directory clean. Git-ignored files are not part of a release; unexpected local files still cause integrity checks to refuse operation.

## Contributing and security

Report reproducible workflow or routing issues with the agent version, request, expected workflow, actual selection, evidence and limitations. Propose focused improvements with a testable acceptance case. Keep one discoverable skill, independent complete workflows, intent-based routing and existing approval boundaries. Avoid bulk imports or unrelated rewrites. Use plain British English where practical.

Contribute only material you can redistribute under MIT or disclose its third-party terms and required notices. Do not submit proprietary client data, credentials or unreviewed executables. Run the read-only validator and offline tests where authorised. Maintainers must regenerate the manifest and affected pins. A passing source check does not prove agent behaviour.

For security issues, use private repository security reporting if enabled or a verified private maintainer channel. Include the affected version, impact and safe reproduction. Never publish confidential data or exploit details. Review scripts, external sources and permissions before use. The skill provides guidance, not privileged access, and does not install dependencies or send data automatically.

## Licence and acknowledgements

Super Skills is released under the [MIT licence](LICENSE). The maintainer has confirmed redistribution rights or necessary permissions for the included workflow and supporting texts, including those developed using supplied research guides. This confirmation is not independent legal certification.

The package contains original workflow texts, coordinator, supporting guidance and standard-library Python helpers, not historical standalone repositories, third-party modules, scripts, design datasets, assets, fonts, models or provider SDKs.

The [optional source register](references/specialist-sources.json) contains research references, not dependencies or grants of rights. Check source-specific licences, attribution, provider terms and asset rights before separate installation or reuse. Retain exact upstream copyright and licence notices for any incorporated material; acknowledgements are not a substitute.

Research influences include [MarketingSkills](https://github.com/coreyhaines31/marketingskills), [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill), [Hallmark](https://github.com/Nutlope/hallmark), [W3C accessibility guidance](https://www.w3.org/WAI/), [MDN](https://developer.mozilla.org/) and [GOV.UK Design System](https://design-system.service.gov.uk/). These acknowledgements do not imply endorsement or bundled content. Product and platform names belong to their respective owners.
