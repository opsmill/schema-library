from pathlib import Path

from tasks.schemas import Finding, format_annotation, validate_schema_files

VALID = """---
version: "1.0"
nodes:
  - name: Widget
    namespace: Test
    attributes:
      - name: name
        kind: Text
"""


def _write(root: Path, relative: str, content: str) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def _paths(findings: list[Finding]) -> set[str]:
    return {finding.path.as_posix() for finding in findings}


def test_valid_schema_passes(tmp_path: Path) -> None:
    _write(tmp_path, "base/widget.yml", VALID)
    _write(tmp_path, "extensions/one/widget.yaml", VALID)

    assert not validate_schema_files(tmp_path)


def test_unknown_key_fails_and_names_the_file(tmp_path: Path) -> None:
    _write(tmp_path, "base/good.yml", VALID)
    _write(
        tmp_path,
        "extensions/one/bad.yml",
        VALID.replace("namespace: Test", "namespace: Test\n    bogus_key: 1"),
    )

    findings = validate_schema_files(tmp_path)

    assert findings
    assert _paths(findings) == {"extensions/one/bad.yml"}
    assert any("bogus_key" in finding.message for finding in findings)


def test_attribute_kind_outside_allowed_values_fails(tmp_path: Path) -> None:
    _write(tmp_path, "base/bad.yml", VALID.replace("kind: Text", "kind: NotAKind"))

    findings = validate_schema_files(tmp_path)

    assert findings
    assert _paths(findings) == {"base/bad.yml"}


def test_read_only_field_warning_fails(tmp_path: Path) -> None:
    _write(
        tmp_path,
        "base/readonly.yml",
        VALID.replace("namespace: Test", "namespace: Test\n    hash: abc"),
    )

    findings = validate_schema_files(tmp_path)

    assert findings
    assert _paths(findings) == {"base/readonly.yml"}
    assert any(finding.message.startswith("Warning:") for finding in findings)


def test_every_invalid_file_is_reported(tmp_path: Path) -> None:
    _write(tmp_path, "base/bad.yml", VALID.replace("kind: Text", "kind: NotAKind"))
    _write(
        tmp_path,
        "extensions/one/bad.yml",
        VALID.replace("namespace: Test", "namespace: Test\n    bogus_key: 1"),
    )
    _write(tmp_path, "extensions/two/bad.yaml", "nodes: [unclosed")

    assert _paths(validate_schema_files(tmp_path)) == {
        "base/bad.yml",
        "extensions/one/bad.yml",
        "extensions/two/bad.yaml",
    }


def test_experimental_is_not_read(tmp_path: Path) -> None:
    _write(tmp_path, "base/good.yml", VALID)
    _write(tmp_path, "experimental/bad/bad.yml", "nodes: [unclosed")

    assert not validate_schema_files(tmp_path)


def test_annotation_names_the_file_and_escapes_newlines() -> None:
    annotation = format_annotation(Finding(Path("base/a.yml"), "first\nsecond"))

    assert annotation == "::error file=base/a.yml::first%0Asecond"
