#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path


LOWER_BETTER = {"abs_rel", "sq_rel", "rmse", "rmse_log"}
HIGHER_BETTER = {"a1", "a2", "a3"}


def load_rows(path: Path) -> list[dict]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))

    out = []
    for r in rows:
        rr = dict(r)
        for k, v in rr.items():
            if k in {"pred_index", "frame_id", "valid_pixels", "image_h", "image_w"}:
                rr[k] = int(v)
            elif k not in {"split", "folder", "side", "image_path", "gt_path"}:
                rr[k] = float(v)
        out.append(rr)
    return out


def sort_rows(rows: list[dict], metric: str) -> list[dict]:
    reverse = metric in HIGHER_BETTER
    return sorted(rows, key=lambda r: r[metric], reverse=reverse)


def pick_best(rows: list[dict], metric: str, n: int) -> list[dict]:
    ranked = sort_rows(rows, metric)
    return ranked[:n]


def pick_worst(rows: list[dict], metric: str, n: int) -> list[dict]:
    ranked = sort_rows(rows, metric)
    return ranked[-n:]


def pick_median(rows: list[dict], metric: str, n: int) -> list[dict]:
    ranked = sort_rows(rows, metric)
    m = len(ranked) // 2
    half = n // 2

    if n % 2 == 1:
        start = max(0, m - half)
        end = min(len(ranked), m + half + 1)
    else:
        start = max(0, m - half)
        end = min(len(ranked), m + half)

    picked = ranked[start:end]

    while len(picked) < n and start > 0:
        start -= 1
        picked = ranked[start:end]
    while len(picked) < n and end < len(ranked):
        end += 1
        picked = ranked[start:end]

    return picked[:n]


def add_category(rows: list[dict], category: str, metric: str) -> list[dict]:
    out = []
    for r in rows:
        rr = dict(r)
        rr["selection_category"] = category
        rr["selection_metric"] = metric
        out.append(rr)
    return out


def write_csv(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--per_sample_dir", type=Path, required=True)
    parser.add_argument("--out_dir", type=Path, required=True)
    parser.add_argument("--model_name", type=str, required=True)
    parser.add_argument("--metric", type=str, default="abs_rel",
                        choices=["abs_rel", "sq_rel", "rmse", "rmse_log", "a1", "a2", "a3"])
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--folds", nargs="+", required=True)
    parser.add_argument("--min_valid_ratio", type=float, default=0.0)
    parser.add_argument("--min_valid_pixels", type=int, default=0)
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)

    all_selected = []

    for fold in args.folds:
        csv_path = args.per_sample_dir / f"{fold}_per_sample.csv"
        rows = load_rows(csv_path)
        total_before = len(rows)

        filtered = rows

        if args.min_valid_ratio > 0:
            filtered = [r for r in filtered if r.get("valid_ratio", 0.0) >= args.min_valid_ratio]

        if args.min_valid_pixels > 0:
            filtered = [r for r in filtered if r.get("valid_pixels", 0) >= args.min_valid_pixels]

        rows = filtered

        print(
            f"{fold}: total={total_before}, after_filter={len(rows)}, "
            f"min_valid_ratio={args.min_valid_ratio}, min_valid_pixels={args.min_valid_pixels}"
        )

        if len(rows) == 0:
            raise RuntimeError(f"No rows left after filtering for {fold}")

        best = add_category(pick_best(rows, args.metric, args.count), "best", args.metric)
        median = add_category(pick_median(rows, args.metric, args.count), "median", args.metric)
        worst = add_category(pick_worst(rows, args.metric, args.count), "worst", args.metric)

        combined = best + median + worst

        out_csv = args.out_dir / f"{fold}_selected_{args.metric}.csv"
        write_csv(combined, out_csv)

        print(f"{fold}: saved {out_csv} ({len(combined)} rows)")
        all_selected.extend(combined)

    summary_csv = args.out_dir / f"{args.model_name}_selected_samples_{args.metric}.csv"
    write_csv(all_selected, summary_csv)

    print("\nSaved combined file:")
    print(summary_csv)


if __name__ == "__main__":
    main()