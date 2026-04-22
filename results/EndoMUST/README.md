# Evaluation protocol

This folder stores the tracked EndoMUST benchmark outputs for the shared SCARED setup used in this workspace.

Evaluation setup:

- Dataset root: `/l/users/omar.mohamed/datasets/SCARED_prepared`
- Split source: `data/splits/endovis/`
- Test split size: `551` samples
- Checkpoint: `endoMUST/checkpoints/ours/release/EndoMUST`
- Pretrained encoder weights: `endoMUST/pretrained_model/depth_anything_vitb14.pth`

Tracked files:

- `my_metrics.csv`: summary depth metrics for the official EndoMUST `Ours` checkpoint
- `exported_depth_maps/export_manifest.csv`: manifest for exported prediction artifacts

Heavy exported arrays and PNGs are intentionally not tracked here because they are ignored by the repo-level `.gitignore`, matching the existing `results/EndoDac/` convention.

Evaluation command:

```bash
CUDA_VISIBLE_DEVICES=0 /home/khuyen.pham/miniconda3/envs/endodac/bin/python endoMUST/evaluate_depth.py \
  --data_path /l/users/omar.mohamed/datasets/SCARED_prepared \
  --pretrained_path /home/khuyen.pham/MonoDepthEstimation/endoMUST/pretrained_model \
  --load_weights_folder /home/khuyen.pham/MonoDepthEstimation/endoMUST/checkpoints/ours/release/EndoMUST \
  --eval_mono \
  --eval_split endovis \
  --model_type endomust \
  --lora_type dvlora \
  --learn_intrinsics True \
  --num_workers 4 \
  --metrics_csv /home/khuyen.pham/MonoDepthEstimation/endoMUST/checkpoints/ours/ours_metrics.csv
```
