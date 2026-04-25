#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="/home/hamdan.alhadhrami/MonoDepthEstimation"
MODEL_NAME="MonoPCC"

SELECTED_DIR="$REPO_ROOT/results/$MODEL_NAME/per-sample-main/selected"
PRED_DIR="$REPO_ROOT/results/$MODEL_NAME/folds"
OUT_ROOT="$REPO_ROOT/results/$MODEL_NAME/visualizations"

SCRIPT="$REPO_ROOT/scripts/monopcc/make_qualitative_panels.py"

mkdir -p "$OUT_ROOT"

python "$SCRIPT" \
  --selected_csv "$SELECTED_DIR/test_selected_abs_rel.csv" \
  --pred_file "$PRED_DIR/test_main_pred.npz" \
  --out_dir "$OUT_ROOT/test_main_abs_rel"

echo "Done. Saved visualizations under:"
echo "  $OUT_ROOT"
