mkdir -p /l/users/saif.alkindi/projects/ai7102_project/MonoDepthEstimation/results/dares/summary

python /l/users/saif.alkindi/projects/ai7102_project/MonoDepthEstimation/scripts/dares/analyze_fold_metrics.py \
  --metrics_dir /l/users/saif.alkindi/projects/ai7102_project/MonoDepthEstimation/results/dares/folds \
  --out_dir /l/users/saif.alkindi/projects/ai7102_project/MonoDepthEstimation/results/dares/summary \
  --out_prefix dares
