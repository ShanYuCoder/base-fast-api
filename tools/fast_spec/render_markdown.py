"""Bundle + backend spec → markdown (parity portal docs:render)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from fast_spec.markdown_util import MD_NONE, format_inline, render_bullets, render_table, yaml_block

_SKIP_BODY_KEYS = {"id", "title", "summary", "acceptance"}
_BACKEND_FOCUS_KEYS = ("api", "requests", "responses", "codegen", "feature", "approval", "modules")


def bundle_to_spec_shape(bundle: dict[str, Any]) -> dict[str, Any]:
  return {
    "id": bundle.get("id"),
    "title": bundle.get("title"),
    "status": bundle.get("status"),
    "owner": bundle.get("owner"),
    "summary": bundle.get("summary") or (bundle.get("review") or {}).get("summary"),
    **(bundle.get("spec") or {}),
    "openQuestions": bundle.get("openQuestions") or [],
  }


def bundle_slug(bundle_path: Path) -> str:
  name = bundle_path.name
  for suffix in (".bundle.yaml", ".bundle.yml"):
    if name.endswith(suffix):
      return name[: -len(suffix)]
  return bundle_path.stem


def bundle_markdown_output_path(bundle_path: Path, docs_dir: Path, yaml_root: Path, md_root: Path) -> Path:
  rel = bundle_path.relative_to(yaml_root)
  name = rel.name
  for suffix in (".bundle.yaml", ".bundle.yml"):
    if name.endswith(suffix):
      return md_root / rel.with_name(name[: -len(suffix)] + ".md")
  return md_root / rel.with_suffix(".md")


def testcase_md_name(file_path: Path) -> str:
  name = file_path.name
  for suffix in (".test.yaml", ".test.yml", ".api-test.yaml", ".api-test.yml", ".yaml", ".yml"):
    if name.endswith(suffix):
      return name[: -len(suffix)] + ".md"
  return f"{file_path.stem}.md"


def render_testcase_line(testcases: list[dict[str, Any]], output_testcases_dir: str) -> str:
  if not testcases:
    return f"- **Testcase:** {MD_NONE}"
  links: list[str] = []
  for item in testcases:
    file_path = Path(item["file"])
    data = item["data"]
    md_name = testcase_md_name(file_path)
    label = data.get("title") or data.get("id")
    links.append(f"[{label}](./{output_testcases_dir}/{md_name})")
  return f"- **Testcase:** {' · '.join(links)}"


def render_header(spec: dict[str, Any], testcases: list[dict[str, Any]], output_testcases_dir: str) -> str:
  title = spec.get("title") or spec.get("id")
  lines = [
    f"# {title}",
    "",
    render_testcase_line(testcases, output_testcases_dir),
    render_api_line(spec),
  ]
  if spec.get("summary"):
    lines.extend(["", str(spec["summary"])])
  return "\n".join(lines)


def render_api_line(spec: dict[str, Any]) -> str:
  endpoints = (spec.get("api") or {}).get("endpoints") or []
  if not endpoints:
    return f"- **API:** {MD_NONE}"
  parts = [f"`{ep.get('method', 'GET')} {ep.get('path', '')}`" for ep in endpoints[:3]]
  suffix = f" (+{len(endpoints) - 3})" if len(endpoints) > 3 else ""
  return f"- **API:** {' · '.join(parts)}{suffix}"


def render_body(spec: dict[str, Any]) -> str:
  sections: list[str] = []
  for key in _BACKEND_FOCUS_KEYS:
    if spec.get(key) is not None:
      sections.append(_render_section(key, spec[key]))
  for key, value in spec.items():
    if key in _SKIP_BODY_KEYS or key in _BACKEND_FOCUS_KEYS or value is None:
      continue
    if key == "ui":
      sections.append(_render_ui_section(value))
    else:
      sections.append(_render_section(key, value))
  return "\n\n".join(s for s in sections if s)


def _render_section(key: str, value: Any) -> str:
  title = f"## {key}"
  if value is None or value == {} or value == []:
    return f"{title}\n\n{MD_NONE}"
  if isinstance(value, str):
    return f"{title}\n\n{value}"
  if key == "api" and isinstance(value, dict) and value.get("endpoints"):
    rows = [
      [
        ep.get("id", ""),
        ep.get("method", ""),
        ep.get("path", ""),
        ep.get("request", ""),
        ep.get("response", ""),
      ]
      for ep in value["endpoints"]
    ]
    return f"{title}\n\n{render_table(['ID', 'Method', 'Path', 'Request', 'Response'], rows)}"
  return f"{title}\n\n{yaml_block(value)}"


def _render_ui_section(ui: dict[str, Any]) -> str:
  return f"## ui\n\n{yaml_block(ui)}"


def render_design_section(design: dict[str, Any] | None) -> str:
  if not design:
    return ""
  parts = ["## Design intent", ""]
  if design.get("inherits"):
    parts.extend([f"**Inherits:** `{design['inherits']}`", ""])
  if (design.get("shell") or {}).get("tag"):
    parts.extend([f"**Shell:** {design['shell']['tag']}", ""])
  if design.get("patterns"):
    parts.extend(["**Patterns:**", "", "\n".join(f"- {p}" for p in design["patterns"]), ""])
  extras = {k: v for k, v in design.items() if k not in ("inherits", "shell", "patterns", "id")}
  if extras:
    parts.extend(["### Design (other)", "", yaml_block(extras), ""])
  return "\n".join(parts)


def render_legacy_section(legacy: dict[str, Any] | None) -> str:
  if not legacy:
    return ""
  parts = ["## Legacy evidence", ""]
  behaviors = legacy.get("behaviors") or []
  if behaviors:
    rows = [[b.get("id", ""), format_inline(b.get("fact", {})), b.get("confidence", "")] for b in behaviors]
    parts.extend(["### Behaviors", "", render_table(["ID", "Fact", "Confidence"], rows), ""])
  fields = legacy.get("fields") or []
  if fields:
    rows = [[f.get("name", ""), f.get("via", ""), f.get("confidence", "")] for f in fields]
    parts.extend(["### Fields", "", render_table(["Name", "Via", "Confidence"], rows), ""])
  return "\n".join(parts)


def render_spec_markdown(spec: dict[str, Any], testcases: list[dict[str, Any]], output_testcases_dir: str) -> str:
  header = render_header(spec, testcases, output_testcases_dir)
  body = render_body(spec)
  return f"{header}\n\n{body}\n" if body else f"{header}\n"


def render_bundle_markdown(bundle: dict[str, Any], testcases: list[dict[str, Any]], output_testcases_dir: str) -> str:
  parts = [render_spec_markdown(bundle_to_spec_shape(bundle), testcases, output_testcases_dir)]
  review = bundle.get("review") or {}
  layout_notes = review.get("layoutNotes")
  if layout_notes:
    if isinstance(layout_notes, list):
      parts.append("## Review — layout notes\n\n" + "\n".join(f"- {line}" for line in layout_notes))
    else:
      parts.append(f"## Review — layout notes\n\n- {layout_notes}")
  design_md = render_design_section(bundle.get("design"))
  if design_md:
    parts.append(design_md)
  legacy_md = render_legacy_section(bundle.get("legacy"))
  if legacy_md:
    parts.append(legacy_md)
  body = "\n\n".join(p for p in parts if p)
  return body if body.endswith("\n") else f"{body}\n"


def render_testcase_markdown(testcase: dict[str, Any], spec: dict[str, Any]) -> str:
  title = testcase.get("title") or testcase.get("id")
  return "\n".join(
    [
      f"# {title}",
      "",
      f"Feature: {spec.get('title') or testcase.get('feature', '')}",
      "",
      "## Type",
      "",
      testcase.get("type", "api-contract"),
      "",
      "## Endpoint",
      "",
      yaml_block(testcase.get("endpoint") or testcase.get("route")),
      "",
      "## Assertions",
      "",
      yaml_block(testcase.get("assertions")),
      "",
      "## Setup",
      "",
      yaml_block(testcase.get("setup")),
      "",
      "## Expected",
      "",
      render_bullets(testcase.get("expected") if isinstance(testcase.get("expected"), list) else None)
      or yaml_block(testcase.get("expected")),
      "",
    ]
  )


def read_yaml(path: Path) -> dict[str, Any]:
  return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
