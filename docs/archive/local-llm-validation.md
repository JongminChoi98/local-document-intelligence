# Local LLM Validation

## 1. Validation Objective

Verify local model execution, Korean language generation,
GPU acceleration, and baseline inference performance
before introducing RAG components.

Validation date: 2026-11-25

## 2. Model Specification

| Component | Value |
|---|---|
| Runtime | Ollama 0.40.17 |
| Model | Qwen3.5 4B |
| Model Tag | qwen3.5:4b-q4_K_M |
| Model ID | d8b0f5e9760c |
| Architecture | qwen35 |
| Parameters | 4.2B |
| Quantization | Q4_K_M |
| Download Size | 3.3 GB |
| Maximum Model Context | 262144 tokens |
| Runtime Context | 4096 tokens |
| Thinking | Disabled for validation |
| Runner | llamacpp |
| License | Apache 2.0 |

## 3. Model Installation

    ollama pull qwen3.5:4b-q4_K_M
    ollama list
    ollama show qwen3.5:4b-q4_K_M

## 4. Inference

Interactive execution:

    ollama run qwen3.5:4b-q4_K_M --verbose --think=false

GPU verification:

    ollama ps
    nvidia-smi

## 5. Hardware Validation

| Metric | Result |
|---|---|
| GPU | NVIDIA RTX 4060 Laptop |
| Total VRAM | 8188 MiB |
| Idle VRAM | 0 MiB |
| Loaded VRAM | 3761 MiB |
| Available VRAM | 4427 MiB |
| GPU Offloading | 100% GPU |
| Loaded Model Size | 3.1 GB |

## 6. Inference Benchmark

| Test | Total (s) | Prefill (tokens/s) | Decode (tokens/s) |
|---|---:|---:|---:|
| Initial Inference | 33.57 | 1.70 | 41.46 |
| Warm Test 1 | 2.80 | 94.41 | 58.30 |
| Warm Test 2 | 3.19 | 368.20 | 57.50 |
| Warm Test 3 | 2.64 | 369.42 | 57.54 |

Warm inference baseline:

- Average response time: 2.88 seconds
- Average decode rate: 57.78 tokens/s
- GPU offloading: 100%

The initial inference showed significant prefill latency.
Subsequent requests did not reproduce the issue.
Initialization overhead is suspected but not confirmed.

The tests used different short Korean prompts and are
preliminary measurements, not a controlled benchmark.

## 7. Answer Quality

The model successfully generated Korean responses
covering the following topics:

- RAG architecture
- Embedding models
- Vector databases
- Fine-tuning

Some responses contained oversimplified or overstated
claims. Further factual validation is required.

Document-grounded accuracy and citation quality have
not yet been evaluated.

## 8. Validation Result

PASS: Model download
PASS: Local inference
PASS: Korean text generation
PASS: GPU acceleration
PASS: Warm inference performance

The current model and runtime configuration will be
retained for initial RAG development.

## 9. References

- https://ollama.com/library/qwen3.5
- https://docs.ollama.com/faq
- https://docs.ollama.com/api
