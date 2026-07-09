# ── Merit Calculator — Seat Allocation Engine ─────────────────────────────────
"""
Greedy merit-based seat allocation.

Algorithm
---------
1. Sort eligible students by CGPA (desc), roll_num (asc) as fallback order.
2. Initialise seat counters from ``models.SPECIALIZATIONS``.
3. For each student (highest GPA first):
   - Walk through choice_1 → choice_5.
   - If seats remain for that specialization → allocate, decrement, continue.
   - If no valid choice has seats → mark "Unallocated".
4. In case of **tied CGPA**: both students are processed with equal access
   to remaining seats (first by roll number order is the fallback, but the
   UI flags them as "Tied").

Outputs
-------
- ``allocated_df``: Original DataFrame + ``allocated``, ``alloc_choice``,
  ``is_tied`` columns.
- ``closing_merit``: Dict mapping specialization → info about the last
  student who took a seat in that category.
- ``remaining_seats``: Dict mapping specialization → seats still available.
"""

from __future__ import annotations

import pandas as pd

from data.models import SPECIALIZATIONS, CHOICE_COLUMNS, NO_RESPONSE


def allocate_seats(df: pd.DataFrame) -> dict:
    """
    Run the merit-based allocation algorithm.

    Parameters
    ----------
    df : DataFrame from ``parser.load_data()`` — already sorted by
         CGPA desc, roll_num asc.

    Returns
    -------
    dict with keys:
        ``allocated_df``   – DataFrame with allocation columns added.
        ``closing_merit``  – {spec_name: {"roll_no", "name", "cgpa", "section"}}.
        ``remaining_seats``– {spec_name: int}.
        ``seat_log``       – list of (roll_no, allocated_spec, choice_number)
                             in allocation order.
    """
    # ── Initialise seat counters ─────────────────────────────────────────
    remaining: dict[str, int] = {
        name: info["seats"] for name, info in SPECIALIZATIONS.items()
    }

    # Track last student allocated per specialization (= closing merit)
    last_allocated: dict[str, dict] = {}

    # Results per student (indexed by DataFrame index)
    alloc_spec: dict[int, str] = {}
    alloc_choice: dict[int, int] = {}  # which choice number (1–5) they got

    seat_log: list[tuple[str, str, int]] = []

    # ── Detect ties ──────────────────────────────────────────────────────
    tied_indices: set[int] = set()
    cgpa_list = df["cgpa"].tolist()
    for i in range(1, len(cgpa_list)):
        if cgpa_list[i] == cgpa_list[i - 1] and cgpa_list[i] > 0:
            tied_indices.add(df.index[i])
            tied_indices.add(df.index[i - 1])

    # ── Allocate ─────────────────────────────────────────────────────────
    for idx, row in df.iterrows():
        # Skip students without valid choices
        if not row["has_data"]:
            alloc_spec[idx] = "No Data"
            alloc_choice[idx] = 0
            continue

        allocated = False
        for choice_num, col in enumerate(CHOICE_COLUMNS, start=1):
            spec = row[col]
            if spec == NO_RESPONSE or spec not in remaining:
                continue
            if remaining[spec] > 0:
                remaining[spec] -= 1
                alloc_spec[idx] = spec
                alloc_choice[idx] = choice_num
                seat_log.append((row["roll_no"], spec, choice_num))
                last_allocated[spec] = {
                    "roll_no": row["roll_no"],
                    "name": row["name"],
                    "cgpa": row["cgpa"],
                    "section": row["section"],
                }
                allocated = True
                break

        if not allocated:
            alloc_spec[idx] = "Unallocated"
            alloc_choice[idx] = 0

    # ── Build result DataFrame ───────────────────────────────────────────
    result_df = df.copy()
    result_df["allocated"] = result_df.index.map(alloc_spec)
    result_df["alloc_choice"] = result_df.index.map(alloc_choice)
    result_df["is_tied"] = result_df.index.isin(tied_indices)

    return {
        "allocated_df": result_df,
        "closing_merit": last_allocated,
        "remaining_seats": remaining,
        "seat_log": seat_log,
    }


def get_student_availability(
    row: pd.Series, remaining_seats: dict[str, int]
) -> list[dict]:
    """
    For a specific student, show which specializations still have seats
    and whether any of their choices are available.

    Returns a list of dicts: [{spec, seats_left, is_in_choices, choice_rank}]
    """
    result = []
    student_choices = [row.get(c, NO_RESPONSE) for c in CHOICE_COLUMNS]

    for spec_name, info in SPECIALIZATIONS.items():
        seats_left = remaining_seats.get(spec_name, 0)
        choice_rank = None
        if spec_name in student_choices:
            choice_rank = student_choices.index(spec_name) + 1
        result.append({
            "specialization": spec_name,
            "emoji": info["emoji"],
            "seats_left": seats_left,
            "total_seats": info["seats"],
            "is_in_choices": spec_name in student_choices,
            "choice_rank": choice_rank,
        })
    return result


# ── Quick self-test ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    from data.parser import load_data

    df = load_data()
    result = allocate_seats(df)
    adf = result["allocated_df"]
    remaining = result["remaining_seats"]
    closing = result["closing_merit"]

    print("=== Allocation Summary ===")
    print(f"Total students     : {len(adf)}")
    print(f"With data          : {adf['has_data'].sum()}")
    print(f"Allocated          : {(adf['allocated'] != 'No Data').sum() - (adf['allocated'] == 'Unallocated').sum()}")
    print(f"Unallocated        : {(adf['allocated'] == 'Unallocated').sum()}")
    print(f"No Data            : {(adf['allocated'] == 'No Data').sum()}")
    print(f"Tied students      : {adf['is_tied'].sum()}")

    print("\n=== Remaining Seats ===")
    for spec, seats in remaining.items():
        print(f"  {spec:40s}: {seats}")

    print("\n=== Closing Merit ===")
    for spec, info in closing.items():
        print(f"  {spec:40s}: {info['name']:30s} GPA={info['cgpa']}")

    print("\n=== Choice Distribution ===")
    for i in range(6):
        count = (adf["alloc_choice"] == i).sum()
        label = f"Choice {i}" if i > 0 else "Not allocated"
        print(f"  {label}: {count}")
