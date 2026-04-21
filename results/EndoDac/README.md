
# Evaluation protocol

For all reported SCARED benchmark numbers in this workspace, we use the EndoVis split resolved by `endoDAC/evaluate_depth.py` with `--eval_split endovis`.

The split files are taken from:

`data/splits/endovis/`

Files:
- `train_files.txt`: 12913 samples
- `val_files.txt`: 1705 samples
- `test_files.txt`: 551 samples

Reporting rule:
- training uses `train_files.txt`
- model selection can use `val_files.txt`
- final benchmark numbers should be reported on `test_files.txt`

The evaluator computes and logs:
- `abs_rel`
- `sq_rel`
- `rmse`
- `rmse_log`
- `a1`, `a2`, `a3` corresponding to threshold accuracy at `delta < 1.25`, `delta < 1.25^2`, and `delta < 1.25^3`

Default evaluation command:

```bash
conda run -n endodac python endoDAC/evaluate_depth.py \
  --data_path /l/users/<username>/datasets/SCARED_prepared \
  --load_weights_folder ./endoDAC/full_model \
  --eval_split endovis \
  --eval_mono
```

By default, metrics are appended to:

`<load_weights_folder>/eval_metrics.csv`