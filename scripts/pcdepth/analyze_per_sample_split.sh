#!/usr/bin/env bash
set -euo pipefail

mkdir -p /home/omar.mohamed/projects/MonoDepthEstimation/results/pcdepth/per-sample-main

python /home/omar.mohamed/projects/MonoDepthEstimation/scripts/analyze_per_sample_split.py \
  --data_root /l/users/omar.mohamed/datasets/SCARED_prepared_fixed \
  --results_dir /home/omar.mohamed/projects/MonoDepthEstimation/results/pcdepth/folds \
  --splits_dir /home/omar.mohamed/projects/MonoDepthEstimation/data/splits \
  --summary_csv /home/omar.mohamed/projects/MonoDepthEstimation/results/pcdepth/summary/pcdepth_fold_summary.csv \
  --out_dir /home/omar.mohamed/projects/MonoDepthEstimation/results/pcdepth/per-sample-main \
  --model_name pcdepth \
  --splits test