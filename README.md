# Nenapiyuma 4B

Sinhala-first + English local/offline LLM project based on Microsoft Phi-3.5-mini-instruct (3.8B parameters, MIT).

## Honest release gate

A file is called the real Nenapiyuma-4B model only after real local weights are trained/merged, GGUF Q2/Q3/Q4/Q5 files are actually generated, exact byte sizes are measured, the selected file is strictly below 1,500,000,000 bytes, SHA-256 is computed, and offline smoke tests pass. This repository never fabricates weights, benchmarks, sizes or hashes.

## Files

- configs/qlora.yaml — QLoRA settings
- data/README.md — dataset format
- scripts/train_qlora.py — local-only QLoRA
- scripts/merge_lora.py — local-only LoRA merge
- scripts/convert_and_select_gguf.sh — real Q2/Q3/Q4/Q5 conversion and selection
- scripts/check_size.py — hard <1,500,000,000-byte gate
- scripts/offline_infer.py — local GGUF inference
- scripts/smoke_test.py — repository syntax/structure checks
- android/nenapiyuma-android — Kotlin/Compose deployment shell
- windows/Nenapiyuma.Windows — .NET offline runner
- MODEL_CARD.md — provenance and limitations

## Training

Supply a local copy of the base model and legal training data. Automatic downloads are disabled.

```bash
python -m venv .venv
pip install -r requirements.txt
python scripts/train_qlora.py --config configs/qlora.yaml
```

QLoRA requires a CUDA-capable environment with compatible bitsandbytes. If CUDA or weights are missing, the script exits without claiming training happened.

## GGUF

Install/build llama.cpp locally and set `LLAMA_CPP_DIR`. No automatic downloads occur.

```bash
export LLAMA_CPP_DIR=/path/to/llama.cpp
bash scripts/convert_and_select_gguf.sh
```

The script generates Q2_K, Q3_K_M, Q4_K_M and Q5_K_M, records real bytes/SHA-256, and chooses the highest tested quantization below the hard limit.

## Offline inference

```bash
python scripts/offline_infer.py --model models/Nenapiyuma-4B.gguf --prompt "ආයුබෝවන්"
```

No cloud API or network model download is used.

## Android / Windows

Android: open `android/nenapiyuma-android` in Android Studio and provide a locally built/bundled llama.cpp native backend. This environment currently has no Android SDK/Gradle toolchain, so no APK build is claimed.

Windows: build `windows/Nenapiyuma.Windows` with .NET 8 and a local `llama-cli.exe`. This environment currently has no .NET SDK, so no EXE build is claimed.

See MODEL_CARD.md for model provenance and limitations.


## CI
GitHub Actions validates Python syntax and the repository's automated tests on every push to `main` and pull request.
