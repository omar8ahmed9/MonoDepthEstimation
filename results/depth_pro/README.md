# Depth Pro Results (Endoscopic Depth Estimation)

This folder contains the evaluation results of **Depth Pro** on the **SCARED dataset**, following the same evaluation protocol used for other models where applicable.

---

## 📊 Evaluation Setup

- Model: Depth Pro (pretrained)
- Dataset: SCARED (prepared, fixed version)
- Evaluation mode: Monocular (with median scaling)
- Input: Left RGB images
- Resolution: Native (resized internally by model)

### Metrics

The following standard depth estimation metrics are reported:

- Absolute Relative Error (Abs Rel)
- Squared Relative Error (Sq Rel)
- Root Mean Squared Error (RMSE)
- RMSE (log)
- Accuracy under threshold:
  - δ < 1.25 (a1)
  - δ < 1.25² (a2)
  - δ < 1.25³ (a3)

---

## 📁 Folder Structure

- `metrics.csv` → Main test set performance  
- `metrics.txt` → Raw output log (optional, for reference)  

---

## 📈 Main Test Results

| Model      | Dataset | Split         | abs_rel | sq_rel | rmse  | rmse_log | a1     | a2     | a3     | scaling |
|------------|--------|---------------|--------|--------|-------|----------|--------|--------|--------|---------|
| Depth Pro  | SCARED | endovis test  | 0.0699 | 0.6519 | 6.026 | 0.0964   | 0.9528 | 0.9945 | 0.9988 | median  |

---

## ⚠️ Notes on Evaluation

- Median scaling was applied to ensure fair comparison with other monocular depth estimation models.
- Ground truth depth for Depth Pro evaluation was derived from the **scene_points** data by extracting the Z-axis and applying absolute value transformation.
- Invalid values (NaN, zero, or out-of-range depths) were filtered using a validity mask.

---

## ❗ Cross-Validation (Folds)

Cross-validation across the 5 folds was **not performed for Depth Pro**.

This is due to differences in ground truth handling:
- Depth Pro requires per-frame depth reconstruction from 3D scene geometry (`scene_points`)
- Other models use precomputed ground truth depth maps (`gt_depths.npz`)
- This leads to inconsistencies when directly applying the same fold evaluation pipeline

---

## 🧠 Discussion

- Depth Pro performs strongly on the SCARED dataset after applying median scaling.
- The model achieves high accuracy (a1 > 0.95), indicating good alignment with ground truth structure.
- However, compared to domain-specific models (e.g., DARES), Depth Pro:
  - is significantly slower
  - requires additional preprocessing for ground truth
  - is less straightforward to integrate into standardized evaluation pipelines

---

## ✅ Status

✔ Main test evaluation completed  
✔ Results standardized and formatted  
✔ Ready for comparison and reporting  
