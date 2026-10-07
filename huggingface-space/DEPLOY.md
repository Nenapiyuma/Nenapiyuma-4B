# Hugging Face Docker Space deployment

1. Create a new Docker Space on Hugging Face.
2. Upload the contents of this folder into the Space repository root.
3. The Space must expose port 8080.
4. Set MODEL_URL in Space Settings → Variables.
5. Rebuild/start the Space.
6. Test /health.
7. Use https://YOUR-SPACE-NAME.hf.space/v1/chat/completions as the GitHub demo endpoint.

Current verified bootstrap model:
https://github.com/Nenapiyuma/Nenapiyuma-4B/releases/download/v0.1.0-bootstrap/Phi-3.5-mini-instruct-Q2_K.gguf

SHA-256:
2e6564bea11e9447560fd9a83acac1b248293c2466ffee97683d3bf2288ce8e9

Size:
1,416,204,288 bytes (< 1,500,000,000 bytes)

This is a real downloadable bootstrap GGUF, not a fine-tuned final Nenapiyuma checkpoint.
