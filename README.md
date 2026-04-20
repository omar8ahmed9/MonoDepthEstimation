# MonoDepthEstimation

Benchmarking endoscopic monocular depth estimation models on the SCARED dataset under a unified evaluation protocol.

## Purpose
This repository defines the shared benchmarking setup used by the team:
- official data split
- official dataset structure
- benchmark protocol
- shared result organization
- shared dataset preparation script

## Key Files
- Benchmark protocol: `docs/benchmark_protocol.md`
- Dataset structure: `docs/dataset_structure.md`
- Dataset notes: `data/README.md`
- Official split files: `data/splits/endovis/`
- Shared preparation script: `scripts/prepare_scared.py`

## Official Split
The benchmark uses the split files stored in:

`data/splits/endovis/`

Official counts:
- train: 12913
- val: 1705
- test: 551

## Notes
The benchmark follows the available SCARED split protocol rather than using all available prepared frames.

During verification, the training split was filtered against actual raw/prepared SCARED file availability because some entries referenced by the original split were not present in the released depth/pose archives.

Validation and test splits were kept unchanged.

## Results
Store outputs in:

`results/<model_name>/`
