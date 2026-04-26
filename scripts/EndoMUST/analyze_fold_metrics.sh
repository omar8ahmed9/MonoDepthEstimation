mkdir -p /home/khuyen.pham/MonoDepthEstimation/results/EndoMUST/summary

/home/khuyen.pham/miniconda3/envs/endodac/bin/python /home/khuyen.pham/MonoDepthEstimation/scripts/EndoMUST/analyze_fold_metrics.py \
  --metrics_dir /home/khuyen.pham/MonoDepthEstimation/results/EndoMUST/folds \
  --out_dir /home/khuyen.pham/MonoDepthEstimation/results/EndoMUST/summary \
  --out_prefix EndoMUST