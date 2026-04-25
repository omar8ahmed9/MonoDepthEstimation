#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import cv2
import numpy as np
import tifffile
from tqdm import tqdm
from PIL import Image


LOWER_BETTER = {"abs_rel", "sq_rel", "rmse", "rmse_log"}
HIGHER_BETTER = {"a1", "a2", "a3"}


def readlines(path: Path) -> list[str]:
    return path.read_text().splitlines()


def compute_errors(gt: np.ndarray, pred: np.ndarray) -> dict | None:
    h, w = gt.shape
    pred = cv2.resize(pred, (w, h))

    min_depth = 0.1
    max_depth = 150.0

    valid = np.isfinite(gt) & np.isfinite(pred)
    valid &= (gt > min_depth) & (gt < max_depth)

    if valid.sum() == 0:
        return None

    valid_gt = gt[valid]
    valid_pred = pred[valid]

    pred_med = np.median(valid_pred)
    gt_med = np.median(valid_gt)

    if (not np.isfinite(pred_med)) or pred_med <= 0:
        return None
    if (not np.isfinite(gt_med)) or gt_med <= 0:
        return None

    valid_pred = valid_pred * (gt_med / pred_med)
    valid_pred = np.clip(valid_pred, min_depth, max_depth)

    thresh = np.maximum(valid_gt / valid_pred, valid_pred / valid_gt)
    a1 = float((thresh < 1.25).mean())
    a2 = float((thresh < 1.25 ** 2).mean())
    a3 = float((thresh < 1.25 ** 3).mean())

    rmse = float(np.sqrt(((valid_gt - valid_pred) ** 2).mean()))
    rmse_log = float(np.sqrt(((np.log(valid_gt) - np.log(valid_pred)) ** 2).mean()))
    abs_rel = float(np.mean(np.abs(valid_gt - valid_pred) / valid_gt))
    sq_rel = float(np.mean(((valid_gt - valid_pred) ** 2) / valid_gt))

    vals = [abs_rel, sq_rel, rmse, rmse_log, a1, a2, a3]
    if not np.isfinite(vals).all():
        return None

    return {
        "abs_rel": abs_rel,
        "sq_rel": sq_rel,
        "rmse": rmse,
        "rmse_log": rmse_log,
        "a1": a1,
        "a2": a2,
        "a3": a3,
        "valid_pixels": int(valid.sum()),
        "image_h": int(h),
        "image_w": int(w),
        "valid_ratio": float(valid.sum() / (h * w)),
    }


def parse_summary_csv(summary_csv: Path) -> list[dict]:
    with summary_csv.open(newline="") as f:
        rows = list(csv.DictReader(f))

    out = []
    for r in rows:
        if not r["split"].startswith("test_fold"):
            continue
        rr = dict(r)
        for k, v in rr.items():
            if k != "split":
                rr[k] = float(v)
        out.append(rr)
    return out


def rank_folds(rows: list[dict], metric: str) -> list[dict]:
    reverse = metric in HIGHER_BETTER
    return sorted(rows, key=lambda r: r[metric], reverse=reverse)


def select_folds(rows: list[dict], metric: str) -> dict:
    ranked = rank_folds(rows, metric)
    return {
        "metric": metric,
        "easy_fold": ranked[0]["split"],
        "easy_value": ranked[0][metric],
        "median_fold": ranked[len(ranked) // 2]["split"],
        "median_value": ranked[len(ranked) // 2][metric],
        "hard_fold": ranked[-1]["split"],
        "hard_value": ranked[-1][metric],
    }


def average_rank_selection(rows: list[dict], metrics: list[str]) -> dict:
    scores = {r["split"]: 0.0 for r in rows}
    for metric in metrics:
        ranked = rank_folds(rows, metric)
        for idx, r in enumerate(ranked):
            scores[r["split"]] += idx

    ordered = sorted(scores.items(), key=lambda x: x[1])
    return {
        "easy_fold": ordered[0][0],
        "median_fold": ordered[len(ordered) // 2][0],
        "hard_fold": ordered[-1][0],
        "scores": scores,
    }


def analyze_one_split(
    pred_file: Path,
    split_file: Path,
    data_root: Path,
    out_csv: Path,
    split_name: str,
) -> tuple[int, int]:
    preds = np.load(pred_file, fix_imports=True, encoding="latin1")["data"].squeeze()
    lines = readlines(split_file)

    if len(preds) != len(lines):
        raise ValueError(f"Mismatch for {split_name}: pred={len(preds)}, split={len(lines)}")

    rows = []
    skipped = 0

    for i, line in enumerate(tqdm(lines, desc=split_name)):
        folder, frame_id, side = line.split()
        frame_id = int(frame_id)

        image_path = data_root / folder / "data" / "left" / f"{frame_id:010d}.png"
        gt_path = data_root / folder / "data" / "scene_points" / f"scene_points{frame_id:06d}.tiff"

        rgb = np.array(Image.open(image_path).convert("RGB"))
        rgb_h, rgb_w = rgb.shape[:2]

        gt = tifffile.imread(gt_path)[..., 2].astype(np.float32)
        pred = preds[i].astype(np.float32)

        # Crop stacked GT to match left RGB image
        if gt.shape[0] == 2 * rgb_h and gt.shape[1] == rgb_w:
            gt = gt[:rgb_h, :]

        if gt.shape != (rgb_h, rgb_w):
            skipped += 1
            continue

        errs = compute_errors(gt, pred)
        if errs is None:
            skipped += 1
            continue

        row = {
            "split": split_name,
            "pred_index": i,
            "folder": folder,
            "frame_id": frame_id,
            "side": side,
            "image_path": str(image_path),
            "gt_path": str(gt_path),
            **errs,
        }
        rows.append(row)

    if len(rows) == 0:
        raise RuntimeError(f"No valid rows found for {split_name}")

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    return len(rows), skipped


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_root", type=Path, required=True)
    parser.add_argument("--results_dir", type=Path, required=True)
    parser.add_argument("--splits_dir", type=Path, required=True)
    parser.add_argument("--summary_csv", type=Path, required=True)
    parser.add_argument("--out_dir", type=Path, required=True)
    parser.add_argument("--model_name", type=str, required=True)
    parser.add_argument(
        "--primary_metric",
        type=str,
        default="abs_rel",
        choices=["abs_rel", "sq_rel", "rmse", "rmse_log", "a1", "a2", "a3"],
    )
    parser.add_argument(
        "--selection_mode",
        type=str,
        default="model_specific",
        choices=["model_specific", "common", "both"],
    )
    parser.add_argument(
        "--common_folds",
        nargs="*",
        default=["test_fold2", "test_fold4", "test_fold5"],
    )
    parser.add_argument(
        "--splits",
        nargs="*",
        default=None,
        help="Explicit split names to analyze, e.g. test_main",
    )
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)

    selected = []
    report = {"model_name": args.model_name}

    if args.splits:
        selected = list(args.splits)
        report["selection_mode"] = "explicit"
        report["explicit_splits"] = selected
    else:
        fold_rows = parse_summary_csv(args.summary_csv)

        primary_sel = select_folds(fold_rows, args.primary_metric)
        avg_sel = average_rank_selection(
            fold_rows,
            ["abs_rel", "sq_rel", "rmse", "rmse_log", "a1", "a2", "a3"],
        )

        report.update({
            "selection_mode": args.selection_mode,
            "common_folds": args.common_folds,
            "primary_metric_selection": primary_sel,
            "average_rank_selection": avg_sel,
        })

        if args.selection_mode in {"model_specific", "both"}:
            selected.extend([
                primary_sel["easy_fold"],
                primary_sel["median_fold"],
                primary_sel["hard_fold"],
            ])
        if args.selection_mode in {"common", "both"}:
            selected.extend(args.common_folds)

    seen = set()
    selected = [x for x in selected if not (x in seen or seen.add(x))]

    print("Selected splits:")
    for s in selected:
        print(" ", s)

    saved = []
    for split_name in selected:
        pred_file = args.results_dir / f"{split_name}_main_pred.npz"
        split_file = args.splits_dir / f"{split_name}_files.txt"
        out_csv = args.out_dir / f"{split_name}_per_sample.csv"

        rows, skipped = analyze_one_split(
            pred_file=pred_file,
            split_file=split_file,
            data_root=args.data_root,
            out_csv=out_csv,
            split_name=split_name,
        )
        saved.append({
            "split": split_name,
            "out_csv": str(out_csv),
            "rows": rows,
            "skipped": skipped,
        })
        print(f"saved: {out_csv} | rows={rows} | skipped={skipped}")

    report["saved_per_sample_files"] = saved

    txt_path = args.out_dir / f"{args.model_name}_selected_folds.txt"
    json_path = args.out_dir / f"{args.model_name}_selected_folds.json"

    lines = []
    lines.append(f"Model: {args.model_name}")
    lines.append(f"Selection mode: {report['selection_mode']}")
    lines.append("")

    if report["selection_mode"] == "explicit":
        lines.append("Explicit splits:")
        for x in selected:
            lines.append(f"  - {x}")
    else:
        lines.append("Common folds:")
        for x in args.common_folds:
            lines.append(f"  - {x}")
        lines.append("")
        lines.append(f"Primary metric selection ({args.primary_metric}):")
        lines.append(f"  easy   : {report['primary_metric_selection']['easy_fold']} ({report['primary_metric_selection']['easy_value']:.6f})")
        lines.append(f"  median : {report['primary_metric_selection']['median_fold']} ({report['primary_metric_selection']['median_value']:.6f})")
        lines.append(f"  hard   : {report['primary_metric_selection']['hard_fold']} ({report['primary_metric_selection']['hard_value']:.6f})")
        lines.append("")
        lines.append("Average-rank selection:")
        lines.append(f"  easy   : {report['average_rank_selection']['easy_fold']}")
        lines.append(f"  median : {report['average_rank_selection']['median_fold']}")
        lines.append(f"  hard   : {report['average_rank_selection']['hard_fold']}")

    lines.append("")
    lines.append("Generated per-sample CSVs:")
    for s in saved:
        lines.append(f"  - {s['split']}: {s['out_csv']} (rows={s['rows']}, skipped={s['skipped']})")

    txt_path.write_text("\n".join(lines) + "\n")
    json_path.write_text(json.dumps(report, indent=2) + "\n")

    print("\nSaved selection files:")
    print(txt_path)
    print(json_path)


if __name__ == "__main__":
    main()