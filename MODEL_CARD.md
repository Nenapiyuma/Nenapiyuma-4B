# Nenapiyuma 4B Model Card

Nenapiyuma 4B is intended to be a Sinhala-first + English compact language model for local/offline conversation, Q&A, maths, coding and mixed Sinhala-English use.

## Base
- Microsoft Phi-3.5-mini-instruct
- 3.8B parameters
- MIT license
- https://huggingface.co/microsoft/Phi-3.5-mini-instruct

## Adaptation
LoRA/QLoRA supervised fine-tuning is used. Training data must be legally usable and documented.

## Quantization release gate
Q2_K, Q3_K_M, Q4_K_M and Q5_K_M are tested. The final GGUF must have measured size strictly below 1,500,000,000 bytes.

## Honesty policy
No benchmark, file size, SHA-256, training success or final-model claim is valid until produced by the repository tools on real files.

## Limitations
Sinhala quality depends on adaptation data. Quantization can reduce quality. Android speed depends on device CPU/RAM.
