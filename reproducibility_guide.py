"""Rebuild generated guide content without overwriting manual sections.

The first migration recognizes only the documented legacy guide title. Its
title/preamble and two named generated sections belong to the generator; every
other level-two section is retained verbatim after the generated region.
Subsequent rebuilds replace only that explicitly marked region.
"""

import re


LEGACY_TITLE = "# Reproducibility, pre-specification and consulted editions"
GENERATED_BEGIN = "<!-- BEGIN REPRODUCIBILITY_V3 GENERATED -->"
GENERATED_END = "<!-- END REPRODUCIBILITY_V3 GENERATED -->"

_OWNED_HEADINGS = frozenset(
    {
        "Original reference-edition notes retained verbatim",
        "Additional appendix execution records",
    }
)
_HEADING = re.compile(r"^[ ]{0,3}##[ \t]+(.+?)[ \t]*$")
_FENCE = re.compile(r"^[ ]{0,3}(`{3,}|~{3,})")


def read_guide_text(path) -> str:
    """Read an existing guide without universal-newline normalization."""
    if not path.exists():
        return ""
    with path.open("r", encoding="utf-8", newline="") as stream:
        return stream.read()


def _manual_legacy_sections(previous: str) -> str:
    """Retain unknown H2 sections, ignoring heading-like fenced examples."""
    preserved = []
    keep = False
    fence_char = None
    fence_length = 0
    for line in previous.splitlines(keepends=True):
        content = line.rstrip("\r\n")
        fence = _FENCE.match(content)
        if fence_char is not None:
            if (
                fence is not None
                and fence.group(1)[0] == fence_char
                and len(fence.group(1)) >= fence_length
                and not content[fence.end() :].strip()
            ):
                fence_char = None
            if keep:
                preserved.append(line)
            continue
        if fence is not None:
            fence_char = fence.group(1)[0]
            fence_length = len(fence.group(1))
        else:
            heading = _HEADING.fullmatch(content)
            if heading is not None:
                keep = heading.group(1) not in _OWNED_HEADINGS
        if keep:
            preserved.append(line)
    return "".join(preserved)


def rebuild_guide(previous: str, generated: str) -> str:
    """Return a guide with only its generated region rebuilt.

    Unknown legacy titles and missing, duplicated, inline, or reversed reserved
    markers raise ``ValueError`` rather than guessing which text may be replaced.
    This function performs no file operations.
    """
    if not isinstance(previous, str) or not isinstance(generated, str):
        raise TypeError("previous and generated must be strings")
    if GENERATED_BEGIN in generated or GENERATED_END in generated:
        raise ValueError("generated content must not contain reserved markers")
    body_end = "" if not generated or generated.endswith("\n") else "\n"
    region = GENERATED_BEGIN + "\n" + generated + body_end + GENERATED_END
    counts = (previous.count(GENERATED_BEGIN), previous.count(GENERATED_END))
    if counts != (0, 0):
        if counts != (1, 1):
            raise ValueError("both generated-region markers must occur exactly once")
        for marker in (GENERATED_BEGIN, GENERATED_END):
            if re.search(r"(?m)^" + re.escape(marker) + r"\r?$", previous) is None:
                raise ValueError("generated-region markers must occupy standalone lines")
        start = previous.index(GENERATED_BEGIN)
        finish = previous.index(GENERATED_END)
        if finish < start:
            raise ValueError("generated-region markers are reversed")
        return previous[:start] + region + previous[finish + len(GENERATED_END) :]
    if previous:
        if previous.splitlines()[0] != LEGACY_TITLE:
            raise ValueError("unrecognized nonempty legacy guide title")
        manual = _manual_legacy_sections(previous)
        return region + ("\n\n" + manual if manual else "\n")
    return region + "\n"
