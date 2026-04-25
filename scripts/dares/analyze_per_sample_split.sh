#!/usr/bin/env bash
set -euo pipefail

mkdir -p /l/users/saif.alkindi/projects/ai7102_project/MonoDepthEstimation/results/dares/per-sample-main

python /l/users/saif.alkindi/projects/ai7102_project/MonoDepthEstimation/scripts/dares/analyze_per_sample_split.py \
  --data_root /l/users/omar.mohamed/datasets/SCARED_prepared_fixed \
  --results_dir /l/users/saif.alkindi/projects/ai7102_project/MonoDepthEstimation/results/dares/folds \
  --splits_dir /l/users/saif.alkindi/projects/ai7102_project/MonoDepthEstimation/data/splits \
  --summary_csv /l/users/saif.alkindi/projects/ai7102_project/MonoDepthEstimation/results/dares/summary/dares_fold_summary.csv \
  --out_dir /l/users/saif.alkindi/projects/ai7102_project/MonoDepthEstimation/results/dares/per-sample-main \
  --model_name dares \
  --splits test
