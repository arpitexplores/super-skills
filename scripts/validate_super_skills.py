#!/usr/bin/env python3
"""Read-only package and workflow integrity checks. Python 3.9+, standard library."""
from __future__ import annotations
import hashlib
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = "PACKAGE_MANIFEST.json"
ROOT_FILES = {
    ".gitattributes", ".gitignore",
    "SKILL.md", "VERSION", "LICENSE",
    "README.md", "CATALOGUE.md", "CHANGELOG.md",
    MANIFEST,
}
REQUIRED_REFS = {
    "references/routes.json", "references/routing-rules.md",
    "references/specialist-sources.json", "references/specialist-policy.md",
    "references/update-policy.md", "references/design-quality-acceptance.md",
    "references/automation-polling-reliability.md",
    "references/marketing-evidence-experiment-acceptance.md",
    "references/marketing-execution-handoff-acceptance.md",
    "references/release-slo-gate-acceptance.md", "references/seo-url-acceptance.md",
}
SCRIPTS = {
    "scripts/validate_super_skills.py", "scripts/search_super_skills_guidance.py",
    "scripts/update_super_skills.py", "scripts/test_update_super_skills.py",
}
ISSUES = {
    ".github/ISSUE_TEMPLATE/bug_report.md",
    ".github/ISSUE_TEMPLATE/improvement.md",
}
REQUIRED = ROOT_FILES | REQUIRED_REFS | SCRIPTS
PROMPT = re.compile(r"prompts/[0-9]{2}-[a-z0-9-]+/[0-9]+\.[0-9]+-[a-z0-9-]+\.md")
REFERENCE = re.compile(r"references/[a-z0-9_-]+\.(?:md|json)")
VERSION = re.compile(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)(?:-rc\.[1-9]\d*)?")
CATALOGUE = re.compile(r"(?m)^\* \*\*(\d+\.\d+) [^\n]+?\*\* \[Workflow\]\((prompts/[^)\n]+)\)$")
MAX_FILE = 4 * 1024 * 1024
MAX_TOTAL = 20 * 1024 * 1024

def require(ok, message):
    if not ok:
        raise ValueError(message)

def blob_sha(data):
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()

def allowed(path):
    return path in ROOT_FILES | SCRIPTS | ISSUES or bool(PROMPT.fullmatch(path) or REFERENCE.fullmatch(path))

def read_local(root):
    root = Path(root).resolve()
    files = {}
    total = 0
    for folder, dirs, names in os.walk(root, followlinks=False):
        base = Path(folder)
        if base == root:
            dirs[:] = [d for d in dirs if d != ".git"]
            names = [n for n in names if n != ".git"]
        for name in dirs:
            p = base / name
            require(not p.is_symlink(), "Unexpected symbolic directory: " + p.relative_to(root).as_posix())
        for name in names:
            p = base / name
            rel = p.relative_to(root).as_posix()
            require(allowed(rel), "Unexpected file: " + rel)
            require(p.is_file() and not p.is_symlink(), "Expected ordinary file: " + rel)
            require(p.stat().st_size <= MAX_FILE, "Oversized file: " + rel)
            files[rel] = p.read_bytes()
            total += len(files[rel])
            require(total <= MAX_TOTAL, "Package exceeds size limit")
    return files

def validate(files):
    require(REQUIRED <= files.keys(), "Required package files missing: " + ", ".join(sorted(REQUIRED-files.keys())))
    require(all(allowed(p) for p in files), "Unexpected package path")
    require(all(len(b) <= MAX_FILE for b in files.values()) and sum(map(len, files.values())) <= MAX_TOTAL, "Package exceeds size limit")
    manifest = json.loads(files[MANIFEST])
    require(manifest.get("schema_version") == 1 and isinstance(manifest.get("files"), dict), "Invalid package manifest")
    listed = manifest["files"]
    require(set(listed) == set(files)-{MANIFEST}, "Manifest file set mismatch")
    for path, expected in listed.items():
        require(isinstance(expected, str) and re.fullmatch(r"[a-f0-9]{40}", expected) and blob_sha(files[path]) == expected, "Package hash mismatch: " + path)
    version = files["VERSION"].decode("utf-8").strip()
    require(bool(VERSION.fullmatch(version)), "Invalid version")
    skill = files["SKILL.md"].decode("utf-8")
    header = re.match(r"\A---\n(.*?)\n---\n", skill, re.S)
    require(header is not None, "Missing skill frontmatter")
    head = header.group(1)
    require(re.search(r"(?m)^name: super-skills$", head) is not None, "Unexpected skill identity")
    require(re.search(r"(?m)^license: MIT$", head) is not None, "Missing MIT metadata")
    require(f'  version: "{version}"' in head.splitlines(), "Version metadata mismatch")
    desc = re.search(r'(?m)^description: "([^"\n]+)"$', head)
    require(desc is not None and 1 <= len(desc.group(1)) <= 1024, "Invalid discovery description")
    routes = json.loads(files["references/routes.json"])
    require(routes.get("schema_version") == 2 and routes.get("catalogue_name") == "Super Skills", "Unsupported route schema")
    items = routes.get("prompts")
    require(isinstance(items, list) and len(items) == 53, "Expected 53 complete workflows")
    registry = json.loads(files["references/specialist-sources.json"])
    require(isinstance(registry.get("sources"), list), "Invalid specialist registry")
    refs = [x["id"] for x in registry["sources"]]
    require(len(refs)==len(set(refs)) and not {"R010","R011"} & set(refs) and all(re.fullmatch(r"R\d{3}",x) for x in refs), "Invalid specialist IDs")
    pins = {}
    ids = set()
    links = {}
    for item in items:
        require(isinstance(item, dict) and set(item)=={"id","title","intent","file","git_blob_sha","optional_external_sources"}, "Invalid route record")
        ident, path = item["id"], item["file"]
        require(isinstance(ident,str) and re.fullmatch(r"\d+\.\d+",ident) and ident not in ids, "Invalid or duplicate workflow ID")
        require(isinstance(path,str) and PROMPT.fullmatch(path) and path not in pins and path in files, "Invalid, duplicate or missing workflow path")
        require(Path(path).name.startswith(ident+"-") and int(path.split("/")[1][:2])==int(ident.split(".")[0]), "Workflow ID/path mismatch")
        require(all(isinstance(item[k],str) and item[k].strip() for k in ("title","intent")), "Empty workflow metadata")
        optional = item["optional_external_sources"]
        require(isinstance(optional,list) and all(isinstance(x,str) and x in refs for x in optional), "Unresolved optional source: "+ident)
        require(len(files[path])>=500 and blob_sha(files[path])==item["git_blob_sha"], "Workflow hash mismatch: "+ident)
        ids.add(ident); pins[path]=item["git_blob_sha"]; links[ident]=path
    require({p for p in files if p.startswith("prompts/")}==set(pins), "Workflow file set mismatch")
    require(len({i.split(".")[0] for i in ids})==12, "Expected 12 workflow categories")
    rows = CATALOGUE.findall(files["CATALOGUE.md"].decode("utf-8"))
    require(len(rows)==53 and dict(rows)==links, "Catalogue route mismatch")
    for path in re.findall(r"(?:references|scripts)/[a-z0-9_/-]+\.(?:md|json|py)",skill):
        require(path in files, "Missing coordinator reference: "+path)
    return {"ok":True,"version":version,"route_count":len(ids),"prompt_files":len(pins),"package_files":len(files),"pins":pins}

def main():
    try:
        result = validate(read_local(ROOT))
        result.pop("pins",None)
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as e:
        result = {"ok":False,"problems":[str(e)]}
    if "--json" in sys.argv:
        print(json.dumps(result,indent=2))
    else:
        print("PASS" if result["ok"] else "FAIL")
        print(json.dumps(result,indent=2))
    return 0 if result["ok"] else 1

if __name__ == "__main__":
    sys.exit(main())
