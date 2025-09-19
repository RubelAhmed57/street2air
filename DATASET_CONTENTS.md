# Dataset contents and hosting recommendations

This file documents which files should be kept in the GitHub repository and which should be hosted externally (e.g., Zenodo, Figshare, or Git LFS).

Keep in repository (small files, examples)
- Small example images per class (a few dozen images)
- Example `multiview scripts/` used to demonstrate data preparation and usage
- Metadata files: `CITATION.cff`, `DATASET_CONTENTS.md`, `README.md`
- Small sample 3D preview images (PNG)

Host externally (large files)
- Large archives: `ground_truth_3d.zip`, `synthesized top views.zip` — put these on Zenodo or GitHub releases and link to them from the README.
- Full `trellis artifacts/` 3D models (`*.glb`) if large — use Git LFS or an external archive.

Suggested workflow
1. Add the small example files to the repo and commit.
2. Upload large archives to Zenodo (create a DOI) or attach to a GitHub release.
3. Update `README.md` with download links and DOI.

Privacy & ethical notes
- Ensure no personally-identifying information (PII) is included in images or metadata.
- If necessary, redact or remove sensitive images before sharing.
