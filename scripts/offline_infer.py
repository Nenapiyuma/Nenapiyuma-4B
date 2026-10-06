#!/usr/bin/env python3
import argparse
from pathlib import Path
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--model",required=True); ap.add_argument("--prompt"); a=ap.parse_args()
    if not Path(a.model).is_file() or a.model.startswith(("http://","https://")):
        raise SystemExit("ERROR: use a local GGUF file only")
    try:
        from llama_cpp import Llama
    except Exception as e:
        raise SystemExit(f"ERROR: llama-cpp-python unavailable: {e}")
    llm=Llama(model_path=a.model,n_ctx=4096,verbose=False)
    prompt=a.prompt or input("You: ")
    r=llm.create_chat_completion(messages=[{"role":"user","content":prompt}],max_tokens=256,temperature=0.7)
    print(r["choices"][0]["message"]["content"])
if __name__=="__main__": main()
