# Model evidence

`optimization/` preserves original search tables, eligibility checks, fitting audits and protocol/selection records supporting the final model choices. These describe the historical candidate pool. Current scores and final selection are in [final_four](../final_four/README.md).

`source/` contains historical audit, optimization and packaging implementations for review only. Their original directory assumptions and input model collections no longer exist; they are not executable entry points for this clean package. Use the active notebooks for saved-model verification or fixed-setting refitting.

`documentation_verification.json` records fresh checks of the four final models against the reported scores. `cleanup_manifest.json` records exactly which files were removed.

`cross_validation/` contains newly computed final-settings three-fold diagnostics, loaded by default in the model notebooks. The supported training/tuning entry point is `src/tuning_workflow.py`; see [reproducibility](../../docs/reproducibility.md).
