#!/usr/bin/env python3
"""Validate the repository structure without third-party Python packages."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote, urlsplit


SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
FRONTMATTER_KEY_RE = re.compile(r"^(?P<indent>\s*)(?P<key>[A-Za-z_][A-Za-z0-9_-]*):(?:\s*(?P<value>.*))?$")
MARKDOWN_LINK_RE = re.compile(
    r"(?<!!)\[[^\]\n]*\]\(\s*(?P<inline>[^)\n]+?)\s*\)"
    r"|(?<!!)\[[^\]\n]+\]\s*:\s*(?P<definition><[^>\n]+>|\S+)"
)

PLUGIN_MANIFESTS = (
    Path(".claude-plugin/plugin.json"),
    Path(".cursor-plugin/plugin.json"),
    Path("gemini-extension.json"),
)
FRONTMATTER_KEYS = {
    "name",
    "description",
    "license",
    "compatibility",
    "user-invocable",
    "allowed-tools",
    "metadata",
}


class Validator:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.skills: dict[str, Path] = {}

    def error(self, path: Path | str, message: str) -> None:
        self.errors.append(f"{self.display(path)}: {message}")

    def warning(self, path: Path | str, message: str) -> None:
        self.warnings.append(f"{self.display(path)}: {message}")

    def display(self, path: Path | str) -> str:
        candidate = Path(path)
        if not candidate.is_absolute():
            candidate = self.root / candidate
        try:
            return str(candidate.resolve().relative_to(self.root.resolve()))
        except ValueError:
            return str(candidate)

    def run(self) -> int:
        self.validate_skills()
        self.validate_plugin_versions()
        self.validate_readme()
        self.print_results()
        return 1 if self.errors else 0

    def validate_skills(self) -> None:
        skills_dir = self.root / "skills"
        if not skills_dir.is_dir():
            self.error("skills", "directory is missing")
            return

        skill_dirs = sorted(
            path for path in skills_dir.iterdir() if path.is_dir() and not path.name.startswith(".")
        )
        if not skill_dirs:
            self.error("skills", "no skill directories found")
            return

        for skill_dir in skill_dirs:
            name = skill_dir.name
            self.skills[name] = skill_dir
            skill_file = skill_dir / "SKILL.md"
            if not skill_file.is_file():
                self.error(skill_file, "missing SKILL.md")
                continue

            frontmatter, body = self.read_frontmatter(skill_file)
            if frontmatter is None:
                continue

            top_level_keys = {key.split(".", 1)[0] for key in frontmatter}
            unexpected_keys = top_level_keys - FRONTMATTER_KEYS
            if unexpected_keys:
                self.error(
                    skill_file,
                    "unsupported frontmatter key(s): "
                    + ", ".join(sorted(unexpected_keys)),
                )

            declared_name = frontmatter.get("name")
            if declared_name != name:
                self.error(
                    skill_file,
                    f"frontmatter name must be {name!r}, got {declared_name!r}",
                )

            for key in ("description", "license", "compatibility", "allowed-tools"):
                if not frontmatter.get(key):
                    self.error(skill_file, f"frontmatter {key!r} must be non-empty")
            if frontmatter.get("user-invocable") not in {"true", "false"}:
                self.error(
                    skill_file,
                    "frontmatter user-invocable must be true or false",
                )
            if not frontmatter.get("metadata.author"):
                self.error(skill_file, "frontmatter metadata.author must be non-empty")
            if not frontmatter.get("metadata.openclaw.homepage"):
                self.error(
                    skill_file,
                    "frontmatter metadata.openclaw.homepage must be non-empty",
                )

            version = frontmatter.get("metadata.version") or frontmatter.get("version")
            if not version:
                self.error(
                    skill_file,
                    "frontmatter must define metadata.version or version",
                )
            elif not SEMVER_RE.fullmatch(version):
                self.error(skill_file, f"version {version!r} is not valid semantic versioning")

            if not frontmatter.get("description"):
                self.error(skill_file, "frontmatter description must be non-empty")

            for markdown_path in sorted(skill_dir.rglob("*.md")):
                try:
                    markdown_text = markdown_path.read_text(encoding="utf-8")
                except (OSError, UnicodeDecodeError) as exc:
                    self.error(markdown_path, f"must be readable UTF-8 text ({exc})")
                    continue
                self.validate_local_links(markdown_path, markdown_text)
            self.validate_evals(skill_dir, name, version if isinstance(version, str) else None)
            self.validate_ui_metadata(skill_dir, name)

    def read_frontmatter(self, path: Path) -> tuple[dict[str, str], str] | tuple[None, str]:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            self.error(path, f"must be UTF-8 text ({exc})")
            return None, ""

        lines = text.splitlines()
        if not lines or lines[0].strip() != "---":
            self.error(path, "must start with YAML frontmatter delimiter ---")
            return None, text

        closing_index = next(
            (index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"),
            None,
        )
        if closing_index is None:
            self.error(path, "frontmatter is missing its closing --- delimiter")
            return None, text

        values: dict[str, str] = {}
        sections: list[tuple[int, str]] = []
        for line_number, line in enumerate(lines[1:closing_index], start=2):
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            if line.lstrip().startswith("-"):
                if not sections:
                    self.error(path, f"invalid frontmatter at line {line_number}: {line!r}")
                continue
            match = FRONTMATTER_KEY_RE.match(line)
            if not match:
                self.error(path, f"invalid frontmatter at line {line_number}: {line!r}")
                continue

            indent = len(match.group("indent").replace("\t", "    "))
            key = match.group("key")
            raw_value = (match.group("value") or "").strip()
            while sections and indent <= sections[-1][0]:
                sections.pop()

            if not raw_value:
                sections.append((indent, key))
                continue

            full_key = ".".join(section_key for _, section_key in sections) + (
                "." if sections else ""
            ) + key
            if full_key in values:
                self.error(path, f"duplicate frontmatter key {full_key!r}")
                continue
            values[full_key] = self.unquote_yaml_scalar(raw_value)

        body = "\n".join(lines[closing_index + 1 :])
        return values, body

    @staticmethod
    def unquote_yaml_scalar(value: str) -> str:
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            if value[0] == '"':
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value[1:-1]
            return value[1:-1].replace("''", "'")
        return value

    def validate_local_links(
        self,
        source: Path,
        text: str,
        *,
        allow_planned_skill_links: bool = False,
    ) -> None:
        for target in markdown_targets(text):
            local_target = local_path_from_target(target)
            if local_target is None:
                continue

            decoded_target = unquote(local_target)
            candidate = (source.parent / decoded_target).resolve()
            try:
                candidate.relative_to(self.root.resolve())
            except ValueError:
                self.error(source, f"local link escapes repository root: {target!r}")
                continue
            if not candidate.exists():
                if allow_planned_skill_links and is_planned_skill_link(decoded_target):
                    self.warning(source, f"planned skill link is not available yet: {target!r}")
                else:
                    self.error(source, f"local link target does not exist: {target!r}")

    def validate_evals(
        self,
        skill_dir: Path,
        skill_name: str,
        skill_version: str | None,
    ) -> None:
        evals_path = skill_dir / "evals" / "evals.json"
        if not evals_path.is_file():
            self.error(evals_path, "missing evals/evals.json")
            return

        try:
            data = json.loads(evals_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            self.error(evals_path, f"must be valid UTF-8 JSON ({exc})")
            return

        if not isinstance(data, dict):
            self.error(evals_path, "root must be an object")
            return

        expected_keys = {"skill", "version", "cases"}
        unexpected_keys = set(data) - expected_keys
        if unexpected_keys:
            self.error(
                evals_path,
                "unsupported root key(s): " + ", ".join(sorted(unexpected_keys)),
            )

        declared_skill = data.get("skill")
        if declared_skill != skill_name:
            self.error(
                evals_path,
                f"skill must be {skill_name!r}, got {declared_skill!r}",
            )
        if skill_version is not None and data.get("version") != skill_version:
            self.error(
                evals_path,
                f"version must match SKILL.md metadata.version {skill_version!r}",
            )
        if not isinstance(data.get("version"), str) or not SEMVER_RE.fullmatch(
            data["version"]
        ):
            self.error(evals_path, "version must be a valid semantic version string")

        evaluations = data.get("cases")
        if not isinstance(evaluations, list):
            self.error(evals_path, "cases must be an array")
            return
        if not evaluations:
            self.error(evals_path, "cases must contain at least one evaluation")
            return

        case_ids: set[str] = set()
        for index, evaluation in enumerate(evaluations, start=1):
            location = f"{self.display(evals_path)} evaluation {index}"
            if not isinstance(evaluation, dict):
                self.error(location, "must be an object")
                continue
            for field in ("id", "name", "prompt", "description"):
                value = evaluation.get(field)
                if not isinstance(value, str) or not value.strip():
                    self.error(location, f"{field} must be a non-empty string")
            case_id = evaluation.get("id")
            if isinstance(case_id, str):
                if case_id in case_ids:
                    self.error(location, f"duplicate case id {case_id!r}")
                case_ids.add(case_id)

            traps = evaluation.get("traps")
            if not isinstance(traps, list) or not traps:
                self.error(location, "traps must be a non-empty array")
            elif any(not isinstance(trap, str) or not trap.strip() for trap in traps):
                self.error(location, "traps must contain non-empty strings")

            assertions = evaluation.get("assertions")
            if not isinstance(assertions, list) or not assertions:
                self.error(location, "assertions must be a non-empty array")
                continue
            assertion_ids: set[str] = set()
            for assertion_index, assertion in enumerate(assertions, start=1):
                assertion_location = f"{location} assertion {assertion_index}"
                if not isinstance(assertion, dict):
                    self.error(assertion_location, "must be an object")
                    continue
                assertion_id = assertion.get("id")
                if not isinstance(assertion_id, str) or not assertion_id.strip():
                    self.error(assertion_location, "id must be a non-empty string")
                elif assertion_id in assertion_ids:
                    self.error(assertion_location, f"duplicate assertion id {assertion_id!r}")
                else:
                    assertion_ids.add(assertion_id)
                text = assertion.get("text")
                if not isinstance(text, str) or not text.strip():
                    self.error(assertion_location, "text must be a non-empty string")

    def validate_ui_metadata(self, skill_dir: Path, skill_name: str) -> None:
        path = skill_dir / "agents" / "openai.yaml"
        if not path.exists():
            return
        if not path.is_file():
            self.error(path, "must be a regular file")
            return

        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            self.error(path, f"must be readable UTF-8 text ({exc})")
            return

        fields = {
            "display_name": re.search(
                r'^\s+display_name:\s*"([^"\n]+)"\s*$', text, re.MULTILINE
            ),
            "short_description": re.search(
                r'^\s+short_description:\s*"([^"\n]+)"\s*$', text, re.MULTILINE
            ),
            "default_prompt": re.search(
                r'^\s+default_prompt:\s*"([^"\n]+)"\s*$', text, re.MULTILINE
            ),
        }
        for field, match in fields.items():
            if match is None or not match.group(1).strip():
                self.error(path, f"interface.{field} must be a quoted non-empty string")

        short_description = fields["short_description"]
        if short_description is not None:
            length = len(short_description.group(1))
            if not 25 <= length <= 64:
                self.error(
                    path,
                    f"interface.short_description must contain 25–64 characters (got {length})",
                )

        default_prompt = fields["default_prompt"]
        if default_prompt is not None and f"${skill_name}" not in default_prompt.group(1):
            self.error(
                path,
                f"interface.default_prompt must mention ${skill_name}",
            )

        if not re.search(
            r"^\s+allow_implicit_invocation:\s*(true|false)\s*$",
            text,
            re.MULTILINE,
        ):
            self.error(
                path,
                "policy.allow_implicit_invocation must be true or false",
            )

    def validate_plugin_versions(self) -> None:
        versions: dict[Path, str] = {}
        for relative_path in PLUGIN_MANIFESTS:
            path = self.root / relative_path
            if not path.is_file():
                self.error(path, "missing plugin manifest")
                continue
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
                self.error(path, f"must be valid UTF-8 JSON ({exc})")
                continue
            if not isinstance(data, dict):
                self.error(path, "root must be a JSON object")
                continue
            version = data.get("version")
            if not isinstance(version, str) or not SEMVER_RE.fullmatch(version):
                self.error(path, "version must be a valid semantic version string")
                continue
            versions[relative_path] = version

        if versions and len(set(versions.values())) != 1:
            details = ", ".join(f"{path}={version}" for path, version in versions.items())
            self.error("plugin manifests", f"versions must match ({details})")

    def validate_readme(self) -> None:
        readme = self.root / "README.md"
        if not readme.is_file():
            self.error(readme, "missing README.md")
            return

        try:
            text = readme.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            self.error(readme, f"must be readable UTF-8 text ({exc})")
            return

        targets = list(markdown_targets(text))
        self.validate_local_links(readme, text)
        linked_skill_paths: set[Path] = set()
        for target in targets:
            path = local_path_from_target(target)
            if path is None:
                continue
            candidate = (readme.parent / unquote(path)).resolve()
            if candidate.name == "SKILL.md":
                linked_skill_paths.add(candidate)
            elif candidate.parent.name == "skills" and candidate.name in self.skills:
                linked_skill_paths.add(candidate / "SKILL.md")
        for skill_name, skill_dir in self.skills.items():
            expected = (skill_dir / "SKILL.md").resolve()
            if expected not in linked_skill_paths:
                self.error(readme, f"missing link to skills/{skill_name}/SKILL.md")

    def print_results(self) -> None:
        for warning in self.warnings:
            print(f"warning: {warning}", file=sys.stderr)
        for error in self.errors:
            print(f"error: {error}", file=sys.stderr)
        if self.errors:
            print(f"Validation failed with {len(self.errors)} error(s).", file=sys.stderr)
        else:
            print("Repository validation passed.")


def markdown_targets(text: str) -> Iterable[str]:
    for match in MARKDOWN_LINK_RE.finditer(text):
        target = match.group("inline") or match.group("definition")
        if target is None:
            continue
        target = target.strip()
        if target.startswith("<") and ">" in target:
            target = target[1 : target.index(">")]
        else:
            target = target.split(maxsplit=1)[0]
        yield target


def local_path_from_target(target: str) -> str | None:
    stripped = target.strip()
    if not stripped or stripped.startswith("#"):
        return None
    parsed = urlsplit(stripped)
    if parsed.scheme or parsed.netloc or stripped.startswith("//"):
        return None
    return parsed.path or None


def is_planned_skill_link(path: str) -> bool:
    normalized = path.rstrip("/")
    parts = Path(normalized).parts
    return path.endswith("/") and len(parts) == 2 and parts[0] == "skills"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root (default: parent of scripts/)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        print(f"error: repository root does not exist: {root}", file=sys.stderr)
        return 2
    return Validator(root).run()


if __name__ == "__main__":
    sys.exit(main())
