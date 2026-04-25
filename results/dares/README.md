# DARES

## Overview
This folder contains the evaluation results of the **DARES** model on the **SCARED (EndoVis) dataset** using the standardized evaluation pipeline adopted in this project.

The evaluation includes:
- Main test split performance
- 5-fold cross-validation for robustness analysis
- Per-sample error analysis
- Qualitative visualization results

---

## Dataset
All experiments were conducted using the corrected dataset:

/l/users/omar.mohamed/datasets/SCARED_prepared_fixed

---

## Evaluation Setup

- Evaluation type: Monocular depth estimation
- Scaling: Median scaling
- Resolution: 320 × 256
- Metrics:
  - abs_rel, sq_rel, rmse, rmse_log, a1, a2, a3

---

## Main Test Result

| Model | Dataset | Split | abs_rel | sq_rel | rmse | rmse_log | a1 | a2 | a3 | scaling |
|------|--------|------|--------|--------|------|----------|----|----|----|--------|
| DARES | SCARED | endovis test | 0.052 | 0.356 | 4.479 | 0.073 | 0.980 | 0.998 | 1.000 | median |

---

## Cross-Validation (5-Fold)

| Fold | abs_rel | rmse | a1 |
|------|--------|------|----|
| Fold 1 | 0.064 | 4.753 | 0.964 |
| Fold 2 | 0.030 | 2.413 | 0.995 |
| Fold 3 | 0.046 | 3.752 | 0.994 |
| Fold 4 | 0.062 | 7.045 | 0.954 |
| Fold 5 | 0.080 | 6.404 | 0.933 |

---

## Notes
- Invalid GT samples were removed before fold evaluation
- Median scaling was used
- Same pipeline as other models

