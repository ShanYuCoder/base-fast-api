"""Render docs/features/md from yaml bundles (Python-native)."""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any

from fast_spec.render_markdown import (
  bundle_markdown_output_path,
  bundle_slug,
  read_yaml,
  render_bundle_markdown,
  render_testcase_markdown,
  testcase_md_name,
)


def _list_testcase_files(feature_dir: Path, slug: str) -> list[Path]:
  patterns = [
    f"{slug}.test.yaml",
    f"{slug}.test.yml",
    f"{slug}.api-test.yaml",
    f"{slug}.api-test.yml",
  ]
  root_files = [feature_dir / name for name in patterns if (feature_dir / name).is_file()]
  testcase_dir = feature_dir / "testcases"
  testcase_files: list[Path] = []
  if testcase_dir.is_dir():
    for path in sorted(testcase_dir.glob("*.yaml")) + sorted(testcase_dir.glob("*.yml")):
      if slug == feature_dir.name or path.name.startswith(f"{slug}."):
        testcase_files.append(path)
  return sorted(set(root_files + testcase_files))


def _testcase_md_name(file_path: Path) -> str:
  return testcase_md_name(file_path)


def render_bundle_feature(
  bundle_file: Path,
  *,
  docs_dir: Path,
  yaml_root: Path,
  md_root: Path,
) -> int:
  feature_dir = bundle_file.parent
  slug = bundle_slug(bundle_file)
  bundle = read_yaml(bundle_file)
  spec_shape = {
    "id": bundle.get("id"),
    "title": bundle.get("title"),
    **(bundle.get("spec") or {}),
  }
  md_out = bundle_markdown_output_path(bundle_file, docs_dir, yaml_root, md_root)
  md_dir = md_out.parent
  md_testcases_dir = md_dir / "testcases"
  md_testcases_dir.mkdir(parents=True, exist_ok=True)

  testcase_files = _list_testcase_files(feature_dir, slug)
  testcases: list[dict[str, Any]] = []
  for file_path in testcase_files:
    data = read_yaml(file_path)
    testcases.append({"file": str(file_path), "data": data})
    (md_testcases_dir / _testcase_md_name(file_path)).write_text(
      render_testcase_markdown(data, spec_shape),
      encoding="utf-8",
    )

  md_out.parent.mkdir(parents=True, exist_ok=True)
  md_out.write_text(
    render_bundle_markdown(bundle, testcases, "testcases"),
    encoding="utf-8",
  )
  return len(testcase_files)


def render_all(
  project_root: Path | None = None,
  *,
  yaml_root: Path | None = None,
  md_root: Path | None = None,
  write_index: bool = True,
) -> tuple[int, int, int]:
  root = (project_root or Path.cwd()).resolve()
  docs_dir = root / "docs"
  features_dir = docs_dir / "features"
  y_root = yaml_root or features_dir / "yaml"
  m_root = md_root or features_dir / "md"

  started = time.time()
  bundles = sorted(y_root.glob("**/*.bundle.yaml")) + sorted(y_root.glob("**/*.bundle.yml"))
  testcase_count = 0
  failed = 0
  bundle_links: list[str] = []

  for bundle_file in bundles:
    try:
      testcase_count += render_bundle_feature(
        bundle_file,
        docs_dir=docs_dir,
        yaml_root=y_root,
        md_root=m_root,
      )
      md_path = bundle_markdown_output_path(bundle_file, docs_dir, y_root, m_root)
      rel = (Path("..") / md_path.relative_to(docs_dir)).as_posix()
      bundle = read_yaml(bundle_file)
      bundle_links.append(f"- [{bundle.get('title') or bundle_slug(bundle_file)}]({rel})")
    except Exception as exc:  # noqa: BLE001 — render boundary
      failed += 1
      print(f"docs:render: FAIL {bundle_file.relative_to(root)}: {exc}")

  if failed:
    raise RuntimeError(f"docs:render aborted — {failed} file(s) failed")

  if write_index:
    index_dir = docs_dir / "common-ui"
    index_dir.mkdir(parents=True, exist_ok=True)
    index_body = "# Tài liệu tính năng đã render\n\n" + ("\n".join(bundle_links) if bundle_links else "_None_") + "\n"
    (index_dir / "generated.md").write_text(index_body, encoding="utf-8")

  elapsed = time.time() - started
  print(
    f"docs:render: {len(bundles)} bundle(s) → {testcase_count} testcase(s) [{elapsed:.1f}s]"
  )
  return len(bundles), testcase_count, int(elapsed)
