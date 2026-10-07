---
title: Nenapiyuma 4B Online Chat
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 8080
pinned: false
---

# Nenapiyuma 4B — Hugging Face Space

This Space runs the real GGUF through llama.cpp and exposes an OpenAI-compatible API.

The default model is the verified Phi-3.5-mini-instruct Q2_K bootstrap model, not the final fine-tuned Nenapiyuma checkpoint.

The model is downloaded by the Space server, not by visitors.

## Variables

Set these in Space Settings → Variables:

- MODEL_URL — GGUF download URL
- CTX_SIZE — default 4096
- THREADS — default 4
- PARALLEL — default 1

API endpoint:
https://YOUR-SPACE-NAME.hf.space/v1/chat/completions

Health:
https://YOUR-SPACE-NAME.hf.space/health

The GitHub demo can use the API endpoint directly.

The server enables CORS for the GitHub Pages chat UI.

A 4B GGUF needs substantial RAM/CPU. Free/shared hosting can be slow or may not have enough memory.
