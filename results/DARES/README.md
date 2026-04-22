# Evaluation protocol

For all reported SCARED benchmark numbers in this workspace, we use the EndoVis split resolved by `DARES/evaluate_depth.py` with evaluation on the `endovis` split.

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
conda run -n dares python DARES/evaluate_depth.py \
  --data_path /l/users/saif.alkindi/datasets/SCARED_DARES \
  --load_weights_folder /l/users/saif.alkindi/projects/ai7102_project/DARES/pretrained/best_weights \
  --eval_mono \
  --num_workers 0
