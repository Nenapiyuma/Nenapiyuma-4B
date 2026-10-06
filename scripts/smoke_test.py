#!/usr/bin/env python3
from pathlib import Path
import ast,sys
ROOT=Path(__file__).resolve().parents[1]
required=["README.md","MODEL_CARD.md","requirements.txt","configs/qlora.yaml","scripts/check_size.py",
"scripts/train_qlora.py","scripts/merge_lora.py","scripts/convert_and_select_gguf.sh","scripts/offline_infer.py",
"android/nenapiyuma-android/settings.gradle.kts","windows/Nenapiyuma.Windows/Nenapiyuma.Windows.csproj"]
missing=[p for p in required if not (ROOT/p).exists()]
if missing: print("MISSING:",*missing,sep="\n"); sys.exit(1)
for p in ROOT.glob("scripts/*.py"): ast.parse(p.read_text())
print("PASS: structure and Python syntax")
print("NOTE: real model execution needs local weights/toolchains.")
