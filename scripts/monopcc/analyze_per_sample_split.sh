#!/usr/bin/env bash
set -euo pipefail

mkdir -p /home/hamdan.alhadhrami/MonoDepthEstimation/results/MonoPCC/per-sample-main

python /home/hamdan.alhadhrami/MonoDepthEstimation/scripts/monopcc/analyze_per_sample_split.py \
  --data_root /l/users/omar.mohamed/datasets/SCARED_prepared_fixed \
  --results_dir /home/hamdan.alhadhrami/MonoDepthEstimation/results/MonoPCC/folds \
  --splits_dir /home/hamdan.alhadhrami/MonoDepthEstimation/data/splits \
  --summary_csv /home/hamdan.alhadhrami/MonoDepthEstimation/results/MonoPCC/summary/monopcc_fold_summary.csv \
  --out_dir /home/hamdan.alhadhrami/MonoDepthEstimation/results/MonoPCC/per-sample-main \
  --model_name monopcc \
  --splits test
