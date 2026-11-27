#!/usr/bin/env python3
"""Explicit versioned Git updates for the public Super Skills package.

Python 3.9+ and Git. No background jobs. No arbitrary source or branch.
"""
from __future__ import annotations
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urlsplit
import validate_super_skills as integrity

TRUSTED_REPOSITORY = "arpitexplores/super-skills"
TRUSTED_BRANCH = "main"
PREVIOUS = "refs/super-skills/previous-good"
LAST = "refs/super-skills/last-update"
FETCHED = "refs/super-skills/fetched-release"
MAIN = "refs/remotes/origin/main"
TAG = re.compile(r"v(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)")
COMMIT = re.compile(r"[a-f0-9]{40}")

class UpdateRefused(Exception):
    pass

class CheckoutFailure(UpdateRefused):
    """A checkout operation failed after mutation may have started."""

def require(ok, message):
    if not ok:
        raise UpdateRefused(message)

def git(root, *args, check=True):
    r = subprocess.run(["git","-C",str(root),"-c","core.hooksPath="+os.devnull,
                        "-c","core.fsmonitor=false","-c","submodule.recurse=false",*args],
                       stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False,
                       env={**os.environ,"GIT_TERMINAL_PROMPT":"0"})
    if check and r.returncode:
        raise UpdateRefused("Git operation failed: "+args[0]+"; check access and repository state")
    return r

def output(root,*args):
    return git(root,*args).stdout.decode("utf-8","strict").strip()

def observe(root, *args):
    try:
        result = git(root, *args, check=False)
        if result.returncode == 0 and not result.stderr:
            return result.stdout.decode("utf-8", "strict").strip()
    except (OSError, UnicodeError):
        pass
    return None

def observed_ref(root, ref):
    listing = observe(root, "for-each-ref", "--format=%(refname) %(objectname)", ref)
    if listing is None:
        return "unknown"
    for line in listing.splitlines():
        name, _, oid = line.partition(" ")
        if name == ref:
            return oid if COMMIT.fullmatch(oid) else "unknown"
    return "missing"

def checkout_failure(root, action, start, target, error):
    head = observe(root, "rev-parse", "--verify", "HEAD") or "unknown"
    status = observe(root, "--no-optional-locks", "status", "--porcelain=v1",
                     "--untracked-files=all", "--ignored")
    worktree = "unknown" if status is None else ("dirty" if status else "clean")
    previous = observed_ref(root, PREVIOUS)
    last = observed_ref(root, LAST)
    return CheckoutFailure(
        f"{action}: {error}\n"
        f"Starting commit: {start}\nIntended commit: {target}\nObserved HEAD: {head}\n"
        f"Worktree: {worktree}\n{PREVIOUS}: {previous}\n{LAST}: {last}"
    )

def trusted_remote(url):
    if url in (f"git@github.com:{TRUSTED_REPOSITORY}", f"git@github.com:{TRUSTED_REPOSITORY}.git",
               f"ssh://git@github.com/{TRUSTED_REPOSITORY}", f"ssh://git@github.com/{TRUSTED_REPOSITORY}.git"):
        return True
    try:
        p=urlsplit(url)
        return (p.scheme=="https" and p.hostname=="github.com" and p.username is None and p.password is None
                and p.port is None and not p.query and not p.fragment
                and p.path in (f"/{TRUSTED_REPOSITORY}",f"/{TRUSTED_REPOSITORY}.git"))
    except ValueError:
        return False

def snapshot(root, commit):
    files={}
    total=0
    for entry in git(root,"ls-tree","-r","-z",commit).stdout.split(b"\0"):
        if not entry:
            continue
        meta, rawpath=entry.split(b"\t",1)
        mode,kind,oid=meta.decode("ascii").split()
        path=rawpath.decode("utf-8","strict")
        require(mode=="100644" and kind=="blob" and integrity.allowed(path),"Unexpected fetched file type/path: "+path)
        size=int(output(root,"cat-file","-s",oid))
        total+=size
        require(size<=integrity.MAX_FILE and total<=integrity.MAX_TOTAL,"Fetched package exceeds size limit")
        files[path]=git(root,"cat-file","blob",oid).stdout
    return files

def verified_tree(root,commit):
    try:
        return integrity.validate(snapshot(root,commit))
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as e:
        raise UpdateRefused("Package validation failed: "+str(e)) from e

def preflight(root):
    root=root.resolve()
    require(Path(output(root,"rev-parse","--show-toplevel")).resolve()==root,"Not the skill's own Git checkout")
    require(output(root,"symbolic-ref","--quiet","--short","HEAD")==TRUSTED_BRANCH,"Expected local main branch")
    require(trusted_remote(output(root,"config","--local","--get","remote.origin.url")) and
            trusted_remote(output(root,"remote","get-url","origin")),"Origin is not the approved public repository")
    require(not output(root,"--no-optional-locks","status","--porcelain=v1","--untracked-files=all"),
            "Local changes or untracked files exist")
    old=output(root,"rev-parse","HEAD")
    try:
        local=integrity.read_local(root)
        integrity.validate(local)
        require(local==snapshot(root,old),"Working package differs from committed package")
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as e:
        raise UpdateRefused("Local package validation failed: "+str(e)) from e
    return old,verified_tree(root,old)

def ancestor(root,a,b):
    return git(root,"merge-base","--is-ancestor",a,b,check=False).returncode==0

def numeric_version(v):
    return tuple(int(x) for x in v.split("-")[0].split("."))

def fetch_candidate(root, remote, old, old_version, tag, commit):
    require(isinstance(tag,str) and TAG.fullmatch(tag) and isinstance(commit,str) and COMMIT.fullmatch(commit),
            "Supply a stable tag and exact 40-character commit")
    git(root,"fetch","--no-tags","--no-recurse-submodules",remote,
        "+refs/heads/main:"+MAIN, "+refs/tags/"+tag+":"+FETCHED)
    target=output(root,"rev-parse",FETCHED+"^{commit}")
    require(target==commit,"Release tag does not match the approved commit")
    require(ancestor(root,target,MAIN),"Release is not on public main")
    require(ancestor(root,old,target),"Upstream is not a fast-forward descendant")
    report=verified_tree(root,target)
    require(report["version"]==tag[1:],"Release version and tag disagree")
    if old!=target:
        require(numeric_version(report["version"])>=numeric_version(old_version),"Downgrade requires recorded rollback")
        require(report["version"]!=old_version,"Same version points to a different commit")
    return target,report

def preview(root, tag, commit):
    old,old_report=preflight(root)
    remote=output(root,"remote","get-url","origin")
    with TemporaryDirectory(prefix="super-skills-preview-") as directory:
        staging=Path(directory)
        git(staging,"init","--bare","--quiet")
        require(trusted_remote(output(staging,"ls-remote","--get-url",remote)),
                "Preview origin is not the approved public repository")
        target,report=fetch_candidate(staging,remote,old,old_report["version"],tag,commit)
        files=output(staging,"diff","--no-ext-diff","--name-only",old,target).splitlines()
    print("Installed version:",old_report["version"],old)
    print("Target release:",tag,target)
    if old==target:
        print("ALREADY CURRENT")
        return 0
    old_pins,new_pins=old_report["pins"],report["pins"]
    changed_pins=sorted(path for path in old_pins.keys()|new_pins.keys() if old_pins.get(path)!=new_pins.get(path))
    print("Changed package files:",len(files))
    print("Changed workflow pins:",len(changed_pins))
    for path in changed_pins:
        print(" ",path)
    print("PREVIEW ONLY: the installation and its Git refs were not changed")
    print("APPROVAL REQUIRED: approve the exact release and any listed workflow pin changes before applying")
    return 0

def perform(root, apply=False, tag=None, commit=None, allow_prompt_changes=False):
    root=root.resolve()
    old,old_report=preflight(root)
    print("Installed version:",old_report["version"],old)
    if not apply:
        require(not tag and not commit and not allow_prompt_changes,"Update arguments require --preview or --apply")
        print("CHECK ONLY: local integrity passed; no remote lookup or change")
        return 0
    target,report=fetch_candidate(root,"origin",old,old_report["version"],tag,commit)
    if old==target:
        print("ALREADY CURRENT")
        return 0
    require(old_report["pins"]==report["pins"] or allow_prompt_changes,"Workflow pins changed; separate approval required")
    again,_=preflight(root)
    require(again==old,"Checkout changed during preflight")
    try:
        git(root,"update-ref",PREVIOUS,old)
        git(root,"merge","--ff-only","--no-edit",target)
        git(root,"update-ref",LAST,target)
        now,actual=preflight(root)
        require(now==target and actual["version"]==report["version"],"Post-update verification failed")
    except (UpdateRefused, OSError, ValueError) as error:
        raise checkout_failure(root, "Update", old, target, error) from error
    print("UPDATED:",old,"->",target)
    print("VALIDATED:",actual["route_count"],"workflows; no newly fetched scripts executed")
    return 0

def rollback(root):
    root=root.resolve()
    current,_=preflight(root)
    last=output(root,"rev-parse","--verify",LAST)
    previous=output(root,"rev-parse","--verify",PREVIOUS)
    require(current==last and ancestor(root,previous,current),"Checkout no longer matches the recorded update")
    verified_tree(root,previous)
    again,_=preflight(root)
    require(again==current,"Checkout changed during rollback preflight")
    try:
        git(root,"reset","--hard",previous)
        actual,_=preflight(root)
        require(actual==previous,"Rollback verification failed")
    except (UpdateRefused, OSError, ValueError) as error:
        raise checkout_failure(root, "Rollback", current, previous, error) from error
    print("ROLLED BACK:",current,"->",previous)
    return 0

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument("--preview",action="store_true")
    mode.add_argument("--apply",action="store_true")
    mode.add_argument("--rollback",action="store_true")
    parser.add_argument("--tag")
    parser.add_argument("--commit")
    parser.add_argument("--allow-prompt-changes",action="store_true")
    args=parser.parse_args()
    root=Path(__file__).resolve().parent.parent
    try:
        if args.preview:
            require(not args.allow_prompt_changes,"--allow-prompt-changes requires --apply")
            return preview(root,args.tag,args.commit)
        if args.rollback:
            require(not args.tag and not args.commit and not args.allow_prompt_changes,"Rollback does not accept update arguments")
            return rollback(root)
        return perform(root,args.apply,args.tag,args.commit,args.allow_prompt_changes)
    except CheckoutFailure as e:
        print("FAILED:",str(e),file=sys.stderr)
        return 2
    except (UpdateRefused, OSError, ValueError, UnicodeError) as e:
        print("REFUSED:",str(e),file=sys.stderr)
        return 2

if __name__=="__main__":
    sys.exit(main())
