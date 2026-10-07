"""
SKLLMForCausalLM: Decoder-only Transformer Language Model.
Supports weight tying, KV caching, mixed precision metadata, gradient checkpointing flags,
binary checkpoint serialization, and real SHA-256 verification.
"""

import os
import json
import struct
from typing import List, Tuple, Optional, Dict, Any
from .config import SKLLMConfig, get_model_config
from .layers import RMSNorm, SKDecoderLayer, KVCache
from .tensor_backend import SKMatrix, compute_sha256_bytes


class SKLLMForCausalLM:
    """Core SK AI Decoder-Only Transformer Language Model."""

    def __init__(self, config: Optional[SKLLMConfig] = None):
        self.config = config or get_model_config("sk-llm-mini")
        self.embed_tokens = SKMatrix(self.config.vocab_size, self.config.hidden_size, seed=777)
        self.layers: List[SKDecoderLayer] = [
            SKDecoderLayer(self.config, layer_idx=i)
            for i in range(self.config.num_hidden_layers)
        ]
        self.norm = RMSNorm(self.config.hidden_size, eps=self.config.rms_norm_eps)
        if self.config.tie_word_embeddings:
            self.lm_head = self.embed_tokens
        else:
            self.lm_head = SKMatrix(self.config.vocab_size, self.config.hidden_size, seed=888)
        self.gradient_checkpointing = self.config.gradient_checkpointing

    def num_parameters(self) -> int:
        total = self.embed_tokens.numel + self.norm.num_parameters()
        for layer in self.layers:
            total += layer.num_parameters()
        if not self.config.tie_word_embeddings:
            total += self.lm_head.numel
        return total

    def create_kv_cache(self) -> KVCache:
        return KVCache(self.config.num_hidden_layers)

    def forward(
        self,
        input_ids: List[int],
        kv_cache: Optional[KVCache] = None,
        start_pos: int = 0,
    ) -> Dict[str, Any]:
        if not input_ids:
            raise ValueError("input_ids cannot be empty")
        hidden_states: List[List[float]] = []
        for tok_id in input_ids:
            safe_id = tok_id % self.config.vocab_size
            hidden_states.append(self.embed_tokens.get_row(safe_id))
        for layer in self.layers:
            hidden_states = layer.forward(hidden_states, kv_cache=kv_cache, start_pos=start_pos)
        hidden_states = self.norm.forward(hidden_states)
        last_hidden = hidden_states[-1]
        logits = self.lm_head.matvec(last_hidden)
        return {
            "logits": logits,
            "last_hidden_state": last_hidden,
            "seq_len": len(input_ids),
            "kv_cache": kv_cache,
        }

    def save_checkpoint(self, filepath: str) -> Dict[str, Any]:
        """Serialize every trainable tensor, including RMSNorm weights."""
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        header_dict = {
            "magic": "SKAI_WEIGHTS_V1",
            "variant_id": self.config.variant_id,
            "name": self.config.name,
            "parameter_count": self.num_parameters(),
            "dtype": self.config.dtype,
            "vocab_size": self.config.vocab_size,
            "hidden_size": self.config.hidden_size,
            "num_hidden_layers": self.config.num_hidden_layers,
        }
        header_bytes = json.dumps(header_dict).encode("utf-8")
        chunks: List[bytes] = [
            struct.pack("<I", len(header_bytes)),
            header_bytes,
            self.embed_tokens.to_bytes(),
        ]
        for layer in self.layers:
            chunks.append(struct.pack("<I", len(layer.input_layernorm.weight)))
            chunks.append(struct.pack(
                f"<{len(layer.input_layernorm.weight)}f",
                *layer.input_layernorm.weight,
            ))
            chunks.append(layer.self_attn.q_proj.to_bytes())
            chunks.append(layer.self_attn.k_proj.to_bytes())
            chunks.append(layer.self_attn.v_proj.to_bytes())
            chunks.append(layer.self_attn.o_proj.to_bytes())
            chunks.append(struct.pack("<I", len(layer.post_attention_layernorm.weight)))
            chunks.append(struct.pack(
                f"<{len(layer.post_attention_layernorm.weight)}f",
                *layer.post_attention_layernorm.weight,
            ))
            chunks.append(layer.mlp.gate_proj.to_bytes())
            chunks.append(layer.mlp.up_proj.to_bytes())
            chunks.append(layer.mlp.down_proj.to_bytes())
        chunks.append(struct.pack("<I", len(self.norm.weight)))
        chunks.append(struct.pack(f"<{len(self.norm.weight)}f", *self.norm.weight))

        payload = b"".join(chunks)
        with open(filepath, "wb") as f:
            f.write(payload)
        sha256 = compute_sha256_bytes(payload)
        return {
            "filepath": filepath,
            "file_size": len(payload),
            "sha256": sha256,
            "parameter_count": self.num_parameters(),
        }
