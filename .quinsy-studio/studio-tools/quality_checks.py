#!/usr/bin/env python3
"""Quality gate checks (agency integration L5).

hard   a11y_axe      a product with pages has an axe test, and it does not switch rules off
       e2e_hygiene   no `.only`, no fixed sleeps, no forced clicks in browser tests (FE-006)
       api_contract  route handlers validate the body and do not return raw errors (BE-001)
soft   perf_budget   heavy client imports and raw <img> (FE-003)

Each check returns (findings, not_tested_reason). A check with nothing to look at
is NOT TESTED, not a pass.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Callable, Dict, List, Tuple

from security_checks import CODE_SUFFIXES, _app_roots, _line_of, _read, _rel, iter_files

QUALITY_HARD = ("a11y_axe", "e2e_hygiene", "api_contract")
QUALITY_SOFT = ("perf_budget",)

Result = Tuple[List[str], str]

_TEST_FILE = re.compile(r"\.(spec|test)\.(t|j)sx?$")


def _test_files(root: Path) -> List[Path]:
    return [p for base in _app_roots(root) for p in iter_files(base, CODE_SUFFIXES) if _TEST_FILE.search(p.name)]


def _browser_tests(root: Path) -> List[Path]:
    return [p for p in _test_files(root) if re.search(r"@playwright/test|from ['\"]playwright", _read(p))]


def _pages(root: Path) -> List[Path]:
    return [
        p for base in _app_roots(root)
        for p in iter_files(base / "src" / "app", {".tsx", ".jsx"})
        if p.stem == "page" and "(payload)" not in p.parts and "(design-mocks)" not in p.parts
    ]


def a11y_axe(root: Path) -> Result:
    if not _pages(root):
        return [], "no product pages"
    findings: List[str] = []
    axe = [p for p in _test_files(root) if re.search(r"AxeBuilder|@axe-core/|vitest-axe|jest-axe", _read(p))]
    if not axe:
        findings.append("no axe test: add @axe-core/playwright over the smoke routes (FE-004, FE-006)")
    for path in axe:
        text = _read(path)
        for match in re.finditer(r"\.disableRules\(\s*\[[^\]]*\]", text):
            findings.append(f"{_rel(root, path)}:{_line_of(text, match.start())}: axe rules switched off; fix the markup instead")
    return findings, ""


_E2E_SMELLS = (
    (re.compile(r"\b(?:test|describe|it)\.only\s*\("), "`.only` skips the rest of the suite"),
    (re.compile(r"\bwaitForTimeout\s*\("), "fixed sleep; wait for a locator or response"),
    (re.compile(r"force\s*:\s*true"), "forced click hides an overlay or disabled control"),
    (re.compile(r"\b(?:test|it)\.skip\s*\(\s*\)"), "`.skip()` without a reason"),
)


def e2e_hygiene(root: Path) -> Result:
    tests = _test_files(root)
    if not tests:
        return [], "no test files"
    findings: List[str] = []
    for path in tests:
        text = _read(path)
        for pattern, why in _E2E_SMELLS:
            for match in pattern.finditer(text):
                findings.append(f"{_rel(root, path)}:{_line_of(text, match.start())}: {why}")
    return findings, ""


_BODY_READ = re.compile(r"\b(?:req|request)\.(json|formData)\(\)")
_SCHEMA = re.compile(r"\.(?:safeParse|parse|parseAsync|safeParseAsync)\s*\(|\bvalidate\w*\s*\(|\bv\.parse\(")
_RAW_ERROR = re.compile(r"(?:Response|NextResponse)\.json\([^)]*\b(?:err|error|e)\.(?:message|stack)\b")


def api_contract(root: Path) -> Result:
    routes = [
        p for base in _app_roots(root)
        for p in iter_files(base / "src" / "app", CODE_SUFFIXES)
        if p.stem == "route" and "(payload)" not in p.parts
    ]
    if not routes:
        return [], "no route handlers"
    findings: List[str] = []
    for path in routes:
        text = _read(path)
        rel = _rel(root, path)
        if "webhook" in rel.lower():
            continue
        body = _BODY_READ.search(text)
        if body and not _SCHEMA.search(text):
            findings.append(f"{rel}:{_line_of(text, body.start())}: request.{body.group(1)}() without a schema parse (BE-001)")
        for match in _RAW_ERROR.finditer(text):
            findings.append(
                f"{rel}:{_line_of(text, match.start())}: returns the raw error; answer with {{code, message, details, request_id}}"
            )
    return findings, ""


_HEAVY = (
    (re.compile(r"from\s+['\"]moment['\"]"), "moment (use date-fns or Intl)"),
    (re.compile(r"from\s+['\"]lodash['\"]"), "whole lodash (import the function)"),
    (re.compile(r"import\s+\*\s+as\s+\w+\s+from\s+['\"]lucide-react['\"]"), "every lucide icon"),
)
_RAW_IMG = re.compile(r"<img\b")


def perf_budget(root: Path) -> Result:
    files = [p for base in _app_roots(root) for p in iter_files(base / "src", {".tsx", ".jsx"})]
    if not files:
        return [], "no UI source"
    findings: List[str] = []
    for path in files:
        text = _read(path)
        client = bool(re.search(r"^\s*['\"]use client['\"]", text[:400], re.M))
        for pattern, why in _HEAVY:
            for match in pattern.finditer(text):
                if client:
                    findings.append(f"{_rel(root, path)}:{_line_of(text, match.start())}: client bundle pulls {why}")
        for match in _RAW_IMG.finditer(text):
            findings.append(f"{_rel(root, path)}:{_line_of(text, match.start())}: raw <img>; use next/image with sizes (LCP)")
    return findings, ""


CHECKS: Dict[str, Callable[[Path], Result]] = {
    "a11y_axe": a11y_axe,
    "e2e_hygiene": e2e_hygiene,
    "api_contract": api_contract,
    "perf_budget": perf_budget,
}
