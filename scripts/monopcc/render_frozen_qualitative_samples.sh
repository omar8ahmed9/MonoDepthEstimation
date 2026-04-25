#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="/home/hamdan.alhadhrami/MonoDepthEstimation"
MODEL_NAME="MonoPCC"

python "$REPO_ROOT/scripts/monopcc/render_frozen_qualitative_samples.py" \
  --frozen_csv "$REPO_ROOT/results/common/common_qualitative_samples.csv" \
  --pred_file "$REPO_ROOT/results/$MODEL_NAME/folds/test_main_pred.npz" \
  --out_dir "$REPO_ROOT/results/$MODEL_NAME/frozen_visualizations" \
  --model_name "$MODEL_NAME"
