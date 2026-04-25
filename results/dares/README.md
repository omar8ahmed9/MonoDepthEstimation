# DARES Results

DARES was evaluated on the fixed SCARED / EndoVis test split using mono evaluation with median scaling.

## Dataset

Fixed dataset path used:

`/l/users/omar.mohamed/datasets/SCARED_prepared_fixed`

## Main Result

| Model | Dataset | Split | abs_rel | sq_rel | rmse | rmse_log | a1 | a2 | a3 | scaling |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| DARES | SCARED | endovis test | 0.052 | 0.356 | 4.479 | 0.073 | 0.980 | 0.998 | 1.000 | median |

## Notes

The model was also evaluated across all five test folds. Invalid ground-truth samples with no valid pixels were skipped during fold evaluation, following the team decision.
