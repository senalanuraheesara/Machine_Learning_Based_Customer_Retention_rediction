# Retail customer inactivity project

## Submission reading order

1. [Submission report](docs/submission_report.md) â€” consolidated account of the project and findings.
2. [Decision log](docs/decision_log.md) â€” decisions, alternatives, reasons and evidence.
3. [Model/method comparison](docs/model_method_comparison.md) â€” final scores, parameters, tradeoffs and evaluation.
4. [Documentation index](docs/README.md) â€” preprocessing, features, fitting, segmentation and review details.

**Final selection: Random Forest**, threshold **0.425**, validation accuracy **68.63%**, test accuracy **67.12%**. These are reused-holdout results. Segmentation remains exploratory: the final fixed-window K-means solution groups 1,696 customers into clusters of 1,577 and 119. See [population definitions](docs/customer_populations.md).

## Notebook order

1. `notebooks/01_data_understanding.ipynb`
2. `notebooks/02_preprocessing.ipynb`
3. `notebooks/03_01_logistic_regression.ipynb`
4. `notebooks/03_02_decision_tree.ipynb`
5. `notebooks/03_03_random_forest.ipynb`
6. `notebooks/03_04_gradient_boosting.ipynb`
7. `notebooks/03_05_model_comparison_selection.ipynb`
8. `notebooks/FINAL_Four_Optimized_Models.ipynb`
9. `notebooks/04_segmentation.ipynb`

The active input is `data/processed/customer_snapshot_features.csv`. Use the four bundles and CSV/JSON records in [outputs/final_four](outputs/final_four/README.md). Individual model notebooks load saved pipelines by default; `RETRAIN=True` refits frozen settings without publishing replacements or repeating search. The final notebook verifies saved models rather than training them.

## Reproducible tuning and CV

Each model notebook now contains historical tuning evidence, saved three-fold CV results and optional `RECOMPUTE_CV` and `RUN_TUNING` controls. See [training and tuning instructions](docs/reproducibility.md). Run `python src/tuning_workflow.py --model all --mode tune --n-iter 32` to produce separate candidates without replacing published models.

## Execution

From the project root, with a working Python environment containing the project dependencies:

```powershell
python src/run_notebooks.py
python src/run_notebooks.py 04_segmentation.ipynb
```

The first command runs comparison and final verification only. Pass other notebook names explicitly to run them. The supplied `.venv` launcher currently references an unavailable interpreter path and failed during the documentation review; recreate a compatible environment before relying on that launcher. `requirements-lock.txt` records the original dependencies, and `requirements.txt` is the broader dependency list. The earlier documentation audit did not install packages or retrain models. The segmentation cleanup created a working local .segmentation-venv from requirements.txt and executed the final segmentation notebook; classifier models were not retrained.

Preprocessing changes can invalidate saved model fingerprints. Revalidate or retrain models before using changed data. EDA/preprocessing now write their generated notes under `outputs/generated_docs/`, so rerunning them will not overwrite the curated submission documents.

## Clean package contents

| Folder | Contents |
| --- | --- |
| `notebooks/` | Nine active notebooks with saved results |
| `docs/` | Submission report, decision log, method comparison and supporting documentation |
| `data/` | Raw dataset and outputs from the active preprocessing/segmentation notebooks |
| `outputs/final_four/` | Exactly four final models and their selection/comparison records |
| `outputs/segmentation/` and `outputs/figures/` | Final segmentation tables and supporting figures |
| `outputs/evidence/` | Audit/search provenance, historical source and verification/cleanup records |
| `src/` | Runtime helpers, notebook runner and verification script |

Superseded model bundles/notebooks, stale classifier tables/plots, one-off builders, log files and duplicate review exports have been removed. Historical source under `outputs/evidence/source/` is retained for explanation only, not as runnable reconstruction scripts.

The local `.venv` is retained as an installed dependency cache but excluded from the submission ZIP. The ZIP also excludes bytecode caches and itself. Create a compatible Python environment from the requirements files on the receiving machine; the supplied local launcher is not portable.

No supplied rubric was found. The documentation includes the requested decision logs and model/method comparison; additional institution-specific requirements still need checking.

## Build the submission ZIP

Run `python src/package_submission.py` from the project root. It creates and verifies `submission.zip`, excluding local environments, Python bytecode caches and other ZIP files. The final segmentation workflow uses dependencies from `requirements.txt`; no notebook installation cells are needed. See [population definitions](docs/customer_populations.md) for the classification/segmentation count differences.
