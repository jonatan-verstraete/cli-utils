#!/usr/bin/env python3
"""
find_uiavatar.py
Find all self-closing <UiAvatar ... /> instances in .tsx files under whitelist dirs,
skipping blacklisted folders. Outputs a single text file with all instances.

Usage examples:
  python find_uiavatar.py
  python find_uiavatar.py --root . --whitelist src packages/*/src --output uiavatar_instances.txt
  python find_uiavatar.py --use-gitignore --dedupe --include-location

Notes:
 - Default whitelist: ["src"]
 - Default blacklist: ["node_modules","dist","build",".git",".*"]
 - --use-gitignore loads simple patterns from .gitignore (ignores comments and negations).
 - This uses a regex (non-greedy) to match self-closing tags. Not a full JSX parser.
"""

import os
import re
import argparse
import fnmatch
import glob
from pathlib import Path
from typing import List, Set

DEFAULT_WHITELIST = ["src"]
DEFAULT_BLACKLIST = [
    "node_modules",
    "dist",
    "build",
    ".git",
    ".*",          # hidden files/dirs
    ".venv",
    "__pycache__",
]

# Regex: non-greedy match for <UiAvatar ... /> including newlines
UIAVATAR_RE = re.compile(r"<UiAvatar\b.*?\/>", re.DOTALL)


def load_simple_gitignore_patterns(root: Path) -> List[str]:
    """Load lines from .gitignore as simple patterns.
       This is a best-effort parser: ignores comments and blank lines, ignores negations.
       Does NOT implement full gitignore semantics (e.g., directory vs file rules, ! negation).
    """
    gitignore = root / ".gitignore"
    if not gitignore.exists():
        return []
    patterns = []
    for line in gitignore.read_text(encoding="utf-8", errors="ignore").splitlines():
        s = line.strip()
        if not s or s.startswith("#") or s.startswith("!"):
            continue
        # Normalize trailing slash pattern to match directories more easily:
        if s.endswith("/"):
            s = s + "*"   # so "dist/" -> "dist/*"
        patterns.append(s)
    return patterns


def path_matches_any_pattern(path: str, patterns: List[str]) -> bool:
    """
    Test whether any part of the given path (or the final path string) matches one of the glob-style patterns.
    We check:
      - the full relative path string
      - each path component separately (so "node_modules" catches "/foo/node_modules/bar")
    """
    # Normalize for fnmatch (use posix-style)
    norm = path.replace(os.sep, "/")
    for pat in patterns:
        # try matching both against full path and against each component
        try:
            if fnmatch.fnmatch(norm, pat) or fnmatch.fnmatch(os.path.basename(norm), pat):
                return True
        except Exception:
            # Be robust if somebody passes an invalid pattern
            continue
    # check path components
    parts = norm.split("/")
    for part in parts:
        for pat in patterns:
            if fnmatch.fnmatch(part, pat):
                return True
    return False


def expand_whitelist_roots(root: Path, whitelist_patterns: List[str]) -> List[str]:
    """Expand whitelist patterns (glob-style) under root to concrete folder paths."""
    roots = []
    for pat in whitelist_patterns:
        # Use glob relative to root
        matches = glob.glob(str(root / pat), recursive=True)
        if not matches:
            # also try literal (maybe user passed an existing subdir)
            candidate = root / pat
            if candidate.exists() and candidate.is_dir():
                matches = [str(candidate)]
        for m in matches:
            if os.path.isdir(m):
                roots.append(os.path.abspath(m))
    # dedupe and sort
    return sorted(set(roots))


def find_uiavatar_instances_in_content(content: str) -> List[re.Match]:
    return list(UIAVATAR_RE.finditer(content))


def main():
    ap = argparse.ArgumentParser(description="Find self-closing <UiAvatar ... /> instances in .tsx files.")
    ap.add_argument("--root", default=".", help="Repo root to run from (default: current directory).")
    ap.add_argument("--whitelist", nargs="+", default=DEFAULT_WHITELIST,
                    help="Whitelist folder globs relative to root (default: src). Example: src packages/*/src")
    ap.add_argument("--blacklist", nargs="+", default=DEFAULT_BLACKLIST,
                    help="Blacklist name/patterns to skip (glob-style). Default includes node_modules, dist, .*")
    ap.add_argument("--use-gitignore", action="store_true", help="Also load patterns from .gitignore (best-effort).")
    ap.add_argument("--output", default="uiavatar_instances.txt", help="Output file (default uiavatar_instances.txt).")
    ap.add_argument("--dedupe", action="store_true", help="Deduplicate identical snippets in the output.")
    ap.add_argument("--include-location", action="store_true",
                    help="Prefix each snippet with a comment containing file path and line number.")
    ap.add_argument("--ext", default=".tsx", help="File extension to scan (default .tsx).")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    if args.verbose:
        print(f"[INFO] root: {root}")

    blacklist_patterns = list(args.blacklist)
    if args.use_gitignore:
        gitignore_patterns = load_simple_gitignore_patterns(root)
        if args.verbose:
            print(f"[INFO] loaded {len(gitignore_patterns)} patterns from .gitignore")
        blacklist_patterns.extend(gitignore_patterns)

    if args.verbose:
        print(f"[INFO] whitelist globs: {args.whitelist}")
        print(f"[INFO] blacklist patterns: {blacklist_patterns}")

    search_roots = expand_whitelist_roots(root, args.whitelist)
    if not search_roots:
        print("[WARN] No whitelist directories found. Nothing to do.", flush=True)
        return

    if args.verbose:
        print(f"[INFO] expanded search roots: {search_roots}")

    collected = []  # list of tuples (snippet_str, filepath, line)
    seen_snippets: Set[str] = set()

    for search_root in search_roots:
        for dirpath, dirnames, filenames in os.walk(search_root):
            # mutate dirnames in-place to prune blacklisted folders (speed + correctness)
            # Keep only subdirs that are NOT blacklisted.
            pruned = []
            for d in dirnames:
                candidate_path = os.path.join(dirpath, d)
                rel_candidate = os.path.relpath(candidate_path, start=str(root))
                if path_matches_any_pattern(rel_candidate, blacklist_patterns):
                    if args.verbose:
                        print(f"[SKIP DIR] {candidate_path} (blacklisted)")
                    continue
                pruned.append(d)
            dirnames[:] = pruned

            for fname in filenames:
                if not fname.endswith(args.ext):
                    continue
                file_path = os.path.join(dirpath, fname)
                rel_file_path = os.path.relpath(file_path, start=str(root))
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as fh:
                        content = fh.read()
                except Exception as e:
                    if args.verbose:
                        print(f"[ERROR] reading {file_path}: {e}")
                    continue

                for m in find_uiavatar_instances_in_content(content):
                    snippet = m.group(0)
                    # compute 1-based line number
                    line_no = content.count("\n", 0, m.start()) + 1
                    if args.dedupe:
                        key = snippet
                        if key in seen_snippets:
                            continue
                        seen_snippets.add(key)
                    collected.append((snippet, rel_file_path, line_no))

    # Write output file
    out_path = Path(args.output)
    with open(out_path, "w", encoding="utf-8") as outf:
        for snippet, relpath, line_no in collected:
            if args.include_location:
                # write a comment line with file and line
                outf.write(f"// {relpath}:{line_no}\n")
            # Write the snippet as-is to preserve indentation and formatting
            outf.write(snippet + "\n\n")

    print(f"✅ Done. Found {len(collected)} UiAvatar instances. Wrote to: {out_path}")

if __name__ == "__main__":
    main()
