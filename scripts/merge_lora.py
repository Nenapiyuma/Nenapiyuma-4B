#!/usr/bin/env python3
import argparse
from pathlib import Path
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--base",required=True); ap.add_argument("--adapter",required=True); ap.add_argument("--out",required=True)
    a=ap.parse_args()
    if not Path(a.base).exists() or not Path(a.adapter).exists():
        raise SystemExit("ERROR: local base/adapter path missing")
    try:
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from peft import PeftModel
    except Exception as e:
        raise SystemExit(f"ERROR: merge dependencies unavailable: {e}")
    base=AutoModelForCausalLM.from_pretrained(a.base,local_files_only=True,trust_remote_code=True)
    model=PeftModel.from_pretrained(base,a.adapter,local_files_only=True)
    model.merge_and_unload().save_pretrained(a.out,safe_serialization=True)
    AutoTokenizer.from_pretrained(a.base,local_files_only=True,trust_remote_code=True).save_pretrained(a.out)
    print("MERGE_OK",a.out)
if __name__=="__main__": main()
