#!/usr/bin/env bash
set -euo pipefail
: "$LLAMA_CPP_DIR"
MERGED_DIR=${MERGED_DIR:-artifacts/nenapiyuma-4b-merged}
OUT_DIR=${OUT_DIR:-models}
LIMIT=1500000000
mkdir -p "$OUT_DIR"
CONVERTER="$LLAMA_CPP_DIR/convert_hf_to_gguf.py"
QUANT="$LLAMA_CPP_DIR/build/bin/llama-quantize"
[ -f "$CONVERTER" ] || { echo "ERROR: missing $CONVERTER"; exit 2; }
[ -x "$QUANT" ] || { echo "ERROR: missing $QUANT"; exit 2; }
python "$CONVERTER" "$MERGED_DIR" --outfile "$OUT_DIR/Nenapiyuma-4B-F16.gguf" --outtype f16
declare -A Q
Q[Q2_K]=q2_k; Q[Q3_K_M]=q3_k_m; Q[Q4_K_M]=q4_k_m; Q[Q5_K_M]=q5_k_m
best=""; best_bytes=0
printf "quantization,bytes,sha256,status\n" > "$OUT_DIR/quantization_results.csv"
for label in Q2_K Q3_K_M Q4_K_M Q5_K_M; do
  out="$OUT_DIR/Nenapiyuma-4B-$label.gguf"
  "$QUANT" "$OUT_DIR/Nenapiyuma-4B-F16.gguf" "$out" "${Q[$label]}"
  bytes=$(stat -c '%s' "$out")
  sha=$(sha256sum "$out" | awk '{print $1}')
  status=FAIL
  [ "$bytes" -lt "$LIMIT" ] && status=PASS
  printf "%s,%s,%s,%s\n" "$label" "$bytes" "$sha" "$status" | tee -a "$OUT_DIR/quantization_results.csv"
  if [ "$bytes" -lt "$LIMIT" ] && [ "$bytes" -gt "$best_bytes" ]; then best="$out"; best_bytes="$bytes"; fi
done
[ -n "$best" ] || { echo "ERROR: no tested quantization is below 1500 MB"; exit 1; }
cp "$best" "$OUT_DIR/Nenapiyuma-4B.gguf"
python scripts/check_size.py "$OUT_DIR/Nenapiyuma-4B.gguf"
echo "SELECTED=$best"
