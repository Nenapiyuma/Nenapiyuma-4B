# Nenapiyuma 4B — Separate Demo Chat

This folder is a separate public-facing demo system for people who download Nenapiyuma 4B.

## Purpose
- Let visitors try a few Sinhala, English, coding and maths prompts.
- Keep the downloadable model separate from the demo website.
- Never fake model responses.
- Do not expose API keys in the browser.

## How it will work
1. The real Nenapiyuma 4B GGUF is trained, converted, size-checked and released.
2. A demo server loads that real model.
3. The demo page sends HTTPS OpenAI-compatible chat requests to that server.
4. Visitors can test the model before downloading it.

## Important
GitHub Pages only hosts the web UI. It does not run a 4B model by itself.

The final public demo therefore needs a real HTTPS inference server (with CORS enabled) or a browser-compatible model build. Until that exists, this page intentionally shows that the demo server is not configured instead of generating fake AI answers.

Do not put private API keys in `demo/index.html`.
