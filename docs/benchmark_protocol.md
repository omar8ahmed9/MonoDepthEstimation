# Benchmark Protocol

## Official Split
Use the shared benchmark split located at:

`data/splits/endovis/`

Files:
- `train_files.txt`
- `val_files.txt`
- `test_files.txt`

Official counts:
- train: 12913
- val: 1705
- test: 551

All team members must use the same split files for benchmarking.

## Split Verification Note
The benchmark follows the available SCARED split protocol rather than using all available prepared frames.

During verification, the training split was filtered against actual raw/prepared SCARED file availability because some entries referenced by the original split were not present in the released raw depth/pose archives.

Validation and test splits were kept unchanged.

Therefore:
- `train_files.txt` is the validated official training split
- `val_files.txt` is the official validation split
- `test_files.txt` is the official test split

## Main Metrics
The main benchmark should report:
- Abs Rel
- Sq Rel
- RMSE
- RMSE log
- delta < 1.25

Optional secondary metrics may be reported separately, but they should not replace the main comparison table.

## Evaluation Rules
All models must be evaluated under the same benchmark setting.

Rules:
- use the same shared split files
- do not redefine the train/val/test split per model
- clearly document any model-specific preprocessing or postprocessing
- if scale alignment or median scaling is used, it must be stated explicitly and applied consistently

The final benchmark table should clearly state whether results are:
- raw predictions
- median-scaled predictions
- scale-aligned predictions

## Dataset Convention
All team members must follow the official dataset structure defined in:

`docs/dataset_structure.md`

If a model requires a different internal input layout, the model owner should create a model-specific adapter without changing the benchmark dataset definition.

## Results Format
Store outputs in:

`results/<model_name>/`

Recommended contents:
- `metrics.txt`
- `notes.txt`
- `predictions/`

## Practical Principle
This repository defines the benchmark.

Model repositories may differ internally, but they must adapt to this benchmark rather than changing:
- the official split
- the official dataset structure
- the benchmark indexing convention