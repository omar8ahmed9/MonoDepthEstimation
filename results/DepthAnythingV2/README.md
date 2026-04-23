# DepthAnythingV2

Depth Anything V2 evaluation results on the SCARED / Endovis test split.

## Notes
- Used pretrained Depth Anything V2 large model (`vitl`).
- Inference was run on the SCARED endovis test split.
- Raw depth predictions were saved from a modified inference script before visualization normalization.
- Test images were prepared from the official `test_files.txt` split.
- Ground-truth depth was taken from the prepared SCARED MonoPCC-format folders and cropped to the top half to match the prediction resolution.
- Median scaling was applied before metric computation, for consistency with monocular evaluation.
- Environment used:
  - Python 3.10
  - torch 2.5.1+cu121
  - torchvision 0.20.1+cu121
- Evaluation completed successfully on GPU.
