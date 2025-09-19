Street2Air Dataset and Code

Street2Air: A Framework for Synthesizing Aerial Vehicle Views from Ground Images

Authors: Md Rubel Ahmed, Fazle Rahat, M Shifat Hossain, Sumit Kumar Jha, Rickard Ewetz

Abstract
--------
Annotated aerial view images are often missing from fine-grained vehicle type classification datasets. This lack of data limits both the accuracy and robustness of models when applied to top-down views, which are essential for applications such as autonomous drones and aerial surveillance. Models trained only on street-level images often fail to generalize to aerial perspectives, requiring more time and multiple observations to recognize vehicles accurately. In contrast, models trained with both street-level and aerial views can perform more reliably and with faster inference in drone-based systems. However, collecting real aerial data at scale can be costly and logistically challenging. In this regard, we want to leverage the recent advances in 3D generation which have made it feasible to synthesize diverse 3D assets.

In this repository we share a curated subset of the Street2Air data and the scripts used to generate/prepare examples for sharing. The full dataset (large archives and 3D assets) is available on request or via the project release (see `DATASET_CONTENTS.md` for hosting recommendations).

Included in this repo
- `README.md` — this file
- `CITATION.cff` — citation metadata for this dataset
- `LICENSE` — project license (MIT)
- `.gitignore` — recommended ignores for the repo
- `DATASET_CONTENTS.md` — what to include in the repo vs external hosting
- `scripts/prepare_dataset.py` — tiny helper to inspect and prepare example data
- `multiview scripts/`, `street views/`, `top views/`, `trellis artifacts/` — example project folders (may be present locally)

Quick start
-----------
1. Inspect the dataset structure locally (or after cloning):

```bash
ls -la
python3 scripts/prepare_dataset.py --list
```

2. To use the small example images included in this repo, copy them to your training folder and follow your normal training pipeline. For reproducible experiments with the full dataset, see `DATASET_CONTENTS.md` for hosting and download instructions.

Citing this dataset
--------------------
If you use Street2Air in a paper or project, please cite our paper (accepted to the 24th International Conference on Machine Learning and Applications) and the dataset. A `CITATION.cff` is included for convenience. Example BibTeX:

```bibtex
@inproceedings{ahmed2025street2air,
  title={Street2Air: A Framework for Synthesizing Aerial Vehicle Views from Ground Images},
  author={Ahmed, Md Rubel and Rahat, Fazle and Hossain, M Shifat and Jha, Sumit Kumar and Ewetz, Rickard},
  booktitle={Proceedings of the 24th International Conference on Machine Learning and Applications},
  year={2025}
}
```

License
-------
This repository and dataset are released under the Creative Commons Attribution 4.0 International License (CC BY 4.0). See `LICENSE`.

Contact
-------
For questions about dataset access, usage, or to request the full archives, please contact the authors (see `CITATION.cff`).
