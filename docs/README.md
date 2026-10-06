# Nenapiyuma 4B Web Chat

This is the GitHub Pages chat interface for Nenapiyuma 4B.

## Important
GitHub Pages is a static website; it cannot itself run a 4B-parameter model. The page therefore connects to an OpenAI-compatible local model server (for example llama.cpp) at:

http://127.0.0.1:8080/v1/chat/completions

Once the real Nenapiyuma GGUF is trained, verified, and released, the local server can load that GGUF and this UI can be used as the chat front-end.

No fake model, benchmark, file size, or response is claimed.
