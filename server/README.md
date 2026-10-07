# Nenapiyuma 4B Online Inference Server

This folder provides a real HTTPS-ready server setup for the GitHub demo.

## What it does

- Runs a real GGUF model with llama.cpp.
- Exposes an OpenAI-compatible `/v1/chat/completions` endpoint.
- Enables CORS so the GitHub Pages chat UI can call it.
- Downloads the model **on the server**, not to each visitor's phone/browser.
- Keeps the offline download option unchanged.

## Important model status

The included default model is the verified **Phi-3.5-mini-instruct Q2_K bootstrap GGUF**, not a fine-tuned final Nenapiyuma checkpoint.

Default model size: 1,416,204,288 bytes (< 1,500,000,000 bytes).

Model URL:
https://github.com/Nenapiyuma/Nenapiyuma-4B/releases/download/v0.1.0-bootstrap/Phi-3.5-mini-instruct-Q2_K.gguf

When the final fine-tuned Nenapiyuma GGUF is published, set `MODEL_URL` to that release asset.

## Run

```bash
docker compose up --build
```

The local endpoint will be:

```
http://localhost:8080/v1/chat/completions
```

For public use, put this service behind an HTTPS domain. Then put that HTTPS endpoint into the GitHub demo's **Online model server** setting.

GitHub Pages is only the web UI; it is not a persistent GPU/CPU inference server.

## Production notes

A 4B model is resource-intensive. A small public server may be slow or run out of RAM. Use a host with enough RAM/CPU (or GPU) and HTTPS.

Do not put private API keys or cloud credentials in `demo/index.html`.

The server intentionally makes no fake responses: if the model cannot load or inference fails, the API returns an error.
