#!/usr/bin/env bash
set -euo pipefail

mkdir -p /home/khuyen.pham/MonoDepthEstimation/results/EndoFASt3r/per-sample-main/selected

/home/khuyen.pham/miniconda3/envs/endodac/bin/python /home/khuyen.pham/MonoDepthEstimation/scripts/EndoFASt3r/select_qualitative_samples.py \
  --per_sample_dir /home/khuyen.pham/MonoDepthEstimation/results/EndoFASt3r/per-sample-main \
  --out_dir /home/khuyen.pham/MonoDepthEstimation/results/EndoFASt3r/per-sample-main/selected \
  --model_name EndoFASt3r_main \
  --metric abs_rel \
  --count 5 \
  --min_valid_ratio 0.05 \
  --min_valid_pixels 50000 \
  --folds test