# Training, tuning and cross-validation

The four individual model notebooks now show the retained historical search distributions, chosen historical trial, highest search CV score, three fold scores, final parameters and the eligible variant comparison. They also show fresh, saved CV diagnostics of the **actual final model settings**. Existing final bundles remain unchanged.

## Environment and inputs

The tested setup uses Windows and Python 3.14.3 with scikit-learn 1.9.1. From a freshly extracted submission folder, with Python 3.14 installed:

```powershell
py -3.14 -m venv .repro-venv
.repro-venv/Scripts/python.exe -m pip install -r requirements-lock.txt
.repro-venv/Scripts/python.exe src/verify_environment.py
.repro-venv/Scripts/python.exe src/run_notebooks.py 04_segmentation.ipynb
.repro-venv/Scripts/python.exe src/verify_segmentation.py
```

The supplied local `.venv` launcher is not portable; create your own environment. Required inputs are included: `data/processed/customer_snapshot_features.csv` and `outputs/final_four/<model>.joblib`. `src/accuracy_experiments.py` must remain importable because saved pipelines reference its transformer class. To regenerate snapshots from raw data, execute `02_preprocessing.ipynb`; changed fingerprints require review before reusing model evidence.

## Three distinct operations

| Operation | Notebook control | What happens |
| --- | --- | --- |
| View evidence (default) | All switches False | Load saved final model, historical tuning table and final-settings CV CSV. No tuning or training. |
| Recompute final-settings CV | `RECOMPUTE_CV=True` | Clone and refit the final pipeline in three customer-disjoint training folds. Save fold scores/provenance. Published fitted model stays unchanged. |
| Refit final settings | `RETRAIN=True` | Refit a clone on the whole training partition; use the frozen threshold. Does not search or publish a replacement. |
| Rerun tuning | `RUN_TUNING=True` | Search the explicit rerun grid on training folds, refit the eligible candidate on training data, select threshold using validation and save a separate candidate. |

Equivalent commands, using your environment's Python:

```powershell
python src/tuning_workflow.py --model all --mode cv
python src/tuning_workflow.py --model logistic_regression --mode tune --n-iter 32
python src/tuning_workflow.py --model decision_tree --mode tune --n-iter 32
python src/tuning_workflow.py --model random_forest --mode tune --n-iter 32
python src/tuning_workflow.py --model gradient_boosting --mode tune --n-iter 32
```

`--model all --mode tune` runs all four. The number of trials is capped by the number of configurations (Logistic Regression has ten in the rerun grid). Folds use StratifiedGroupKFold with three splits, shuffle=True and seed 42; search sampling uses seed 73. Pipeline cloning removes learned state, so imputation/scaling/encoding are fitted inside each training fold. No test score is calculated by this tuning command.

CV diagnostics are saved in `outputs/evidence/cross_validation/`, with data fingerprints, model hashes and software versions. Rerun artifacts go to `outputs/reproduction/<model>/`: all search results, run metadata, and, when a CV candidate passes selection, a training-fitted candidate and validation threshold table. Rejection is explicit; no unsafe fallback is selected. The run metadata also reports the temporal-gap eligibility screen. This candidate is not automatically promoted: repeated-CV and threshold-matched audits and independent future-period evaluation remain necessary before promotion. Never interpret a saved candidate file alone as deployment approval.

## Historical evidence versus rerun evidence

The retained `updated_optimized_*_search.csv` tables are later experiments, not necessarily the original search that produced each final incumbent. Their original parameter distributions and selected-trial fold results are displayed separately. The original incumbent per-trial CSVs were not retained during cleanup; no missing historical scores are invented. Final default-threshold CV means were independently reproduced from the included pipelines and snapshots.

The new rerun grid includes the final estimator's values and nearby alternatives while fixing its final feature/preprocessing design. It can therefore be rerun from the clean package but is **not** a bit-for-bit replay of the full historical multi-stage search. Historical scripts under `outputs/evidence/source/` remain read-only provenance; the supported entry point is `src/tuning_workflow.py`.

## Interpretation and verification

Final-settings CV was freshly computed once for this revision, then loaded when the four notebooks were executed. At 0.50 the means reproduce the published values: Logistic Regression 69.18%, Decision Tree 68.22%, Random Forest 69.59% and Gradient Boosting 69.54%. The new seed-42 operating-threshold scores differ from the older seed-137 audit and are labelled separately.

The complete documented randomized rerun finished for all four models: 10 Logistic Regression configurations and 32 each for Decision Tree, Random Forest and Gradient Boosting (106 configurations, 318 CV fits). Candidate refits and validation threshold selection completed for all four. This is not an exhaustive grid search or an exact replay of the historical multi-stage optimization. Published model hashes remain unchanged. See `outputs/evidence/full_tuning_verification.json` and `outputs/reproduction/` for trial-level results and candidate metadata. Earlier two-trial checks remain historical evidence in `outputs/evidence/tuning_workflow_checks.json`.

Grouped CV within training does not replace independent temporal validation. Search scores reuse the folds used to select settings, and validation/test were inspected repeatedly during development. Customer identities can recur across temporal partitions; grouping applies inside CV only. A fresh future period is needed for independent performance confirmation.

## Verified rerun and environment (11 October 2026)

A fresh Windows virtual environment was created using Python 3.14.3 and installed directly from requirements-lock.txt. The submission ZIP was extracted into an isolated project folder. In that extracted copy, pip check, stored scikit-learn version checks, all 12 published model/split accuracy checks, fingerprints, selection, the segmentation notebook and its export checks passed. All four saved bundles contain scikit-learn 1.9.1 estimator states; requirements.txt now pins that version as well.

This tests a clean virtual environment and relocated package on the same Windows computer. It does not claim testing on a separate physical computer, Linux/macOS, or Python 3.12. Installation requires access to the package index. The local environments and extracted test copy are excluded from the submission ZIP.

| Rerun candidate | Configurations | Selected CV accuracy | Validation accuracy | Threshold |
| --- | ---: | ---: | ---: | ---: |
| Logistic Regression | 10 | 69.18% | 68.29% | 0.425 |
| Decision Tree | 32 | 68.22% | 66.10% | 0.425 |
| Random Forest | 32 | 69.64% | 67.88% | 0.400 |
| Gradient Boosting | 32 | 69.54% | 68.01% | 0.400 |

These rerun candidates are separate from the published models and were not promoted. The published Random Forest remains selected with validation accuracy 68.63% at threshold 0.425. The tuning run used the earlier fresh requirements.txt environment (NumPy 2.5.4); the separate lock-file verification used NumPy 2.5.3. Both used scikit-learn 1.9.1 and pandas 3.0.6.

Run `python src/verify_tuning_rerun.py` to check completed search artifacts and unchanged published model hashes. Environment evidence is saved in outputs/evidence/environment_verification.json and outputs/evidence/clean_setup_verification.json. The distinction between observed fixed-window activity and classifier purchasing retention is explained in [population definitions](customer_populations.md).
