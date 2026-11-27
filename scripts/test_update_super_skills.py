"""Offline Git and package acceptance tests. Writes only disposable test fixtures."""
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import validate_super_skills as integrity
import update_super_skills as updater

ROOT=Path(__file__).resolve().parent.parent

def cmd(root,*args):
    return subprocess.run(["git","-C",str(root),*args],check=True,capture_output=True,text=True).stdout.strip()

def manifest(root):
    files=integrity.read_local(root)
    files.pop(integrity.MANIFEST,None)
    (root/integrity.MANIFEST).write_text(json.dumps({"schema_version":1,"files":{p:integrity.blob_sha(b) for p,b in sorted(files.items())}},indent=2)+"\n",encoding="utf-8")

def set_version(root,new):
    old=(root/"VERSION").read_text().strip()
    (root/"VERSION").write_text(new+"\n")
    skill=root/"SKILL.md"
    skill.write_text(skill.read_text().replace(f'version: "{old}"',f'version: "{new}"'))

class PackageTest(unittest.TestCase):
    def test_real_package(self):
        self.assertEqual(integrity.validate(integrity.read_local(ROOT))["route_count"],53)

    def test_missing_and_changed_file(self):
        files=integrity.read_local(ROOT)
        files.pop("LICENSE")
        with self.assertRaises(ValueError):
            integrity.validate(files)
        files=integrity.read_local(ROOT)
        files["README.md"]+=b"tampered"
        with self.assertRaises(ValueError):
            integrity.validate(files)

    def test_unknown_route_source_even_with_refreshed_manifest(self):
        files=integrity.read_local(ROOT)
        routes=json.loads(files["references/routes.json"])
        routes["prompts"][0]["optional_external_sources"]=["R999"]
        files["references/routes.json"]=json.dumps(routes).encode()
        files[integrity.MANIFEST]=json.dumps({"schema_version":1,"files":{p:integrity.blob_sha(b) for p,b in files.items() if p!=integrity.MANIFEST}}).encode()
        with self.assertRaisesRegex(ValueError,"Unresolved optional"):
            integrity.validate(files)

    def test_origin_allowlist(self):
        for value in ("https://github.com/arpitexplores/super-skills.git","git@github.com:arpitexplores/super-skills.git"):
            self.assertTrue(updater.trusted_remote(value))
        for value in ("https://github.com/arpitexplores/skills-super","https://github.com/example-org/another-skill",
                      "https://github.com.evil.test/arpitexplores/super-skills","https://user@github.com/arpitexplores/super-skills",
                      "file:///tmp/fake","https://github.com:444/arpitexplores/super-skills"):
            self.assertFalse(updater.trusted_remote(value))

class UpdateTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        base=Path(self.tmp.name)
        self.remote=base/"remote.git"
        self.src=base/"source"
        self.checkout=base/"installation"
        self.src.mkdir()
        cmd(base,"init","--bare",str(self.remote))
        for path,data in integrity.read_local(ROOT).items():
            p=self.src/path
            p.parent.mkdir(parents=True,exist_ok=True)
            p.write_bytes(data)
        set_version(self.src,"2.0.0")
        manifest(self.src)
        cmd(self.src,"init","-b","main")
        cmd(self.src,"config","user.name","Fixture")
        cmd(self.src,"config","user.email","fixture@example.test")
        cmd(self.src,"add","-A")
        cmd(self.src,"commit","-m","Initial")
        cmd(self.src,"tag","v2.0.0")
        cmd(self.src,"remote","add","origin",str(self.remote))
        cmd(self.src,"push","origin","main","--tags")
        cmd(base,"clone","--branch","main",str(self.remote),str(self.checkout))
        self.first=cmd(self.checkout,"rev-parse","HEAD")
        p=patch.object(updater,"trusted_remote",side_effect=lambda url:url==str(self.remote))
        p.start(); self.addCleanup(p.stop)

    def publish(self, change=None, refresh=True):
        set_version(self.src,"2.0.1")
        if change:
            change()
        if refresh:
            manifest(self.src)
        cmd(self.src,"add","-A")
        cmd(self.src,"commit","-m","New version")
        cmd(self.src,"tag","v2.0.1")
        cmd(self.src,"push","origin","main","--tags")
        return cmd(self.src,"rev-parse","HEAD")

    def assert_unchanged(self):
        self.assertEqual(cmd(self.checkout,"rev-parse","HEAD"),self.first)

    def run_cli(self, *args):
        stdout, stderr = StringIO(), StringIO()
        script = self.checkout / "scripts" / "update_super_skills.py"
        with patch.object(updater, "__file__", str(script)), patch.object(sys, "argv", [str(script), *args]), \
                redirect_stdout(stdout), redirect_stderr(stderr):
            return updater.main(), stdout.getvalue(), stderr.getvalue()

    def assert_failed_checkout(self, result, cause, start, intended, observed, worktree, *, previous, last):
        code, stdout, stderr = result
        self.assertEqual(code, 2)
        self.assertNotIn("UPDATED:", stdout)
        self.assertNotIn("ROLLED BACK:", stdout)
        self.assertEqual(stderr.splitlines(), [
            f"FAILED: {cause}", f"Starting commit: {start}", f"Intended commit: {intended}",
            f"Observed HEAD: {observed}", f"Worktree: {worktree}",
            f"{updater.PREVIOUS}: {previous}", f"{updater.LAST}: {last}",
        ])

    def test_apply_and_rollback(self):
        def replace_validator():
            (self.src / "scripts" / "validate_super_skills.py").write_text("raise SystemExit(41)\n")
        target=self.publish(replace_validator)
        self.assertEqual(updater.perform(self.checkout,True,"v2.0.1",target),0)
        self.assertEqual(cmd(self.checkout,"rev-parse","HEAD"),target)
        self.assertEqual(updater.rollback(self.checkout),0)
        self.assert_unchanged()

    def test_post_update_validation_failure_and_recovery_preflight(self):
        target = self.publish()
        read_local = integrity.read_local

        def invalid_read(root):
            files = read_local(root)
            if files["VERSION"].strip() == b"2.0.1":
                files["README.md"] += b"invalid package read"
            return files

        with patch.object(integrity, "read_local", invalid_read):
            result = self.run_cli("--apply", "--tag", "v2.0.1", "--commit", target)
            self.assert_failed_checkout(
                result, "Update: Local package validation failed: Package hash mismatch: README.md",
                self.first, target, target, "clean", previous=self.first, last=target,
            )
            code, _, stderr = self.run_cli("--rollback")
            self.assertEqual(code, 2)
            self.assertTrue(stderr.startswith("REFUSED: Local package validation failed: "))
            self.assertEqual(cmd(self.checkout, "rev-parse", "HEAD"), target)
        self.assertEqual(updater.rollback(self.checkout), 0)
        self.assert_unchanged()

    def test_last_update_reference_failure_after_merge(self):
        target = self.publish()
        git = updater.git

        def fail_last_ref(root, *args, **kwargs):
            if args[:2] == ("update-ref", updater.LAST):
                raise updater.UpdateRefused("fixture last-update write failed")
            return git(root, *args, **kwargs)

        with patch.object(updater, "git", fail_last_ref):
            result = self.run_cli("--apply", "--tag", "v2.0.1", "--commit", target)
        self.assert_failed_checkout(
            result, "Update: fixture last-update write failed",
            self.first, target, target, "clean", previous=self.first, last="missing",
        )
        self.assertEqual(cmd(self.checkout, "rev-parse", "HEAD"), target)

    def test_failure_after_rollback_reset(self):
        target = self.publish()
        self.assertEqual(updater.perform(self.checkout, True, "v2.0.1", target), 0)
        git = updater.git

        def edit_after_reset(root, *args, **kwargs):
            result = git(root, *args, **kwargs)
            if args[0] == "reset":
                (root / "README.md").write_text("fixture local change")
            return result

        with patch.object(updater, "git", edit_after_reset):
            result = self.run_cli("--rollback")
        self.assert_failed_checkout(
            result, "Rollback: Local changes or untracked files exist",
            target, self.first, self.first, "dirty", previous=self.first, last=target,
        )
        self.assert_unchanged()
        self.assertEqual((self.checkout / "README.md").read_text(), "fixture local change")

    def test_unavailable_checkout_inspection(self):
        target = self.publish()
        git = updater.git
        merge_attempted = False

        def fail_inspection(root, *args, **kwargs):
            nonlocal merge_attempted
            if args[0] == "merge":
                git(root, *args, **kwargs)
                merge_attempted = True
                raise OSError("fixture failure after merge")
            if merge_attempted and (args == ("rev-parse", "--verify", "HEAD")
                                    or args[:2] == ("--no-optional-locks", "status")):
                raise PermissionError("fixture checkout inspection denied")
            if args[0] == "for-each-ref" and args[-1] == updater.PREVIOUS:
                return subprocess.CompletedProcess(args, 0, b"", b"fixture reference read warning")
            return git(root, *args, **kwargs)

        with patch.object(updater, "git", fail_inspection):
            result = self.run_cli("--apply", "--tag", "v2.0.1", "--commit", target)
        self.assert_failed_checkout(
            result, "Update: fixture failure after merge",
            self.first, target, "unknown", "unknown", previous="unknown", last="missing",
        )
        self.assertEqual(cmd(self.checkout, "rev-parse", "HEAD"), target)
        self.assertEqual(cmd(self.checkout, "rev-parse", updater.PREVIOUS), self.first)

    def test_check_only(self):
        self.publish()
        self.assertEqual(updater.perform(self.checkout),0)
        self.assert_unchanged()

    def checkout_state(self):
        return {str(path.relative_to(self.checkout)): path.read_bytes()
                for path in self.checkout.rglob("*") if path.is_file()}

    def test_preview_without_pin_changes_does_not_apply(self):
        def replace_validator():
            (self.src / "scripts" / "validate_super_skills.py").write_text("raise SystemExit(41)\n")

        target = self.publish(replace_validator)
        before = self.checkout_state()
        code, stdout, stderr = self.run_cli("--preview", "--tag", "v2.0.1", "--commit", target)
        self.assertEqual((code, stderr), (0, ""))
        self.assertIn("Target release: v2.0.1 " + target, stdout)
        self.assertIn("Changed workflow pins: 0", stdout)
        self.assertIn("PREVIEW ONLY", stdout)
        self.assertEqual(self.checkout_state(), before)

    def test_preview_reports_pin_changes_and_refuses_wrong_commit(self):
        target = self.publish(self.change_workflow_pin)
        before = self.checkout_state()
        code, stdout, stderr = self.run_cli("--preview", "--tag", "v2.0.1", "--commit", target)
        self.assertEqual((code, stderr), (0, ""))
        self.assertIn("Changed workflow pins: 1", stdout)
        self.assertIn("prompts/01-client-engagement-commercial/1.1-", stdout)
        code, _, stderr = self.run_cli("--preview", "--tag", "v2.0.1", "--commit", self.first)
        self.assertEqual(code, 2)
        self.assertIn("Release tag does not match", stderr)
        self.assertEqual(self.checkout_state(), before)

    def test_wrong_commit(self):
        self.publish()
        with self.assertRaisesRegex(updater.UpdateRefused,"does not match"):
            updater.perform(self.checkout,True,"v2.0.1",self.first)
        self.assert_unchanged()

    def test_dirty_checkout(self):
        target=self.publish()
        (self.checkout/"README.md").write_text("local change")
        with self.assertRaisesRegex(updater.UpdateRefused,"Local changes"):
            updater.perform(self.checkout,True,"v2.0.1",target)
        self.assert_unchanged()

    def test_invalid_manifest(self):
        target=self.publish(refresh=False)
        with self.assertRaisesRegex(updater.UpdateRefused,"hash mismatch"):
            updater.perform(self.checkout,True,"v2.0.1",target)
        self.assert_unchanged()

    def test_previous_identity_refused(self):
        def change():
            p=self.src/"SKILL.md"
            p.write_text(p.read_text().replace("name: super-skills","name: another-skill"))
        target=self.publish(change)
        with self.assertRaisesRegex(updater.UpdateRefused,"identity"):
            updater.perform(self.checkout,True,"v2.0.1",target)
        self.assert_unchanged()

    def change_workflow_pin(self):
        routes_path = self.src / "references/routes.json"
        routes = json.loads(routes_path.read_text())
        item = routes["prompts"][0]
        target = self.src / item["file"]
        target.write_bytes(target.read_bytes() + b"\nApproved fixture change.\n")
        item["git_blob_sha"] = integrity.blob_sha(target.read_bytes())
        routes_path.write_text(json.dumps(routes, indent=2))

    def test_pin_change_requires_approval(self):
        target=self.publish(self.change_workflow_pin)
        with self.assertRaisesRegex(updater.UpdateRefused,"pins changed"):
            updater.perform(self.checkout,True,"v2.0.1",target)
        self.assert_unchanged()
        self.assertEqual(updater.perform(self.checkout,True,"v2.0.1",target,True),0)

    def test_rollback_refuses_unrecorded_head(self):
        with self.assertRaises(updater.UpdateRefused):
            updater.rollback(self.checkout)
        self.assert_unchanged()

    def test_ignored_collision_refused(self):
        target=self.publish()
        exclude=self.checkout/".git/info/exclude"
        exclude.write_text("extra.txt\n")
        (self.checkout/"extra.txt").write_text("local file")
        with self.assertRaisesRegex(updater.UpdateRefused,"Unexpected file"):
            updater.perform(self.checkout,True,"v2.0.1",target)
        self.assert_unchanged()
        self.assertEqual((self.checkout/"extra.txt").read_text(),"local file")

if __name__=="__main__":
    unittest.main(verbosity=2)
