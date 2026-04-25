#!/usr/bin/env bash
set -euo pipefail

mkdir -p /l/users/saif.alkindi/projects/ai7102_project/MonoDepthEstimation/results/dares/per-sample-main/selected

python /l/users/saif.alkindi/projects/ai7102_project/MonoDepthEstimation/scripts/dares/select_qualitative_samples.py \
  --per_sample_dir /l/users/saif.alkindi/projects/ai7102_project/MonoDepthEstimation/results/dares/per-sample-main \
  --out_dir /l/users/saif.alkindi/projects/ai7102_project/MonoDepthEstimation/results/dares/per-sample-main/selected \
  --model_name dares_main \
  --metric abs_rel \
  --count 5 \
  --min_valid_ratio 0.05 \
  --min_valid_pixels 50000 \
  --folds test
