#!/usr/bin/env bash
set -euo pipefail

mkdir -p /l/users/saif.alkindi/projects/ai7102_project/MonoDepthEstimation/results/depth_pro/per-sample-main

python /l/users/saif.alkindi/projects/ai7102_project/MonoDepthEstimation/scripts/depth_pro/analyze_per_sample_split.py \
  --data_root /l/users/omar.mohamed/datasets/SCARED_prepared_fixed \
  --results_dir /l/users/saif.alkindi/projects/ai7102_project/MonoDepthEstimation/results/depth_pro/folds \
  --splits_dir /l/users/saif.alkindi/projects/ai7102_project/MonoDepthEstimation/data/splits \
  --summary_csv /l/users/saif.alkindi/projects/ai7102_project/MonoDepthEstimation/results/depth_pro/summary/depth_pro_fold_summary.csv \
  --out_dir /l/users/saif.alkindi/projects/ai7102_project/MonoDepthEstimation/results/depth_pro/per-sample-main \
  --model_name depth_pro \
  --splits test