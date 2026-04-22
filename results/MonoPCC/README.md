# MonoPCC

MonoPCC evaluation results on the SCARED / Endovis test split.

## Notes
- Used pretrained MonoPCC weights from the official MonoPCC repo link.
- Evaluation was run on SCARED endovis test split.
- Ground-truth depths were prepared using AF-SfMLearner `export_gt_depth.py`.
- Data was arranged into the folder structure expected by MonoPCC:
  - `datasetX/keyframeY/image_02/data/`
  - `datasetX/keyframeY/image_02/data/groundtruth/`
- Environment used:
  - Python 3.7
  - torch 1.9.0+cu111
  - torchvision 0.10.0+cu111
- Evaluation completed successfully on GPU.
