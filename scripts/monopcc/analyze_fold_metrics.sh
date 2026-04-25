mkdir -p /home/hamdan.alhadhrami/MonoDepthEstimation/results/MonoPCC/summary

python /home/hamdan.alhadhrami/MonoDepthEstimation/scripts/monopcc/analyze_fold_metrics.py \
  --metrics_dir /home/hamdan.alhadhrami/MonoDepthEstimation/results/MonoPCC/folds \
  --out_dir /home/hamdan.alhadhrami/MonoDepthEstimation/results/MonoPCC/summary \
  --out_prefix monopcc
