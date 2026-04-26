mkdir -p /l/users/saif.alkindi/projects/ai7102_project/MonoDepthEstimation/results/depth_pro/summary

python /l/users/saif.alkindi/projects/ai7102_project/MonoDepthEstimation/scripts/depth_pro/analyze_fold_metrics.py \
  --metrics_dir /l/users/saif.alkindi/projects/ai7102_project/MonoDepthEstimation/results/depth_pro/folds \
  --out_dir /l/users/saif.alkindi/projects/ai7102_project/MonoDepthEstimation/results/depth_pro/summary \
  --out_prefix depth_pro