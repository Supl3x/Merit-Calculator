# ── Merit Calculator — GPA.txt Parser ─────────────────────────────────────────
"""
Parse the raw GPA.txt file into a clean Pandas DataFrame.

The file is whitespace-aligned (NOT comma-separated) with repeated header
rows interspersed at lines 1, 54, 107, 160, 213, 266.  Each data row has
the structure:

    CT-NNN  NAME  CGPA  SECTION  CHOICE1  CHOICE2  CHOICE3  CHOICE4  CHOICE5

Specialization names are multi-word and share some common tokens, so the
parser uses known specialization names as delimiters to split the line.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

import pandas as pd

from data.models import NO_RESPONSE, SPECIALIZATIONS, CHOICE_COLUMNS

# All valid specialization names (longest first so greedy match works)
_SPEC_NAMES = sorted(SPECIALIZATIONS.keys(), key=len, reverse=True)
_SPEC_NAMES.append(NO_RESPONSE)

# Pre-compile the pattern that splits a line into its 5 choice slots.
# It matches any known specialization name OR "No response submitted".
_SPEC_RE = re.compile(
    r"("
    + "|".join(re.escape(s) for s in _SPEC_NAMES)
    + r")"
)

_HEADER_MARKER = "Roll No"

# Locate the data file relative to this module
_DATA_DIR = Path(__file__).resolve().parent
_DEFAULT_PATH = _DATA_DIR / "GPA.txt"


def _is_header_line(line: str) -> bool:
    """Return True if the line is one of the repeated header rows."""
    return line.strip().startswith(_HEADER_MARKER)


def _parse_line(line: str) -> dict | None:
    """
    Parse a single data line into a dict with keys:
        roll_no, name, cgpa, section,
        choice_1 .. choice_5
    Returns None for header / blank / unparseable lines.
    """
    line = line.strip()
    if not line or _is_header_line(line):
        return None

    # ── 1. Extract roll number (CT-NNN) ──────────────────────────────────
    roll_match = re.match(r"(CT-\d+)", line)
    if not roll_match:
        return None
    roll_no = roll_match.group(1)
    rest = line[roll_match.end():].strip()

    # ── 2. Find all specialization / "No response" tokens ────────────────
    spec_matches = list(_SPEC_RE.finditer(rest))

    # If there are 0 matches, we cannot parse choices.
    if not spec_matches:
        # Could be a student whose entire row is name + CGPA + section only
        # with all "No response submitted" already handled.
        return None

    # Everything before the first specialization token = "NAME  CGPA  SECTION"
    preamble = rest[: spec_matches[0].start()].strip()

    # ── 3. Extract section (single letter at the end of preamble) ────────
    # Preamble looks like "JAVERIA IRFAN ALI 3.673 A"
    # Edge case: some students have no section (e.g. "MUHAMMAD OMER BARI 0.000")
    preamble_parts = preamble.rsplit(maxsplit=2)

    section = None
    cgpa = None
    name = None

    if len(preamble_parts) >= 3:
        candidate_section = preamble_parts[-1]
        # Valid section is a single uppercase letter
        if len(candidate_section) == 1 and candidate_section.isalpha():
            section = candidate_section.upper()
            try:
                cgpa = float(preamble_parts[-2])
            except ValueError:
                return None
            name = " ".join(preamble_parts[:-2]).strip()
        else:
            # Last token is NOT a section — try treating last as CGPA
            try:
                cgpa = float(preamble_parts[-1])
                section = "?"
                name = " ".join(preamble_parts[:-1]).strip()
            except ValueError:
                return None

    elif len(preamble_parts) == 2:
        # Only two parts: could be "NAME CGPA" without section
        try:
            cgpa = float(preamble_parts[-1])
            section = "?"
            name = preamble_parts[0].strip()
        except ValueError:
            return None
    else:
        return None

    if name is None or cgpa is None:
        return None

    # ── 4. Extract the 5 choices ─────────────────────────────────────────
    choices: list[str] = [m.group(1) for m in spec_matches]

    # Pad to exactly 5 if fewer were found (some students have partial data)
    while len(choices) < 5:
        choices.append(NO_RESPONSE)
    choices = choices[:5]  # Safety cap

    return {
        "roll_no": roll_no,
        "name": name.title(),  # Normalise casing
        "cgpa": cgpa,
        "section": section.upper(),
        **{CHOICE_COLUMNS[i]: choices[i] for i in range(5)},
    }


def load_data(filepath: str | Path | None = None) -> pd.DataFrame:
    """
    Load and parse GPA.txt into a clean DataFrame.

    Parameters
    ----------
    filepath : path to the GPA.txt file. Defaults to ``data/GPA.txt``.

    Returns
    -------
    pd.DataFrame sorted by CGPA descending, roll_no ascending (tiebreak).
    Includes ALL students — callers can filter out "No Data" students.
    """
    if filepath is None:
        filepath = _DEFAULT_PATH
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"Data file not found: {filepath}")

    rows: list[dict] = []
    with open(filepath, encoding="utf-8") as fh:
        for line in fh:
            parsed = _parse_line(line)
            if parsed is not None:
                rows.append(parsed)

    df = pd.DataFrame(rows)

    # ── Derived columns ──────────────────────────────────────────────────
    # Numeric roll for sorting (extract the number after CT-)
    df["roll_num"] = df["roll_no"].str.extract(r"(\d+)").astype(int)

    # Flag students with no valid data
    df["has_data"] = df["choice_1"] != NO_RESPONSE

    # Sort: CGPA desc, then roll_num asc (tiebreaker)
    df = df.sort_values(
        ["cgpa", "roll_num"], ascending=[False, True]
    ).reset_index(drop=True)

    return df


# ── Quick self-test ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    df = load_data()
    print(f"Total students parsed: {len(df)}")
    print(f"Students with data   : {df['has_data'].sum()}")
    print(f"Sections             : {sorted(df['section'].unique())}")
    print(f"\nTop 5 by CGPA:")
    print(df[["roll_no", "name", "cgpa", "section", "choice_1"]].head())
    print(f"\nBottom 5 by CGPA:")
    print(df[["roll_no", "name", "cgpa", "section", "choice_1"]].tail())
