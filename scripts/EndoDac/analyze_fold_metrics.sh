mkdir -p /home/khuyen.pham/MonoDepthEstimation/results/EndoDac/summary

/home/khuyen.pham/miniconda3/envs/endodac/bin/python /home/khuyen.pham/MonoDepthEstimation/scripts/EndoDac/analyze_fold_metrics.py \
  --metrics_dir /home/khuyen.pham/MonoDepthEstimation/results/EndoDac/folds \
  --out_dir /home/khuyen.pham/MonoDepthEstimation/results/EndoDac/summary \
  --out_prefix EndoDac