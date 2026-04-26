#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import re
import statistics as stats
from pathlib import Path


METRIC_NAMES = ["abs_rel", "sq_rel", "rmse", "rmse_log", "a1", "a2", "a3"]
COUNT_NAMES = ["total_samples", "valid_samples", "skipped_samples", "skip_pct"]


def parse_metrics_file(path: Path) -> dict:
    text = path.read_text()

    total = re.search(r"Total samples\s*:\s*(\d+)", text)
    valid = re.search(r"Valid samples\s*:\s*(\d+)", text)
    skipped = re.search(r"Skipped samples\s*:\s*(\d+)", text)

    metric_line = None
    for line in text.splitlines():
        if line.strip().startswith("&"):
            metric_line = line
            break

    if metric_line is None:
        raise RuntimeError(f"Could not find metric row in {path}")

    nums = re.findall(r"[-+]?\d+\.\d+", metric_line)
    if len(nums) != 7:
        raise RuntimeError(f"Expected 7 metrics in {path}, found {len(nums)}")

    total_val = int(total.group(1)) if total else 0
    valid_val = int(valid.group(1)) if valid else 0
    skipped_val = int(skipped.group(1)) if skipped else 0
    skip_pct = (100.0 * skipped_val / total_val) if total_val > 0 else 0.0

    return {
        "split": path.stem.replace("_metrics", ""),
        "total_samples": total_val,
        "valid_samples": valid_val,
        "skipped_samples": skipped_val,
        "skip_pct": round(skip_pct, 3),
        "abs_rel": float(nums[0]),
        "sq_rel": float(nums[1]),
        "rmse": float(nums[2]),
        "rmse_log": float(nums[3]),
        "a1": float(nums[4]),
        "a2": float(nums[5]),
        "a3": float(nums[6]),
    }


def load_rows(metrics_dir: Path) -> list[dict]:
    files = [
        metrics_dir / "test_main_metrics.txt",
        metrics_dir / "test_fold1_metrics.txt",
        metrics_dir / "test_fold2_metrics.txt",
        metrics_dir / "test_fold3_metrics.txt",
        metrics_dir / "test_fold4_metrics.txt",
        metrics_dir / "test_fold5_metrics.txt",
    ]

    missing = [str(f) for f in files if not f.exists()]
    if missing:
        raise FileNotFoundError("Missing metric files:\n" + "\n".join(missing))

    return [parse_metrics_file(f) for f in files]


def write_csv(rows: list[dict], out_csv: Path) -> None:
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def summarize_folds(rows: list[dict]) -> tuple[list[dict], list[dict]]:
    main_row = next(r for r in rows if r["split"] == "test_main")
    fold_rows = [r for r in rows if r["split"].startswith("test_fold")]

    summary = []
    for name in COUNT_NAMES + METRIC_NAMES:
        vals = [float(r[name]) for r in fold_rows]
        mean = stats.mean(vals)
        std = stats.stdev(vals) if len(vals) > 1 else 0.0
        vmin = min(vals)
        vmax = max(vals)
        main = float(main_row[name])

        summary.append({
            "metric": name,
            "main": round(main, 6),
            "fold_mean": round(mean, 6),
            "fold_std": round(std, 6),
            "fold_min": round(vmin, 6),
            "fold_max": round(vmax, 6),
        })

    ranking = []
    for name in ["abs_rel", "sq_rel", "rmse", "rmse_log"]:
        vals = [(r["split"], float(r[name])) for r in fold_rows]
        best = min(vals, key=lambda x: x[1])
        worst = max(vals, key=lambda x: x[1])
        ranking.append({
            "metric": name,
            "best_fold": best[0],
            "best_value": round(best[1], 6),
            "worst_fold": worst[0],
            "worst_value": round(worst[1], 6),
        })

    for name in ["a1", "a2", "a3"]:
        vals = [(r["split"], float(r[name])) for r in fold_rows]
        best = max(vals, key=lambda x: x[1])
        worst = min(vals, key=lambda x: x[1])
        ranking.append({
            "metric": name,
            "best_fold": best[0],
            "best_value": round(best[1], 6),
            "worst_fold": worst[0],
            "worst_value": round(worst[1], 6),
        })

    return summary, ranking


def print_report(rows: list[dict], summary: list[dict], ranking: list[dict]) -> str:
    lines = []

    lines.append("=== PER-SPLIT SUMMARY ===")
    for r in rows:
        lines.append(
            f"{r['split']:12s} | total={r['total_samples']:4d} | "
            f"valid={r['valid_samples']:4d} | skipped={r['skipped_samples']:4d} | "
            f"skip%={r['skip_pct']:6.3f} | abs_rel={r['abs_rel']:.3f} | "
            f"rmse={r['rmse']:.3f} | a1={r['a1']:.3f}"
        )

    lines.append("")
    lines.append("=== MAIN TEST VS 5-FOLD STATS ===")
    for s in summary:
        lines.append(
            f"{s['metric']:14s} | main={s['main']:.6f} | "
            f"fold_mean={s['fold_mean']:.6f} | fold_std={s['fold_std']:.6f} | "
            f"min={s['fold_min']:.6f} | max={s['fold_max']:.6f}"
        )

    lines.append("")
    lines.append("=== HARDEST / EASIEST FOLDS ===")
    for r in ranking:
        lines.append(
            f"{r['metric']:10s} | best={r['best_fold']} ({r['best_value']:.6f}) | "
            f"worst={r['worst_fold']} ({r['worst_value']:.6f})"
        )

    report = "\n".join(lines)
    print(report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--metrics_dir",
        type=Path,
        required=True,
        help="Directory containing test_main_metrics.txt and test_fold1..5_metrics.txt",
    )
    parser.add_argument(
        "--out_dir",
        type=Path,
        required=True,
        help="Directory where the summary outputs will be saved",
    )
    parser.add_argument(
        "--out_prefix",
        type=str,
        default="model",
        help="Prefix for output files, e.g. depth_pro",
    )
    args = parser.parse_args()

    rows = load_rows(args.metrics_dir)
    summary, ranking = summarize_folds(rows)

    args.out_dir.mkdir(parents=True, exist_ok=True)

    summary_csv = args.out_dir / f"{args.out_prefix}_fold_summary.csv"
    stats_csv = args.out_dir / f"{args.out_prefix}_fold_stats.csv"
    rank_csv = args.out_dir / f"{args.out_prefix}_fold_ranking.csv"
    report_txt = args.out_dir / f"{args.out_prefix}_fold_report.txt"

    write_csv(rows, summary_csv)
    write_csv(summary, stats_csv)
    write_csv(ranking, rank_csv)
    report = print_report(rows, summary, ranking)
    report_txt.write_text(report + "\n")

    print("\nSaved files:")
    print(summary_csv)
    print(stats_csv)
    print(rank_csv)
    print(report_txt)


if __name__ == "__main__":
    main()