#!/usr/bin/env python3
"""Run portable baseline checks for the Universal Engineering Skill.

This checker is intentionally dependency-free. It is a first gate, not a
replacement for project-specific builds, tests, SAST, license scanning, or
human design review.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class Finding:
    rule_id: str
    severity: str
    message: str
    path: str = ""
    line: int | None = None

    def as_dict(self) -> dict[str, object]:
        return {
            "rule": self.rule_id,
            "severity": self.severity,
            "message": self.message,
            "path": self.path,
            "line": self.line,
        }


SEVERITIES = {"blocker", "error", "warning", "info"}
EVIDENCE_STATUSES = {"PASS", "FAIL", "NOT_RUN", "BLOCKED", "WAIVED", "UNKNOWN"}
TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".cfg",
    ".conf",
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".java",
    ".kt",
    ".cs",
    ".cpp",
    ".cc",
    ".cxx",
    ".h",
    ".hpp",
    ".c",
    ".go",
    ".rs",
    ".swift",
    ".sh",
    ".ps1",
    ".bat",
    ".cmd",
}
IGNORED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "build",
    "out",
    "dist",
    "target",
    "__pycache__",
}
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(
        r"(?i)\b(?:api[_-]?key|access[_-]?token|secret[_-]?key|client[_-]?secret)"
        r"\s*[:=]\s*['\"][^'\"]{12,}['\"]"
    ),
    re.compile(
        r"(?i)\b(?:password|passwd|authorization)\s*[:=]\s*['\"][^'\"]{12,}['\"]"
    ),
)
PLACEHOLDER_WORDS = {
    "changeme",
    "change-me",
    "example",
    "placeholder",
    "redacted",
    "dummy",
    "test",
    "fake",
    "your-token",
    "your_api_key",
}


def relative_path(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def iter_files(root: Path, suffixes: set[str] | None = None) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        if suffixes is not None and path.suffix.lower() not in suffixes:
            continue
        yield path


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def load_rules(root: Path, findings: list[Finding]) -> list[dict[str, object]]:
    rules_path = root / "automation" / "engineering-gate-rules.json"
    try:
        payload = json.loads(rules_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        findings.append(
            Finding("RULE-001", "error", f"Cannot parse rule file: {exc}", relative_path(rules_path, root))
        )
        return []
    rules = payload.get("rules")
    if not isinstance(rules, list):
        findings.append(Finding("RULE-001", "error", "Rule file must contain a rules array.", relative_path(rules_path, root)))
        return []
    for index, rule in enumerate(rules):
        if not isinstance(rule, dict):
            findings.append(Finding("RULE-001", "error", f"Rule {index} is not an object.", relative_path(rules_path, root)))
            continue
        missing = [key for key in ("id", "severity", "scope", "check", "description") if not rule.get(key)]
        if missing:
            findings.append(
                Finding("RULE-001", "error", f"Rule {index} is missing: {', '.join(missing)}.", relative_path(rules_path, root))
            )
        if rule.get("severity") not in SEVERITIES:
            findings.append(
                Finding("RULE-001", "error", f"Rule {index} has invalid severity.", relative_path(rules_path, root))
            )
    return rules


def check_frontmatter(root: Path, findings: list[Finding]) -> None:
    path = root / "SKILL.md"
    text = read_text(path)
    if text is None:
        findings.append(Finding("SKILL-001", "blocker", "SKILL.md is missing or not UTF-8.", "SKILL.md"))
        return
    if not re.match(r"\A---\r?\n.*?\r?\n---(?:\r?\n|$)", text, re.DOTALL):
        findings.append(Finding("SKILL-001", "blocker", "SKILL.md has no closed frontmatter block.", "SKILL.md"))


def check_version_consistency(root: Path, findings: list[Finding]) -> None:
    version_path = root / "VERSION"
    manifest_path = root / "skill-manifest.json"
    skill_path = root / "SKILL.md"
    try:
        version = version_path.read_text(encoding="utf-8").strip()
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        skill = skill_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        findings.append(Finding("VERSION-001", "error", f"Cannot read Skill version metadata: {exc}"))
        return
    frontmatter_match = re.match(r"\A---\r?\n(.*?)\r?\n---", skill, re.DOTALL)
    frontmatter = frontmatter_match.group(1) if frontmatter_match else ""
    manifest_version = str(manifest.get("version", ""))
    skill_version_match = re.search(r"(?m)^version:\s*([^\s#]+)", frontmatter)
    skill_version = skill_version_match.group(1) if skill_version_match else ""
    if not version or version != manifest_version or (skill_version and version != skill_version):
        findings.append(
            Finding(
                "VERSION-001",
                "error",
                f"Version mismatch: VERSION={version!r}, manifest={manifest_version!r}, optional SKILL.md={skill_version!r}.",
            )
        )


def check_markdown_links(root: Path, findings: list[Finding]) -> None:
    link_pattern = re.compile(r"\]\(([^)]+)\)")
    for path in iter_files(root, {".md"}):
        text = read_text(path)
        if text is None:
            continue
        for line_number, line in enumerate(text.splitlines(), 1):
            for match in link_pattern.finditer(line):
                target = match.group(1).strip()
                if (
                    not target
                    or target.startswith(("#", "http://", "https://", "mailto:", "<"))
                    or target.startswith("data:")
                ):
                    continue
                target = target.split("#", 1)[0].strip("<>")
                if not target.lower().endswith(".md"):
                    continue
                candidate = (path.parent / target).resolve()
                try:
                    candidate.relative_to(root.resolve())
                except ValueError:
                    findings.append(
                        Finding("DOC-001", "error", f"Markdown link escapes root: {target}", relative_path(path, root), line_number)
                    )
                    continue
                if not candidate.exists():
                    findings.append(
                        Finding("DOC-001", "error", f"Missing Markdown link target: {target}", relative_path(path, root), line_number)
                    )


def looks_like_placeholder(value: str) -> bool:
    normalized = value.lower().replace(" ", "-")
    return normalized in PLACEHOLDER_WORDS or normalized.startswith("your-")


def check_secret_patterns(root: Path, findings: list[Finding]) -> None:
    for path in iter_files(root, TEXT_SUFFIXES):
        text = read_text(path)
        if text is None:
            continue
        for line_number, line in enumerate(text.splitlines(), 1):
            lowered = line.lower()
            if any(word in lowered for word in ("example", "placeholder", "redacted", "dummy", "fake")):
                continue
            for pattern in SECRET_PATTERNS:
                match = pattern.search(line)
                if not match:
                    continue
                snippet = match.group(0)
                if looks_like_placeholder(snippet):
                    continue
                findings.append(
                    Finding("SEC-001", "blocker", "Possible credential or private key in text.", relative_path(path, root), line_number)
                )
                break


def check_evidence_status(root: Path, findings: list[Finding]) -> None:
    status_pattern = re.compile(r"(?i)\b(NOT_RUN|BLOCKED|UNKNOWN)\b.{0,80}\bPASS(?:ED)?\b")
    reverse_pattern = re.compile(r"(?i)\bPASS(?:ED)?\b.{0,80}\b(NOT_RUN|BLOCKED|UNKNOWN)\b")
    evidence_context = re.compile(
        r"(?i)^\s*(?:[-*]\s*)?(?:[\"`']?"
        r"(?:status|result|evidence|verification|验收|结果|证据|通过|状态)"
        r"[\"`']?)\s*[:|]"
    )
    for path in iter_files(root, {".md", ".txt", ".json", ".yaml", ".yml"}):
        text = read_text(path)
        if text is None:
            continue
        for line_number, line in enumerate(text.splitlines(), 1):
            # Do not flag instructional prose such as "NOT_RUN cannot be PASS".
            # Evidence records normally have a status/result field or a table row.
            is_record = evidence_context.search(line) is not None
            if is_record and (status_pattern.search(line) or reverse_pattern.search(line)):
                findings.append(
                    Finding(
                        "EVIDENCE-001",
                        "error",
                        "Evidence line mixes PASS with NOT_RUN, BLOCKED or UNKNOWN.",
                        relative_path(path, root),
                        line_number,
                    )
                )


def check_evidence_file(root: Path, evidence_path: Path, findings: list[Finding]) -> None:
    schema_path = root / "automation" / "evidence-schema.json"
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        findings.append(Finding("EVIDENCE-002", "error", f"Cannot parse evidence or schema: {exc}", relative_path(evidence_path, root)))
        return
    required_top_level = schema.get("required_top_level", [])
    missing_top_level = [key for key in required_top_level if key not in evidence]
    if missing_top_level:
        findings.append(
            Finding(
                "EVIDENCE-002",
                "error",
                f"Evidence is missing top-level fields: {', '.join(missing_top_level)}.",
                relative_path(evidence_path, root),
            )
        )
    stages = evidence.get("stages")
    if not isinstance(stages, list) or not stages:
        findings.append(Finding("EVIDENCE-002", "error", "Evidence must contain a non-empty stages array.", relative_path(evidence_path, root)))
        return
    required_stage_fields = schema.get("required_stage_fields", [])
    required_check_fields = schema.get("required_check_fields", [])
    for index, stage in enumerate(stages):
        if not isinstance(stage, dict):
            findings.append(Finding("EVIDENCE-002", "error", f"Stage {index} is not an object.", relative_path(evidence_path, root)))
            continue
        missing = [key for key in required_stage_fields if key not in stage]
        if missing:
            findings.append(Finding("EVIDENCE-002", "error", f"Stage {index} is missing: {', '.join(missing)}.", relative_path(evidence_path, root)))
        status = stage.get("status")
        if status not in EVIDENCE_STATUSES:
            findings.append(Finding("EVIDENCE-002", "error", f"Stage {index} has invalid status: {status!r}.", relative_path(evidence_path, root)))
        checks = stage.get("checks")
        if not isinstance(checks, list):
            findings.append(Finding("EVIDENCE-002", "error", f"Stage {index} checks must be an array.", relative_path(evidence_path, root)))
            continue
        check_statuses: list[str] = []
        for check_index, check in enumerate(checks):
            if not isinstance(check, dict):
                findings.append(Finding("EVIDENCE-002", "error", f"Stage {index} check {check_index} is not an object.", relative_path(evidence_path, root)))
                continue
            missing_check = [key for key in required_check_fields if key not in check]
            if missing_check:
                findings.append(
                    Finding(
                        "EVIDENCE-002",
                        "error",
                        f"Stage {index} check {check_index} is missing: {', '.join(missing_check)}.",
                        relative_path(evidence_path, root),
                    )
                )
            check_status = check.get("status")
            check_statuses.append(str(check_status))
            if check_status not in EVIDENCE_STATUSES:
                findings.append(
                    Finding(
                        "EVIDENCE-002",
                        "error",
                        f"Stage {index} check {check_index} has invalid status: {check_status!r}.",
                        relative_path(evidence_path, root),
                    )
                )
        if status == "PASS" and any(check_status != "PASS" for check_status in check_statuses):
            findings.append(
                Finding(
                    "EVIDENCE-002",
                    "error",
                    f"Stage {index} is PASS but contains a non-PASS check.",
                    relative_path(evidence_path, root),
                )
            )


def run(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    load_rules(root, findings)
    check_frontmatter(root, findings)
    check_version_consistency(root, findings)
    check_markdown_links(root, findings)
    check_secret_patterns(root, findings)
    check_evidence_status(root, findings)
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Directory to inspect.")
    parser.add_argument("--changed", action="append", default=[], help="Optional changed path filter (repeatable).")
    parser.add_argument("--evidence", type=Path, help="Validate a stage evidence JSON file.")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--allow-warning", action="store_true", help="Accepted for CI compatibility; warnings remain visible.")
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        print(f"root does not exist: {root}", file=sys.stderr)
        return 2
    findings = run(root)
    if args.evidence:
        evidence_path = args.evidence.resolve()
        try:
            evidence_path.relative_to(root)
        except ValueError:
            print(f"evidence must be inside root: {evidence_path}", file=sys.stderr)
            return 2
        check_evidence_file(root, evidence_path, findings)
    if args.changed:
        changed = {Path(item).as_posix().lstrip("./") for item in args.changed}
        findings = [finding for finding in findings if not finding.path or finding.path in changed or finding.rule_id in {"SKILL-001", "RULE-001"}]
    if args.format == "json":
        print(json.dumps([finding.as_dict() for finding in findings], ensure_ascii=False, indent=2))
    else:
        if not findings:
            print("PASS: universal engineering baseline gates")
        for finding in findings:
            location = finding.path
            if finding.line is not None:
                location += f":{finding.line}"
            suffix = f" [{location}]" if location else ""
            print(f"{finding.severity.upper()} {finding.rule_id}{suffix}: {finding.message}")
    return 1 if any(item.severity in {"blocker", "error"} for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
