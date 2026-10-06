#!/usr/bin/env python3
import argparse
from pathlib import Path
import yaml

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    a = ap.parse_args()
    c = yaml.safe_load(Path(a.config).read_text())
    base, data = Path(c["base_model_path"]), Path(c["dataset_path"])
    if not base.exists():
        raise SystemExit(f"ERROR: local base model not found: {base}. Automatic downloads are disabled.")
    if not data.exists():
        raise SystemExit(f"ERROR: training data not found: {data}")
    try:
        import torch
        from datasets import load_dataset
        from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
        from peft import LoraConfig
        from trl import SFTTrainer, SFTConfig
    except Exception as e:
        raise SystemExit(f"ERROR: training dependencies unavailable: {e}")
    if not torch.cuda.is_available():
        raise SystemExit("ERROR: CUDA GPU unavailable. QLoRA was not run.")
    tok = AutoTokenizer.from_pretrained(str(base), local_files_only=True, trust_remote_code=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    q = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16, bnb_4bit_use_double_quant=True)
    model = AutoModelForCausalLM.from_pretrained(str(base), quantization_config=q,
        device_map="auto", local_files_only=True, trust_remote_code=True)
    ds = load_dataset("json", data_files=str(data), split="train")
    def fmt(x):
        return tok.apply_chat_template(x["messages"], tokenize=False, add_generation_prompt=False)
    ds = ds.map(lambda x: {"text": fmt(x)})
    lora = LoraConfig(r=c["lora_r"], lora_alpha=c["lora_alpha"], lora_dropout=c["lora_dropout"],
        target_modules=c["target_modules"], bias="none", task_type="CAUSAL_LM")
    args = SFTConfig(output_dir=c["output_dir"], max_seq_length=c["max_seq_length"],
        num_train_epochs=c["num_train_epochs"], per_device_train_batch_size=c["per_device_train_batch_size"],
        gradient_accumulation_steps=c["gradient_accumulation_steps"], learning_rate=c["learning_rate"],
        logging_steps=c["logging_steps"], save_steps=c["save_steps"], warmup_ratio=c["warmup_ratio"],
        seed=c["seed"], report_to="none", dataset_text_field="text", packing=True)
    trainer = SFTTrainer(model=model, tokenizer=tok, train_dataset=ds, peft_config=lora, args=args)
    trainer.train()
    trainer.save_model(c["output_dir"])
    tok.save_pretrained(c["output_dir"])
    print("TRAINING_OK", c["output_dir"])

if __name__ == "__main__":
    main()
