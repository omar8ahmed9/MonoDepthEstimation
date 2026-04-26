#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="/home/khuyen.pham/MonoDepthEstimation"
MODEL_NAME="EndoFASt3r"

SELECTED_DIR="$REPO_ROOT/results/$MODEL_NAME/per-sample-main/selected"
PRED_DIR="$REPO_ROOT/results/$MODEL_NAME/folds"
OUT_ROOT="$REPO_ROOT/results/$MODEL_NAME/visualizations"

SCRIPT="$REPO_ROOT/scripts/EndoFASt3r/make_qualitative_panels.py"

mkdir -p "$OUT_ROOT"

/home/khuyen.pham/miniconda3/envs/endodac/bin/python "$SCRIPT" \
  --selected_csv "$SELECTED_DIR/test_selected_abs_rel.csv" \
  --pred_file "$PRED_DIR/test_main_pred.npz" \
  --out_dir "$OUT_ROOT/test_main_abs_rel"

echo "Done. Saved visualizations under:"
echo "  $OUT_ROOT"