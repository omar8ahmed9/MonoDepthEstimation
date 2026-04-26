# Depth Pro Results (SCARED Dataset)

This folder contains the complete evaluation results for Depth Pro on the SCARED dataset, following the standardized evaluation pipeline used across all models in this project.

## Evaluation Setup

- Model: Depth Pro (pretrained)
- Dataset: SCARED (fixed version)
  /l/users/omar.mohamed/datasets/SCARED_prepared_fixed
- Evaluation Mode: Monocular with median scaling
- Input: Left RGB images

Ground Truth:
- Main test: Provided depth maps
- Folds: Derived from scene_points (Z-axis, absolute value)

## Metrics

- Abs Rel
- Sq Rel
- RMSE
- RMSE log
- a1 (δ < 1.25)
- a2 (δ < 1.25²)
- a3 (δ < 1.25³)

## Folder Structure

results/depth_pro/
├── metrics.csv
├── folds/
│   ├── test_main_metrics.txt
│   ├── test_fold1_metrics.txt
│   ├── test_fold2_metrics.txt
│   ├── test_fold3_metrics.txt
│   ├── test_fold4_metrics.txt
│   ├── test_fold5_metrics.txt
│   └── test_main_pred.npz
├── summary/
├── per-sample-main/
├── visualizations/
└── frozen_visualizations/

## Main Test Results

Abs Rel   : 0.0699  
Sq Rel    : 0.6519  
RMSE      : 6.026  
RMSE log  : 0.0964  
a1        : 0.9528  
a2        : 0.9945  
a3        : 0.9988  

## Cross-Validation (5 Folds)

Mean Abs Rel ≈ 3.42  
Performance varies significantly across folds  
Lower consistency compared to main test split  

## Status

✔ Main test completed  
✔ 5-fold evaluation completed  
✔ Analysis pipeline completed  
✔ Visualizations generated  
✔ Ready for report
