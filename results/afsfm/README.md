# AF-SfMLearner Results (Endoscopic Depth Estimation)

This folder contains the evaluation results of **AF-SfMLearner** on the **SCARED dataset**, following the same protocol used for other models (e.g., DARES, MonoPCC, PC-Depth).

---

## 📊 Evaluation Setup

- Dataset: SCARED (prepared split)
- Evaluation mode: Monocular (median scaling)
- Metrics:
  - Abs Rel
  - Sq Rel
  - RMSE
  - RMSE log
  - δ < 1.25 (a1)
  - δ < 1.25² (a2)
  - δ < 1.25³ (a3)

---

## 📁 Folder Structure

- `metrics.csv` → Main test performance  
- `folds/` → 5-fold evaluation results  
- `summary/` → Aggregated fold statistics and rankings  
- `per-sample-main/` → Per-sample error analysis  
- `visualizations/` → Best / median / worst predictions  
- `frozen_visualizations/` → Fixed qualitative comparisons  

---

## 📈 Key Results (Main Test)

| Metric   | Value |
|----------|------|
| Abs Rel  | 0.148 |
| Sq Rel   | 2.753 |
| RMSE     | 11.57 |
| RMSE log | 0.184 |
| a1       | 0.787 |
| a2       | 0.948 |
| a3       | 0.991 |

---

## 🔁 Robustness (5-Fold Evaluation)

- Mean Abs Rel ≈ 0.147  
- Best Fold: Fold 2  
- Worst Fold: Fold 4  

This indicates moderate sensitivity to data distribution.

---

## 🧠 Notes

- Evaluation uses the same folds as other models for fair comparison.
- Some folds show higher error due to challenging scenes and occlusions.
- AF-SfMLearner underperforms compared to domain-specific models (e.g., DARES), as expected.

---

## ✅ Status

✔ Main evaluation  
✔ 5-fold validation  
✔ Per-sample analysis  
✔ Qualitative visualization  

Ready for comparison and reporting.
