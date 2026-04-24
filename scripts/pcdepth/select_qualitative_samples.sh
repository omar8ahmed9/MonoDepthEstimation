#!/usr/bin/env bash
set -euo pipefail

mkdir -p /home/omar.mohamed/projects/MonoDepthEstimation/results/pcdepth/per-sample-main/selected

python /home/omar.mohamed/projects/MonoDepthEstimation/scripts/select_qualitative_samples.py \
  --per_sample_dir /home/omar.mohamed/projects/MonoDepthEstimation/results/pcdepth/per-sample-main \
  --out_dir /home/omar.mohamed/projects/MonoDepthEstimation/results/pcdepth/per-sample-main/selected \
  --model_name pcdepth_main \
  --metric abs_rel \
  --count 5 \
  --min_valid_ratio 0.05 \
  --min_valid_pixels 50000 \
  --folds test