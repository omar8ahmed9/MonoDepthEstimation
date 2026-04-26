#!/usr/bin/env bash
set -euo pipefail

mkdir -p /home/khuyen.pham/MonoDepthEstimation/results/EndoMUST/per-sample-main

/home/khuyen.pham/miniconda3/envs/endodac/bin/python /home/khuyen.pham/MonoDepthEstimation/scripts/EndoMUST/analyze_per_sample_split.py \
  --data_root /l/users/omar.mohamed/datasets/SCARED_prepared_fixed \
  --results_dir /home/khuyen.pham/MonoDepthEstimation/results/EndoMUST/folds \
  --splits_dir /home/khuyen.pham/MonoDepthEstimation/data/splits \
  --summary_csv /home/khuyen.pham/MonoDepthEstimation/results/EndoMUST/summary/EndoMUST_fold_summary.csv \
  --out_dir /home/khuyen.pham/MonoDepthEstimation/results/EndoMUST/per-sample-main \
  --model_name EndoMUST \
  --splits test