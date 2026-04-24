mkdir -p /home/omar.mohamed/projects/MonoDepthEstimation/results/pcdepth/summary

python /home/omar.mohamed/projects/MonoDepthEstimation/scripts/analyze_fold_metrics.py \
  --metrics_dir /home/omar.mohamed/projects/MonoDepthEstimation/results/pcdepth/folds \
  --out_dir /home/omar.mohamed/projects/MonoDepthEstimation/results/pcdepth/summary \
  --out_prefix pcdepth