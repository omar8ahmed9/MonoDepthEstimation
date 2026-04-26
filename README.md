# MonoDepthEstimation

Benchmarking endoscopic monocular depth estimation models on the SCARED dataset under a unified evaluation protocol.

## Purpose
This repository defines the shared benchmarking setup used by the team:
- official data split
- official dataset structure
- benchmark protocol
- shared result organization
- fixed SCARED dataset location for evaluation

## Key Files
- Benchmark protocol: `docs/benchmark_protocol.md`
- Dataset structure: `docs/dataset_structure.md`
- Dataset notes: `data/README.md`
- Main split files: `data/splits/train_files.txt`, `data/splits/val_files.txt`, `data/splits/test_files.txt`
- Test-fold split files: `data/splits/test_folds/test_fold1.txt` through `data/splits/test_folds/test_fold5.txt`
- Model analysis scripts: `scripts/<model_name>/`

## Dataset

Use the fixed prepared SCARED dataset:

`/l/users/omar.mohamed/datasets/SCARED_prepared_fixed`

Do not use `/scared_prepare` for new evaluations.

## Splits

The benchmark uses the split files stored in `data/splits/`.

Official counts:
- train: 12913
- val: 1705
- test: 551

Five-fold test counts:
- fold1: 2177
- fold2: 2014
- fold3: 2274
- fold4: 2223
- fold5: 2271

## Notes
The benchmark follows the available SCARED split protocol rather than using all available prepared frames.

For the five-fold evaluation, use the repo-local files under `data/splits/test_folds/`. These are the splits used by the `pcdepth` and `MonoPCC` results and keep the sample counts consistent across models.

## Results
Store outputs in:

`results/<model_name>/`

Current SCARED fixed-dataset result folders:
- `results/EndoDac`
- `results/EndoMUST`
- `results/EndoFASt3r`
- `results/pcdepth`
- `results/MonoPCC`

Each model result folder should follow the compact `results/pcdepth` layout:

- `folds/*_metrics.txt`
- `summary/*_fold_summary.csv`, `*_fold_stats.csv`, `*_fold_ranking.csv`, `*_fold_report.txt`
- `per-sample-main/test_per_sample.csv`
- `per-sample-main/selected/`
- `frozen_visualizations/{best,median,worst}/`
- `visualizations/test_main_abs_rel/{best,median,worst}/`

Do not commit intermediate or oversized artifacts such as prediction NPZ files, duplicate fold metrics CSV files, raw exported depth maps, temporary qualitative panel folders, `my_metrics.csv`, or generated `__pycache__` files.

## Analysis Scripts

For each evaluated model, use the scripts under `scripts/<model_name>/` in this order:

1. `analyze_fold_metrics.sh`
2. `analyze_per_sample_split.sh`
3. `select_qualitative_samples.sh`
4. `make_qualitative_panels.sh`
5. `render_frozen_qualitative_samples.sh`

The frozen qualitative rendering uses the shared input file:

`results/common/common_qualitative_samples.csv`
