"""Offline Git and package acceptance tests. Writes only disposable test fixtures."""
import json
import shutil
import subprocess
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

    def test_apply_and_rollback(self):
        target=self.publish()
        self.assertEqual(updater.perform(self.checkout,True,"v2.0.1",target),0)
        self.assertEqual(cmd(self.checkout,"rev-parse","HEAD"),target)
        self.assertEqual(updater.rollback(self.checkout),0)
        self.assert_unchanged()

    def test_check_only(self):
        self.publish()
        self.assertEqual(updater.perform(self.checkout),0)
        self.assert_unchanged()

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

    def test_pin_change_requires_approval(self):
        def change():
            p=self.src/"references/routes.json"
            routes=json.loads(p.read_text())
            item=routes["prompts"][0]
            target=self.src/item["file"]
            target.write_bytes(target.read_bytes()+b"\nApproved fixture change.\n")
            item["git_blob_sha"]=integrity.blob_sha(target.read_bytes())
            p.write_text(json.dumps(routes,indent=2))
        target=self.publish(change)
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
