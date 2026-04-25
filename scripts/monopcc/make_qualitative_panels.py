#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np
import tifffile
from PIL import Image
from tqdm import tqdm


def load_rows(path: Path) -> list[dict]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))

    out = []
    for r in rows:
        rr = dict(r)
        for k, v in rr.items():
            if k in {"pred_index", "frame_id", "valid_pixels"}:
                rr[k] = int(v)
            elif k not in {"split", "folder", "side", "image_path", "gt_path", "selection_category", "selection_metric"}:
                rr[k] = float(v)
        out.append(rr)
    return out


def normalize_for_display(x: np.ndarray, valid_mask: np.ndarray | None = None, percentile: float = 99.0) -> np.ndarray:
    x = x.astype(np.float32)

    if valid_mask is None:
        valid = np.isfinite(x)
    else:
        valid = valid_mask & np.isfinite(x)

    if valid.sum() == 0:
        return np.zeros_like(x, dtype=np.float32)

    vals = x[valid]
    vmin = np.percentile(vals, 1.0)
    vmax = np.percentile(vals, percentile)

    if not np.isfinite(vmin) or not np.isfinite(vmax) or vmax <= vmin:
        return np.zeros_like(x, dtype=np.float32)

    y = (x - vmin) / (vmax - vmin)
    y = np.clip(y, 0.0, 1.0)
    y[~np.isfinite(y)] = 0.0
    return y


def compute_aligned_pred_and_error(gt_depth: np.ndarray, pred_depth: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    h, w = gt_depth.shape
    pred_resized = cv2.resize(pred_depth.astype(np.float32), (w, h))

    min_depth = 0.1
    max_depth = 150.0

    valid = np.isfinite(gt_depth) & np.isfinite(pred_resized)
    valid &= (gt_depth > min_depth) & (gt_depth < max_depth)

    aligned = pred_resized.copy()

    if valid.sum() > 0:
        valid_gt = gt_depth[valid]
        valid_pred = pred_resized[valid]

        pred_med = np.median(valid_pred)
        gt_med = np.median(valid_gt)

        if np.isfinite(pred_med) and pred_med > 0 and np.isfinite(gt_med) and gt_med > 0:
            aligned = pred_resized * (gt_med / pred_med)

    aligned = np.clip(aligned, min_depth, max_depth)
    abs_err = np.abs(gt_depth - aligned)
    abs_err[~valid] = np.nan

    return aligned, abs_err, valid


def make_panel(
    rgb: np.ndarray,
    gt_depth: np.ndarray,
    pred_depth: np.ndarray,
    meta: dict,
    out_path: Path,
) -> None:
    aligned_pred, abs_err, valid_mask = compute_aligned_pred_and_error(gt_depth, pred_depth)

    gt_vis = normalize_for_display(gt_depth, valid_mask)
    pred_vis = normalize_for_display(aligned_pred, valid_mask)
    err_vis = normalize_for_display(abs_err, valid_mask, percentile=99.0)

    fig, axes = plt.subplots(1, 4, figsize=(16, 4.5))

    axes[0].imshow(rgb)
    axes[0].set_title("RGB")

    im1 = axes[1].imshow(gt_vis, cmap="plasma")
    axes[1].set_title("GT depth")

    im2 = axes[2].imshow(pred_vis, cmap="plasma")
    axes[2].set_title("Pred depth")

    im3 = axes[3].imshow(err_vis, cmap="inferno")
    axes[3].set_title("Abs error")

    for ax in axes:
        ax.axis("off")

    title = (
        f"{meta['split']} | {meta['selection_category']} | "
        f"{meta['folder']} | frame {meta['frame_id']} | "
        f"abs_rel={meta['abs_rel']:.3f} | rmse={meta['rmse']:.3f} | a1={meta['a1']:.3f}"
    )
    fig.suptitle(title, fontsize=11)
    fig.tight_layout()
    fig.subplots_adjust(top=0.82)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=160, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--selected_csv", type=Path, required=True)
    parser.add_argument("--pred_file", type=Path, required=True)
    parser.add_argument("--out_dir", type=Path, required=True)
    args = parser.parse_args()

    rows = load_rows(args.selected_csv)
    preds = np.load(args.pred_file, fix_imports=True, encoding="latin1")["data"].squeeze()

    args.out_dir.mkdir(parents=True, exist_ok=True)

    for row in tqdm(rows):
        rgb = np.array(Image.open(row["image_path"]).convert("RGB"))
        rgb_h, rgb_w = rgb.shape[:2]

        gt_depth = tifffile.imread(row["gt_path"])[..., 2].astype(np.float32)
        pred_depth = preds[row["pred_index"]].astype(np.float32)

        # crop stacked GT to match left RGB image
        if gt_depth.shape[0] == 2 * rgb_h and gt_depth.shape[1] == rgb_w:
            gt_depth = gt_depth[:rgb_h, :]

        if gt_depth.shape != (rgb_h, rgb_w):
            print(
                "Skipping panel due to shape mismatch:",
                row["split"],
                row["folder"],
                row["frame_id"],
                "gt=",
                gt_depth.shape,
                "rgb=",
                (rgb_h, rgb_w),
            )
            continue

        name = (
            f"{row['split']}_"
            f"{row['selection_category']}_"
            f"{row['folder'].replace('/', '_')}_"
            f"{int(row['frame_id']):06d}.png"
        )
        out_path = args.out_dir / row["selection_category"] / name

        make_panel(rgb, gt_depth, pred_depth, row, out_path)

    print("saved panels to:", args.out_dir)


if __name__ == "__main__":
    main()