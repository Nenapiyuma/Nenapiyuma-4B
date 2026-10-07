# SK AI 1.3T — Initial Engineering Audit

Date: 2026-10-07

## Scope
This report is based on direct inspection and execution of the uploaded `sk-ai (1).zip`. No 1.3T claim is accepted without independently deriving the parameter count from the implementation.

## Verified current architecture

| Variant | Layers | Hidden | FFN | Attention heads | KV heads | Context | Exact counted parameters |
|---|---:|---:|---:|---:|---:|---:|---:|
| Mini | 4 | 128 | 384 | 4 | 2 | 4,096 | 1,311,872 |
| Small | 24 | 2,048 | 5,632 | 16 | 4 | 8,192 | 1,213,302,784 |
| Medium | 32 | 4,096 | 11,008 | 32 | 8 | 32,768 | 6,195,253,248 |
| Large | 64 | 8,192 | 28,672 | 64 | 8 | 131,072 | 56,863,236,096 |

The uploaded code therefore **does not currently implement a 1,300,000,000,000-parameter model**.

The current SK-LLM core is a dense decoder-only Transformer using RMSNorm, RoPE, SwiGLU and GQA. No MoE implementation was found in the inspected SK-LLM core.

## 1.3T storage math

For exactly 1,300,000,000,000 parameters:

- FP32: 5,200,000,000,000 bytes = 5.20 TB
- BF16/FP16: 2,600,000,000,000 bytes = 2.60 TB
- INT8: 1,300,000,000,000 bytes = 1.30 TB
- INT4 theoretical: 650,000,000,000 bytes = 650 GB

Thus a ~1 TB artifact is compatible with 1.3T parameters only through real low-bit storage such as INT4 plus scales/metadata/container overhead. FP16/BF16 cannot meet 1 TB.

## Critical checkpoint bug

The original checkpoint serializer counted RMSNorm weights but did not serialize them. The working tree patches `save_checkpoint()` so trainable RMSNorm weights are included. A production loader and versioned tensor manifest are still required before release.

## Training

Rough dense training estimate:

`FLOPs ~= 6 * parameters * training_tokens`

- 1T tokens: 7.8e24 FLOPs
- 10T tokens: 7.8e25 FLOPs
- 26T tokens: 2.028e26 FLOPs

A rough BF16 + gradients + Adam-state estimate is ~12 bytes/parameter before activations/buffers: ~15.6 TB for 1.3T parameters. Production training therefore requires large distributed infrastructure with tensor, pipeline and data parallelism plus ZeRO-3/FSDP-style state sharding.

The uploaded test environment reports ~5.81 GB RAM and CPU-only execution, so it cannot train or instantiate a dense 1.3T model.

## Tests actually run

- pytest: 10 passed before the checkpoint patch
- pytest: 13 passed after the accounting/serialization patch
- smoke_test.py: PASS
- compileall: PASS
- Mini checkpoint after patch: 5,247,716 bytes, SHA-256 `7a8c78cbd5f8574e196dab949ed910755710a4994b9ca3a4c06656b4917911bd`

The Mini checkpoint result is **not** a 1.3T result.

## Release gates

The 1.3T model must not be marked ready until exact tensor-derived parameter count, real artifact size, quantization overhead, SHA-256, checkpoint load/restore, distributed inference, training resume and Sinhala/English/code/math/reasoning evaluations all pass on the actual model.

Large weights/checkpoints must not enter normal Git history.
