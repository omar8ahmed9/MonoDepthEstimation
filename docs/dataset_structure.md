# Dataset Structure

This benchmark uses a shared prepared SCARED dataset structure.

## Dataset Roots

During setup, the following naming was used:

- raw dataset root: `/l/users/omar.mohamed/datasets/SCARED`
- prepared dataset root: `/l/users/omar.mohamed/datasets/SCARED_prepared`

For reproducibility, team members are encouraged to use the same naming convention in their own `/l/users/<username>/datasets/` directory.

In this document:
- `SCARED` refers to the raw dataset
- `SCARED_prepared` refers to the prepared benchmark dataset used directly for training and evaluation

## Official Prepared Dataset Root

`<DATA_ROOT>` below refers to the prepared dataset root, for example:

`/l/users/<username>/datasets/SCARED_prepared`

The prepared dataset root must follow this structure:

```text
<DATA_ROOT>/
├── train/
│   └── dataset1/
│       └── keyframe1/
│           └── data/
│               ├── left/
│               ├── right/
│               ├── scene_points/
│               └── frame_data/
└── test/
    └── dataset8/
        └── keyframe1/
            └── data/
                ├── left/
                ├── right/
                ├── scene_points/
                └── frame_data/