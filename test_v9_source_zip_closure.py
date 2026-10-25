"""Constructed package-closure sabotage tests; never touches the real package.

Prepared without running pytest or the checker. Every source, ZIP, receipt and
deliberately bad dependency below is created only under pytest's tmp_path.
"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import warnings
import zipfile
import pytest


FIXED_MEMBERS = frozenset({
    "main.tex", "manuscript.tex", "supplement.tex", "extended-v9-technical.tex",
    "title-page.tex", "references.bib", "README.md", "AUTHOR-TODO.md", "cover-letter.md",
    "figures/v7-endpoint-peak-example.pdf",
    "figures/v7-murphy-fx_hourly.pdf",
    "figures/v7-murphy-nyfed_weekly.pdf",
    "figures/v8-wp3-qr33-loss.pdf",
    "figures/v8-wp3-qr4-loss.pdf",
    "figures/v9-unified-history.pdf",
    "generated/v8-backcast-complete-table.tex",
    "generated/v8-daily-results-table.tex",
    "generated/v8-mc-four-table.tex",
    "generated/v8-mc-full-table.tex",
    "generated/v8-three-window-table.tex",
    "generated/v9-evidence-tables.tex",
})
REGULAR_0644 = 0o100644


@pytest.fixture
def api():
    path = Path(__file__).parent / "notes/revision-v9/check_source_zip_closure.py"
    spec = importlib.util.spec_from_file_location("independent_source_zip_closure", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha(data):
    return hashlib.sha256(data).hexdigest()


def source_fixture(tmp_path):
    delivery = tmp_path / "submission-jof"
    delivery.mkdir()
    for name in sorted(FIXED_MEMBERS):
        path = delivery / name
        path.parent.mkdir(parents=True, exist_ok=True)
        if name.endswith(".pdf"):
            data = ("%PDF-1.4\n% Constructed placeholder for " + name + "\n").encode()
        elif name.endswith(".tex"):
            data = ("Constructed plain text for " + name + "\n").encode()
        else:
            data = ("Constructed package member " + name + "\n").encode()
        path.write_bytes(data)
        path.chmod(0o644)
    (delivery / "main.tex").write_text("\\input{manuscript}\n")
    (delivery / "manuscript.tex").write_text(
        "\\documentclass{article}\n\\usepackage{graphicx}\n\\begin{document}\n"
        + "".join("\\includegraphics{" + name + "}\n"
                  for name in sorted(FIXED_MEMBERS) if name.startswith("figures/"))
        + "\\end{document}\n")
    (delivery / "supplement.tex").write_text(
        "\\documentclass{article}\n\\begin{document}\n"
        + "".join("\\input{" + name + "}\n"
                  for name in sorted(FIXED_MEMBERS) if name.startswith("generated/"))
        + "\\end{document}\n")
    return delivery


def archive_and_receipt(delivery, tmp_path, *, omit=(), extras=(), replacements=None,
                        zip_modes=None, duplicate=None):
    """Receipt honestly describes archive bytes, including intentional bad ZIPs.

    Keeping receipt bindings current lets source/ZIP closure sabotage fail on
    its own merits rather than merely on an obsolete archive SHA.
    """
    replacements = replacements or {}
    zip_modes = zip_modes or {}
    entries = [(name, replacements.get(name, (delivery/name).read_bytes()))
               for name in sorted(FIXED_MEMBERS) if name not in omit]
    entries.extend(extras)
    if duplicate is not None:
        entries.append((duplicate, (delivery/duplicate).read_bytes()))
    zip_path = delivery / "overleaf-package.zip"
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="Duplicate name:", category=UserWarning)
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name, data in entries:
                info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = zip_modes.get(name, REGULAR_0644) << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, data)
    zip_bytes = zip_path.read_bytes()
    receipt_path = tmp_path / "sync-receipt.json"
    receipt = dict(status="PASS", package="submission-jof/overleaf-package.zip",
                   bytes=len(zip_bytes), sha256=sha(zip_bytes),
                   members=[dict(path=name, bytes=len(data), sha256=sha(data))
                            for name, data in entries])
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
    return zip_path, receipt_path, receipt


def write_receipt(path, receipt):
    path.write_text(json.dumps(receipt, indent=2) + "\n")


def assert_pass(result):
    assert result["status"] == "PASS"
    assert result["differences"] == []
    assert result["difference_count"] == 0


def assert_fail(result):
    assert result["status"] == "FAIL"
    assert isinstance(result["differences"], list) and result["differences"]
    assert result["difference_count"] > 0


def test_fixed_twenty_one_member_contract_and_valid_package(api, tmp_path):
    assert len(FIXED_MEMBERS) == 21
    assert api.EXPECTED_MEMBERS == FIXED_MEMBERS
    assert api.REQUIRED_MODE == REGULAR_0644
    delivery = source_fixture(tmp_path)
    archive, receipt, _ = archive_and_receipt(delivery, tmp_path)
    assert_pass(api.check_source_zip(delivery, archive, receipt))


def test_receipt_mode_can_be_present_when_correct(api, tmp_path):
    delivery = source_fixture(tmp_path)
    archive, receipt_path, receipt = archive_and_receipt(delivery, tmp_path)
    for member in receipt["members"]:
        member["mode"] = REGULAR_0644
    write_receipt(receipt_path, receipt)
    assert_pass(api.check_source_zip(delivery, archive, receipt_path))


@pytest.mark.parametrize("missing", ["README.md", "references.bib"])
def test_noncompiled_required_members_cannot_disappear_from_zip(api, tmp_path, missing):
    delivery = source_fixture(tmp_path)
    archive, receipt, _ = archive_and_receipt(delivery, tmp_path, omit=(missing,))
    assert_fail(api.check_source_zip(delivery, archive, receipt))


@pytest.mark.parametrize("missing", ["README.md", "references.bib"])
def test_noncompiled_local_sources_are_required_even_when_zip_is_complete(api, tmp_path, missing):
    delivery = source_fixture(tmp_path)
    archive, receipt, _ = archive_and_receipt(delivery, tmp_path)
    (delivery/missing).unlink()
    assert_fail(api.check_source_zip(delivery, archive, receipt))


@pytest.mark.parametrize("extra", [".env", "raw.csv"])
def test_unlisted_sensitive_or_raw_members_are_rejected(api, tmp_path, extra):
    delivery = source_fixture(tmp_path)
    archive, receipt, _ = archive_and_receipt(delivery, tmp_path,
                                              extras=[(extra, b"constructed harmless fixture\n")])
    assert_fail(api.check_source_zip(delivery, archive, receipt))


def test_swapped_payloads_are_rejected_even_with_honest_current_zip_receipt(api, tmp_path):
    delivery = source_fixture(tmp_path)
    replacements = {"README.md": (delivery/"references.bib").read_bytes(),
                    "references.bib": (delivery/"README.md").read_bytes()}
    archive, receipt, _ = archive_and_receipt(delivery, tmp_path, replacements=replacements)
    assert_fail(api.check_source_zip(delivery, archive, receipt))


def test_zip_payload_byte_mutation_cannot_hide_behind_current_receipt(api, tmp_path):
    delivery = source_fixture(tmp_path)
    old = (delivery/"main.tex").read_bytes()
    archive, receipt, _ = archive_and_receipt(delivery, tmp_path,
                                              replacements={"main.tex": old+b"% changed archive byte\n"})
    assert_fail(api.check_source_zip(delivery, archive, receipt))


def test_local_source_byte_mutation_after_zip_and_receipt_is_detected(api, tmp_path):
    delivery = source_fixture(tmp_path)
    archive, receipt, _ = archive_and_receipt(delivery, tmp_path)
    source = delivery/"AUTHOR-TODO.md"
    source.write_bytes(source.read_bytes()+b"changed source byte\n")
    assert_fail(api.check_source_zip(delivery, archive, receipt))


def test_duplicate_archive_member_is_not_collapsed_into_dictionary_success(api, tmp_path):
    delivery = source_fixture(tmp_path)
    archive, receipt, _ = archive_and_receipt(delivery, tmp_path, duplicate="main.tex")
    assert_fail(api.check_source_zip(delivery, archive, receipt))


@pytest.mark.parametrize("name", ["../outside.tex", "/absolute.tex", "figures\\bad.pdf",
                                 "generated/../outside.tex", "./main.tex"])
def test_unsafe_or_noncanonical_zip_member_names_are_rejected(api, tmp_path, name):
    delivery = source_fixture(tmp_path)
    archive, receipt, _ = archive_and_receipt(delivery, tmp_path,
                                              extras=[(name, b"constructed archive entry\n")])
    assert_fail(api.check_source_zip(delivery, archive, receipt))


@pytest.mark.parametrize("mode", [0o100600, 0o100755, 0o120777])
def test_zip_member_modes_must_be_regular_0644(api, tmp_path, mode):
    delivery = source_fixture(tmp_path)
    archive, receipt, _ = archive_and_receipt(delivery, tmp_path,
                                              zip_modes={"README.md": mode})
    assert_fail(api.check_source_zip(delivery, archive, receipt))


@pytest.mark.parametrize("mode", [0o600, 0o755])
def test_local_source_modes_must_be_0644(api, tmp_path, mode):
    delivery = source_fixture(tmp_path)
    archive, receipt, _ = archive_and_receipt(delivery, tmp_path)
    (delivery/"README.md").chmod(mode)
    assert_fail(api.check_source_zip(delivery, archive, receipt))


@pytest.mark.parametrize("sabotage", ["archive_sha", "archive_bytes", "package", "status",
                                    "member_missing", "member_duplicate", "member_sha",
                                    "member_bytes", "member_mode"])
def test_sync_receipt_global_and_member_bindings_are_checked(api, tmp_path, sabotage):
    delivery = source_fixture(tmp_path)
    archive, receipt_path, receipt = archive_and_receipt(delivery, tmp_path)
    if sabotage == "archive_sha":
        receipt["sha256"] = "0"*64
    elif sabotage == "archive_bytes":
        receipt["bytes"] += 1
    elif sabotage == "package":
        receipt["package"] = "submission-jof/other.zip"
    elif sabotage == "status":
        receipt["status"] = "FAIL"
    elif sabotage == "member_missing":
        receipt["members"].pop()
    elif sabotage == "member_duplicate":
        receipt["members"].append(copy.deepcopy(receipt["members"][0]))
    elif sabotage == "member_sha":
        receipt["members"][0]["sha256"] = "0"*64
    elif sabotage == "member_bytes":
        receipt["members"][0]["bytes"] += 1
    else:
        receipt["members"][0]["mode"] = 0o100600
    write_receipt(receipt_path, receipt)
    assert_fail(api.check_source_zip(delivery, archive, receipt_path))


@pytest.mark.parametrize("tex_member,dependency", [
    ("main.tex", "../outside"),
    ("main.tex", "generated/unlisted"),
    ("extended-v9-technical.tex", "uncompiled-private-note"),
])
def test_existing_tex_dependency_outside_explicit_whitelist_is_rejected(api, tmp_path,
                                                                      tex_member, dependency):
    delivery = source_fixture(tmp_path)
    dependency_path = (delivery/(dependency+".tex"))
    dependency_path.parent.mkdir(parents=True, exist_ok=True)
    dependency_path.write_text("Constructed dependency outside the source closure.\n")
    source = delivery/tex_member
    source.write_text(source.read_text()+"\\input{"+dependency+"}\n")
    archive, receipt, _ = archive_and_receipt(delivery, tmp_path)
    assert_fail(api.check_source_zip(delivery, archive, receipt))


def test_unlisted_figure_dependency_is_rejected_with_consistent_source_and_zip(api, tmp_path):
    delivery = source_fixture(tmp_path)
    (delivery/"figures/unlisted.pdf").write_bytes(b"%PDF-1.4\n% harmless unlisted figure\n")
    source = delivery/"manuscript.tex"
    source.write_text(source.read_text()+"\\includegraphics{figures/unlisted.pdf}\n")
    archive, receipt, _ = archive_and_receipt(delivery, tmp_path)
    assert_fail(api.check_source_zip(delivery, archive, receipt))


def test_source_symlink_is_rejected_even_when_target_bytes_match_archive(api, tmp_path):
    delivery = source_fixture(tmp_path)
    archive, receipt, _ = archive_and_receipt(delivery, tmp_path)
    source = delivery/"README.md"
    target = tmp_path/"outside-identical-readme.md"
    target.write_bytes(source.read_bytes())
    target.chmod(0o644)
    source.unlink()
    source.symlink_to(target)
    assert_fail(api.check_source_zip(delivery, archive, receipt))
