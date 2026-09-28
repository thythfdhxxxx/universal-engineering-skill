#!/usr/bin/env python3
"""Detect a conservative, reviewable project profile without editing the project."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


RULE_NAMES = (
    "AGENTS.md",
    "CLAUDE.md",
    "CONTRIBUTING.md",
    "DEVELOPMENT.md",
    "README.md",
)
IGNORED_DIRS = {".git", "node_modules", "build", "out", "dist", "target", "__pycache__"}


def exists(root: Path, name: str) -> bool:
    return (root / name).exists()


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return {}


def add_language(items: list[dict], name: str, source: str) -> None:
    if not any(item.get("name") == name for item in items):
        items.append({"name": name, "source": source})


def detect(root: Path) -> dict:
    languages: list[dict] = []
    frameworks: list[dict] = []
    package_managers: list[str] = []
    platforms: list[str] = []
    conflicts: list[str] = []
    assumptions: list[str] = []

    if exists(root, "CMakeLists.txt") or exists(root, "CMakePresets.json"):
        add_language(languages, "C++/C", "CMakeLists.txt or CMakePresets.json")
        package_managers.append("cmake")
    if exists(root, "Cargo.toml"):
        add_language(languages, "Rust", "Cargo.toml")
        package_managers.append("cargo")
    if exists(root, "go.mod"):
        add_language(languages, "Go", "go.mod")
        package_managers.append("go")
    if exists(root, "pyproject.toml") or exists(root, "setup.py"):
        add_language(languages, "Python", "pyproject.toml or setup.py")
        package_managers.append("python")
    if exists(root, "package.json"):
        package = load_json(root / "package.json")
        add_language(languages, "JavaScript/TypeScript", "package.json")
        package_managers.append(
            "pnpm" if exists(root, "pnpm-lock.yaml")
            else "yarn" if exists(root, "yarn.lock")
            else "npm"
        )
        dependencies = {}
        dependencies.update(package.get("dependencies", {}))
        dependencies.update(package.get("devDependencies", {}))
        for name in ("react", "vue", "svelte", "next", "angular", "electron", "vite"):
            if name in dependencies or any(key.startswith(f"{name}-") for key in dependencies):
                frameworks.append({"name": name, "source": "package.json"})
    if exists(root, "build.gradle") or exists(root, "build.gradle.kts") or exists(root, "gradlew"):
        add_language(languages, "Java/Kotlin", "Gradle build files")
        package_managers.append("gradle-wrapper")
    if list(root.glob("*.sln")) or list(root.glob("*.csproj")):
        add_language(languages, "C#", "solution or project file")
        package_managers.append("dotnet")
    if list(root.glob("*.uproject")) or exists(root, "Engine/Build/BatchFiles/Build.bat"):
        add_language(languages, "C++/Blueprint", "Unreal project markers")
        frameworks.append({"name": "Unreal Engine", "source": "uproject or UBT marker"})
    if exists(root, "Dockerfile") or exists(root, "docker-compose.yml") or exists(root, "compose.yml"):
        package_managers.append("docker")

    if not languages:
        assumptions.append("No supported language marker was detected; inspect the project manually.")
    if len(package_managers) > 3:
        conflicts.append("Several build/package ecosystems were detected; confirm the owning build system.")

    for marker, platform in (
        ("CMakePresets.json", "CMake targets"),
        ("build.gradle", "JVM"),
        ("package.json", "Node/browser"),
        ("*.uproject", "Unreal"),
    ):
        if marker.startswith("*"):
            if list(root.glob(marker)):
                platforms.append(platform)
        elif exists(root, marker):
            platforms.append(platform)
    if not platforms:
        platforms.append("unknown")

    rules = [name for name in RULE_NAMES if exists(root, name)]
    if not rules:
        assumptions.append("No conventional root rule file was detected; search subdirectories and tool-specific rules.")

    commands: list[dict] = []
    package = load_json(root / "package.json") if exists(root, "package.json") else {}
    scripts = package.get("scripts", {}) if isinstance(package, dict) else {}
    if isinstance(scripts, dict):
        for script_name in ("lint", "typecheck", "test", "build"):
            if script_name in scripts:
                manager = "pnpm" if exists(root, "pnpm-lock.yaml") else "yarn" if exists(root, "yarn.lock") else "npm"
                commands.append(
                    {
                        "id": f"node-{script_name}",
                        "category": "unit" if script_name == "test" else script_name,
                        "command": [manager, "run", script_name],
                        "cwd": ".",
                        "required": script_name in {"build", "test"},
                        "timeout_seconds": 1800,
                        "allow_exit_codes": [0],
                        "source": "package.json scripts; review before execution",
                    }
                )
    if exists(root, "Cargo.toml"):
        commands.extend(
            [
                {
                    "id": "cargo-format",
                    "category": "format",
                    "command": ["cargo", "fmt", "--", "--check"],
                    "cwd": ".",
                    "required": False,
                    "timeout_seconds": 300,
                    "allow_exit_codes": [0],
                    "source": "Cargo.toml marker; review before execution",
                },
                {
                    "id": "cargo-test",
                    "category": "unit",
                    "command": ["cargo", "test", "--workspace"],
                    "cwd": ".",
                    "required": True,
                    "timeout_seconds": 1800,
                    "allow_exit_codes": [0],
                    "source": "Cargo.toml marker; review before execution",
                },
            ]
        )
    if exists(root, "go.mod"):
        commands.append(
            {
                "id": "go-test",
                "category": "unit",
                "command": ["go", "test", "./..."],
                "cwd": ".",
                "required": True,
                "timeout_seconds": 1800,
                "allow_exit_codes": [0],
                "source": "go.mod marker; review before execution",
            }
        )

    return {
        "project": root.name,
        "root": ".",
        "detected": {
            "languages": languages,
            "frameworks": frameworks,
            "package_managers": sorted(set(package_managers)),
            "platforms": sorted(set(platforms)),
        },
        "declared": {},
        "rules": rules,
        "commands": commands,
        "gates": {
            "required_categories": sorted(
                {command["category"] for command in commands if command.get("required")}
            )
        },
        "conflicts": conflicts,
        "assumptions": assumptions,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        print(f"root does not exist: {root}")
        return 2
    profile = detect(root)
    output = json.dumps(profile, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        target = args.output.resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
