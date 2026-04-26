#!/usr/bin/env bash
set -euo pipefail

mkdir -p /home/hamdan.alhadhrami/MonoDepthEstimation/results/DepthAnythingV2/per-sample-main

python /home/hamdan.alhadhrami/MonoDepthEstimation/scripts/depthanythingv2/analyze_per_sample_split.py \
  --data_root /l/users/omar.mohamed/datasets/SCARED_prepared_fixed \
  --results_dir /home/hamdan.alhadhrami/MonoDepthEstimation/results/DepthAnythingV2/folds \
  --splits_dir /home/hamdan.alhadhrami/MonoDepthEstimation/data/splits \
  --summary_csv /home/hamdan.alhadhrami/MonoDepthEstimation/results/DepthAnythingV2/summary/depthanythingv2_fold_summary.csv \
  --out_dir /home/hamdan.alhadhrami/MonoDepthEstimation/results/DepthAnythingV2/per-sample-main \
  --model_name depthanythingv2 \
  --splits test
