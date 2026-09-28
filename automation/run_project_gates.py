#!/usr/bin/env python3
"""Plan or execute explicitly declared project gate commands without a shell."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path


VALID_CATEGORIES = {
    "format",
    "typecheck",
    "build",
    "unit",
    "integration",
    "system",
    "dependency",
    "security",
    "performance",
    "package",
}


def inside(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def load_profile(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("profile must be a JSON object")
    return value


def result(command: dict, status: str, message: str, duration: float = 0.0, exit_code: int | None = None) -> dict:
    return {
        "id": command.get("id", "unknown"),
        "category": command.get("category", "unknown"),
        "status": status,
        "message": message,
        "duration_seconds": round(duration, 3),
        "exit_code": exit_code,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--execute", action="store_true", help="Actually run commands; default is plan-only.")
    parser.add_argument("--report", type=Path)
    parser.add_argument("--category", action="append", choices=sorted(VALID_CATEGORIES))
    parser.add_argument("--max-output", type=int, default=4000)
    args = parser.parse_args()
    root = args.root.resolve()
    profile_path = args.profile.resolve()
    try:
        profile = load_profile(profile_path)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        print(f"invalid profile: {exc}", file=sys.stderr)
        return 2
    commands = profile.get("commands", [])
    if not isinstance(commands, list):
        print("profile.commands must be an array", file=sys.stderr)
        return 2

    results: list[dict] = []
    blocking_failure = False
    for command in commands:
        if not isinstance(command, dict):
            results.append(result({}, "FAIL", "command entry is not an object"))
            blocking_failure = True
            continue
        category = command.get("category")
        if args.category and category not in args.category:
            continue
        argv = command.get("command")
        cwd = (root / str(command.get("cwd", "."))).resolve()
        if category not in VALID_CATEGORIES:
            results.append(result(command, "FAIL", f"unsupported category: {category}"))
            blocking_failure = True
            continue
        if not isinstance(argv, list) or not argv or not all(isinstance(item, str) for item in argv):
            results.append(result(command, "FAIL", "command must be a non-empty string array"))
            blocking_failure = True
            continue
        if not inside(cwd, root):
            results.append(result(command, "BLOCKED", "command cwd escapes project root"))
            if command.get("required", False):
                blocking_failure = True
            continue
        if not args.execute:
            results.append(result(command, "NOT_RUN", "not executed; pass --execute to run"))
            continue
        executable = shutil.which(argv[0])
        if executable is None:
            status = "BLOCKED"
            message = f"executable not found: {argv[0]}"
            results.append(result(command, status, message))
            if command.get("required", False):
                blocking_failure = True
            continue
        timeout = int(command.get("timeout_seconds", 1800))
        allow_exit_codes = command.get("allow_exit_codes", [0])
        started = time.monotonic()
        try:
            completed = subprocess.run(
                argv,
                cwd=cwd,
                env=os.environ.copy(),
                shell=False,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
            duration = time.monotonic() - started
            output = (completed.stdout + completed.stderr).strip()
            output = output[-args.max_output:]
            allowed = completed.returncode in allow_exit_codes
            status = "PASS" if allowed else "FAIL"
            message = f"exit={completed.returncode}; output={output}"
            results.append(result(command, status, message, duration, completed.returncode))
            if not allowed and command.get("required", False):
                blocking_failure = True
        except subprocess.TimeoutExpired:
            duration = time.monotonic() - started
            results.append(result(command, "BLOCKED", f"timeout after {timeout}s", duration))
            if command.get("required", False):
                blocking_failure = True
        except OSError as exc:
            results.append(result(command, "BLOCKED", str(exc), time.monotonic() - started))
            if command.get("required", False):
                blocking_failure = True

    overall_status = "NOT_RUN" if not args.execute and results else "PASS"
    if blocking_failure:
        overall_status = "FAIL"
    report = {
        "root": str(root),
        "profile": str(profile_path),
        "executed": args.execute,
        "results": results,
        "status": overall_status,
    }
    if args.report:
        report_path = args.report.resolve()
        if not inside(report_path, root):
            print("report must be inside project root", file=sys.stderr)
            return 2
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if blocking_failure else 0


if __name__ == "__main__":
    raise SystemExit(main())
