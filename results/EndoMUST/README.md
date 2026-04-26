# EndoMUST Results

Evaluation dataset:

`/l/users/omar.mohamed/datasets/SCARED_prepared_fixed`

Do not use `/scared_prepare` for these results.

Splits:
- Main test split: `data/splits/test_files.txt`
- Five test folds: `data/splits/test_folds/test_fold1.txt` through `test_fold5.txt`

Expected fold totals:
- test_main: 551
- test_fold1: 2177
- test_fold2: 2014
- test_fold3: 2274
- test_fold4: 2223
- test_fold5: 2271

This folder follows the compact `results/pcdepth` layout:
- `folds/*_metrics.txt`
- `summary/*`
- `per-sample-main/*`
- `frozen_visualizations/{best,median,worst}/`
- `visualizations/test_main_abs_rel/{best,median,worst}/`

Intermediate files are intentionally excluded: `*_metrics.csv`, `test_main_pred.npz`, `exported_depth_maps/`, `qualitative_panels/`, `my_metrics.csv`, and `__pycache__/`.

Analysis scripts are under `scripts/EndoMUST/`.
