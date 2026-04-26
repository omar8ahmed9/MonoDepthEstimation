mkdir -p /home/hamdan.alhadhrami/MonoDepthEstimation/results/DepthAnythingV2/summary

python /home/hamdan.alhadhrami/MonoDepthEstimation/scripts/depthanythingv2/analyze_fold_metrics.py \
  --metrics_dir /home/hamdan.alhadhrami/MonoDepthEstimation/results/DepthAnythingV2/folds \
  --out_dir /home/hamdan.alhadhrami/MonoDepthEstimation/results/DepthAnythingV2/summary \
  --out_prefix depthanythingv2
