# User-requested updates and rollback

Only the direct official public repository `arpitexplores/super-skills` on GitHub is trusted by this Git updater. The existing installation must be an ordinary clean Git checkout on local `main`, from the approved origin. It must already have the current `super-skills` identity. This is not a migration tool for old standalone skills or another coordinator.

## Local check

`python3 -B scripts/update_super_skills.py`

Checks the installed identity, full package manifest, prompt hashes and clean checkout without network access. A successful check is not proof that a newer release exists.

## Apply an explicitly approved release

Inspect the public releases, choose a stable tag in the form `vX.Y.Z` and verify its exact peeled commit. Present the source, tag, commit and any material changes. After approval, use:

`python3 -B scripts/update_super_skills.py --apply --tag <approved-tag> --commit <approved-40-character-commit>`

The updater fetches the named tag and main from the approved origin, rejects a tag/commit mismatch, requires a fast-forward to a commit on public main, checks the complete package with the installed validation code, and refuses a downgrade or unexpected prompt changes. It records the prior good commit and checks the resulting tree. It does not execute newly fetched scripts. No private authentication, arbitrary remote/branch or background schedule is required.

If prompt bodies or pins change, obtain specific approval after reviewing the diff before rerunning with `--allow-prompt-changes`. Do not use that flag to ignore other errors. If the local tree is dirty, contains unexpected files, has an incompatible identity or fails validation, report and stop. Never stash, reset, bypass the checks, repoint the origin or install a duplicate to force success.

## Rollback

After an explicit request and explanation of the target, run `python3 -B scripts/update_super_skills.py --rollback`. This checks the saved previous and last-update refs, validates the prior package and refuses if the current checkout is no longer the recorded clean updated commit. It does not restore unrelated files or undo external actions.

A copied or ZIP installation cannot use this Git updater. Follow the staged replacement/rollback procedure in README.md. A client without local execution access must report that it cannot perform an update. Do not claim platform compatibility solely from source or unit tests.
