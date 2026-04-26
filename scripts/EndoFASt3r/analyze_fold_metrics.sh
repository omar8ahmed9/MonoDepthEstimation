mkdir -p /home/khuyen.pham/MonoDepthEstimation/results/EndoFASt3r/summary

/home/khuyen.pham/miniconda3/envs/endodac/bin/python /home/khuyen.pham/MonoDepthEstimation/scripts/EndoFASt3r/analyze_fold_metrics.py \
  --metrics_dir /home/khuyen.pham/MonoDepthEstimation/results/EndoFASt3r/folds \
  --out_dir /home/khuyen.pham/MonoDepthEstimation/results/EndoFASt3r/summary \
  --out_prefix EndoFASt3r