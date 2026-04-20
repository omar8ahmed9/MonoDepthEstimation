# Data

Do not upload datasets to this repository.

## Main dataset
The main benchmark dataset is **SCARED**.

Raw dataset used during setup:

`/l/users/omar.mohamed/datasets/SCARED`

Prepared benchmark dataset used for training and evaluation:

`/l/users/omar.mohamed/datasets/SCARED_prepared`

## How each team member should use it
Each team member can either:
- copy the raw dataset into their own directory under `/l/`, then prepare it using the shared script, or
- directly work from an already prepared benchmark dataset if available

Recommended local naming:

- raw dataset: `SCARED`
- prepared dataset: `SCARED_prepared`

Example:

- `/l/users/<username>/datasets/SCARED`
- `/l/users/<username>/datasets/SCARED_prepared`

## Official benchmark split
The official benchmark split is stored in:

`data/splits/endovis/`

Files:
- `train_files.txt`
- `val_files.txt`
- `test_files.txt`

Official counts:
- train: 12913
- val: 1705
- test: 551

## Preprocessing
The raw SCARED dataset needs preprocessing to match the official benchmark structure.

Use the shared script:

`scripts/prepare_scared.py`

This script converts the raw dataset into the prepared benchmark dataset structure.

The final prepared structure is defined in:

`docs/dataset_structure.md`

## Important
All team members must:
- keep the same prepared dataset structure
- use the shared split files in this repository
- avoid creating model-specific benchmark splits