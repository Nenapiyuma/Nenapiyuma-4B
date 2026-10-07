FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV MODEL_URL=https://github.com/Nenapiyuma/Nenapiyuma-4B/releases/download/v0.1.0-bootstrap/Phi-3.5-mini-instruct-Q2_K.gguf

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake git curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN git clone --depth 1 https://github.com/ggml-org/llama.cpp.git /app/llama.cpp \
    && cmake -S /app/llama.cpp -B /app/llama.cpp/build -DGGML_NATIVE=OFF \
    && cmake --build /app/llama.cpp/build --config Release -j2 --target llama-server

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

VOLUME ["/models"]
EXPOSE 8080

ENTRYPOINT ["/entrypoint.sh"]
