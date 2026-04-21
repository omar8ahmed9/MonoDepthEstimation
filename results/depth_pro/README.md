# Evaluation protocol

Apple Depth Pro was evaluated on SCARED using the official benchmark split from:

`data/splits/endovis/test_files.txt`

Final benchmark numbers are reported on the 551 samples in the official test split.

## Adapter / preprocessing details

- Input RGB images were read from the prepared SCARED layout:
  `SCARED_prepared/{train|test}/datasetX/keyframeY/data/left/<frame_id>.png`
- Split entries of the form `datasetX/keyframeY frame_id l` were mapped to the corresponding prepared image path.
- Ground truth depth was loaded from:
  `EndoMUST/splits/endovis/gt_depths.npz`
- Before reuse, the `EndoMUST` test split was verified to exactly match the official benchmark test split.
- Predicted depth maps were resized to the ground-truth resolution before metric computation.
- Predictions were clipped to `[1e-3, 150.0]`.

## Reporting setting

- raw predictions
- no median scaling
- no scale alignment
