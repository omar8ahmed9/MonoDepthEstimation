#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="/home/khuyen.pham/MonoDepthEstimation"
MODEL_NAME="EndoDac"

/home/khuyen.pham/miniconda3/envs/endodac/bin/python "$REPO_ROOT/scripts/EndoDac/render_frozen_qualitative_samples.py" \
  --frozen_csv "$REPO_ROOT/results/common/common_qualitative_samples.csv" \
  --pred_file "$REPO_ROOT/results/$MODEL_NAME/folds/test_main_pred.npz" \
  --out_dir "$REPO_ROOT/results/$MODEL_NAME/frozen_visualizations" \
  --model_name "$MODEL_NAME"