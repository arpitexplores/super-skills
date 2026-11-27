# User-requested updates and rollback

Only the direct official public repository `arpitexplores/super-skills` on GitHub is trusted by this Git updater. The existing installation must be an ordinary clean Git checkout on local `main`, from the approved origin. It must already have the current `super-skills` identity. This is not a migration tool for old standalone skills or another coordinator.

## Local check

`python3 -B scripts/update_super_skills.py`

Checks the installed identity, full package manifest, prompt hashes and clean checkout without network access. A successful check is not proof that a newer release exists.

## Preview a release before asking for approval

For a general update request, check the official public latest stable release. If the user requested a specific release, check that release. Verify the `vX.Y.Z` tag and its exact peeled commit, then run:

`python3 -B scripts/update_super_skills.py --preview --tag <stable-tag> --commit <40-character-commit>`

Preview validates the installed checkout and fetches into a temporary bare repository. It leaves the installed worktree and its Git refs intact. Review the release diff and listed workflow changes, then present a short summary. Ask once for approval of the exact tag and commit and explicit approval of any listed pin changes. Keep routine command output in the technical receipt.

Older updater versions lack `--preview`. For those versions, compare the verified target to the installed commit in an isolated public checkout. Keep `--apply` for the authorised update.

## Apply an explicitly approved release

After approval, run:

`python3 -B scripts/update_super_skills.py --apply --tag <approved-tag> --commit <approved-40-character-commit>`

The updater fetches the named tag and main from the approved origin, rejects a tag/commit mismatch, requires a fast-forward to a commit on public main, checks the complete package with the installed validation code, and refuses a downgrade or unexpected prompt changes. It records the prior good commit and checks the resulting tree. It does not execute newly fetched scripts. No private authentication, arbitrary remote/branch or background schedule is required.

Add `--allow-prompt-changes` only when the user explicitly approved the reviewed pin changes. A refusal still requires investigation before any further apply. If the local tree is dirty, contains unexpected files, has an incompatible identity or fails validation, report and stop. Never stash, reset, bypass the checks, repoint the origin or install a duplicate to force success.

## Checkout failure and rollback

A failure during a checkout change exits nonzero. The report includes the starting and intended commits, observed HEAD, Git worktree status and the two recovery refs. An observation can be unknown, and a recovery ref can be missing. Preserve the checkout and refs for review. The updater performs no automatic retry or rollback.

After an explicit request and explanation of the target, run `python3 -B scripts/update_super_skills.py --rollback`. This checks the saved previous and last-update refs, validates the prior package and refuses if the current checkout is no longer the recorded clean updated commit. It does not restore unrelated files or undo external actions.

Rollback also validates the current package before reset. Unreadable or invalid package data can block rollback even when HEAD is clean and the recovery refs exist. If access can be safely restored, reassess before requesting another rollback. Otherwise preserve the checkout and refs for separately authorised recovery.

Use the Git updater for a Git-backed installation. For a copied or ZIP installation, use the staged replacement and full-folder restoration procedure in README.md. A client without local execution access must report that it cannot perform an update. Do not claim platform compatibility solely from source or unit tests.
