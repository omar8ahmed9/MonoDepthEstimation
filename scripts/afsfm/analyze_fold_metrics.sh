mkdir -p /l/users/saif.alkindi/projects/ai7102_project/MonoDepthEstimation/results/afsfm/summary

python /l/users/saif.alkindi/projects/ai7102_project/MonoDepthEstimation/scripts/afsfm/analyze_fold_metrics.py \
  --metrics_dir /l/users/saif.alkindi/projects/ai7102_project/MonoDepthEstimation/results/afsfm/folds \
  --out_dir /l/users/saif.alkindi/projects/ai7102_project/MonoDepthEstimation/results/afsfm/summary \
  --out_prefix afsfm