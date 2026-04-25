#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path


REQUIRED_KEYS = [
    "split",
    "pred_index",
    "folder",
    "frame_id",
    "side",
    "image_path",
    "gt_path",
]

OPTIONAL_KEYS = [
    "selection_category",
    "selection_metric",
    "abs_rel",
    "sq_rel",
    "rmse",
    "rmse_log",
    "a1",
    "a2",
    "a3",
    "valid_pixels",
    "image_h",
    "image_w",
    "valid_ratio",
]


def load_rows(path: Path) -> list[dict]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def normalize_row(row: dict) -> dict:
    out = {}
    for k in REQUIRED_KEYS + OPTIONAL_KEYS:
        out[k] = row.get(k, "")
    return out


def make_sample_id(row: dict) -> str:
    return f"{row['split']}::{row['folder']}::{int(row['frame_id']):06d}::{row['side']}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_csv",
        type=Path,
        required=True,
        help="CSV containing candidate qualitative samples",
    )
    parser.add_argument(
        "--out_csv",
        type=Path,
        required=True,
        help="Frozen output CSV to reuse across models",
    )
    parser.add_argument(
        "--sample_ids",
        nargs="*",
        default=None,
        help="Optional explicit sample IDs in the form split::folder::000123::l",
    )
    parser.add_argument(
        "--categories",
        nargs="*",
        default=None,
        help="Optional categories to keep, e.g. best median worst",
    )
    parser.add_argument(
        "--max_per_category",
        type=int,
        default=None,
        help="Optional limit per category after filtering",
    )
    args = parser.parse_args()

    rows = [normalize_row(r) for r in load_rows(args.input_csv)]

    for r in rows:
        if r["pred_index"] != "":
            r["pred_index"] = int(r["pred_index"])
        if r["frame_id"] != "":
            r["frame_id"] = int(r["frame_id"])

    if args.sample_ids:
        wanted = set(args.sample_ids)
        rows = [r for r in rows if make_sample_id(r) in wanted]

    if args.categories:
        wanted_categories = set(args.categories)
        rows = [r for r in rows if r.get("selection_category", "") in wanted_categories]

    if args.max_per_category is not None:
        grouped = {}
        for r in rows:
            cat = r.get("selection_category", "")
            grouped.setdefault(cat, []).append(r)

        kept = []
        for cat, items in grouped.items():
            kept.extend(items[:args.max_per_category])
        rows = kept

    if len(rows) == 0:
        raise RuntimeError("No rows selected for export.")

    out_fields = REQUIRED_KEYS + ["sample_id"] + OPTIONAL_KEYS

    args.out_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.out_csv.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=out_fields)
        writer.writeheader()
        for r in rows:
            rr = dict(r)
            rr["sample_id"] = make_sample_id(r)
            writer.writerow(rr)

    print(f"saved: {args.out_csv}")
    print(f"rows : {len(rows)}")
    print("\nSample IDs:")
    for r in rows:
        print(" ", make_sample_id(r))


if __name__ == "__main__":
    main()