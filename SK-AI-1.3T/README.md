# SK AI 1.3T Engineering Track

This branch is the audit/engineering track for the uploaded SK AI project.

## Current verified status

The uploaded implementation does not currently contain a verified 1.3 trillion parameter model. Exact runtime-derived preset counts are:

- Mini: 1,311,872
- Small: 1,213,302,784
- Medium: 6,195,253,248
- Large: 56,863,236,096

The 1.3T target is therefore treated as a new architecture requirement, not as an existing model claim.

## 1 TB target

For 1,300,000,000,000 parameters:

- FP32 = 5.20 TB
- BF16/FP16 = 2.60 TB
- INT8 = 1.30 TB
- INT4 theoretical = 650 GB

The ~1 TB target is feasible only with real low-bit storage and measured quantization overhead. Padding/duplicate/placeholder tensors are prohibited.

## This branch

- AUDIT_1_3T.md — initial engineering audit
- configs/sk_1_3t_target.json — target storage/training specification
- tests/test_1_3t_accounting.py — exact accounting tests
- model/llm.py — checkpoint serialization patch for RMSNorm weights

Large model weights/checkpoints are intentionally not committed to Git history.

## Next production phase

The actual 1.3T implementation needs a production tensor backend, distributed tensor/pipeline/data parallelism, sharded optimizer state, checkpoint resume/load, tokenizer integration, quantization with measured overhead, and real evaluation on Sinhala/English/code/math/reasoning.

No model-ready or training-success claim will be made until those tests run on the actual 1.3T artifact.
