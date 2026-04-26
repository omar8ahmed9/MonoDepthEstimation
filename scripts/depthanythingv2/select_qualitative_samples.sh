#!/usr/bin/env bash
set -euo pipefail

mkdir -p /home/hamdan.alhadhrami/MonoDepthEstimation/results/DepthAnythingV2/per-sample-main/selected

python /home/hamdan.alhadhrami/MonoDepthEstimation/scripts/depthanythingv2/select_qualitative_samples.py \
  --per_sample_dir /home/hamdan.alhadhrami/MonoDepthEstimation/results/DepthAnythingV2/per-sample-main \
  --out_dir /home/hamdan.alhadhrami/MonoDepthEstimation/results/DepthAnythingV2/per-sample-main/selected \
  --model_name depthanythingv2_main \
  --metric abs_rel \
  --count 5 \
  --min_valid_ratio 0.05 \
  --min_valid_pixels 50000 \
  --folds test
