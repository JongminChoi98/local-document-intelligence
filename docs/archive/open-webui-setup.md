# Open WebUI Environment Setup

## 1. Environment

| Component | Version |
|---|---|
| Development OS | WSL2 Ubuntu 26.04 LTS |
| uv | 0.13.10 |
| Managed Python | 3.12.16 |
| System Python | 3.14.4 |
| Open WebUI | 0.13.4 |
| Ollama | 0.40.17 |
| LLM | qwen3.5:4b-q4_K_M |

## 2. Installation

Install uv:

    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"

Install the managed Python runtime:

    uv python install 3.12.16

Install Open WebUI in an isolated tool environment:

    uv tool install --python 3.12.16 "open-webui==0.13.4"

Verify installation:

    uv --version
    uv tool list
    uv python find 3.12.16

## 3. Configuration

Create the local environment file:

    cp --update=none config/open-webui/.env.example config/open-webui/.env

The environment template defines:

- Local Ollama API connection
- OpenAI API disabled
- Web search disabled
- Version update checks disabled
- User signup enabled
- Community sharing disabled

Persistent settings saved through the Admin UI may
override environment variables.

Verify and save the actual settings in the Admin UI.

## 4. Start and Stop

Start Open WebUI from the repository root:

    ./scripts/start-open-webui.sh

Access the application:

    http://localhost:8080

Press Ctrl+C in the server terminal to stop Open WebUI.

Ollama runs independently as a systemd service.

## 5. Data Storage

Application data is stored in:

    storage/open-webui/

This directory contains application databases,
user accounts, chat history, uploaded documents,
and other runtime data.

The storage directory and actual .env file
are excluded from Git.

## 6. Context Window

The initial Ollama context length of 4096 tokens
caused a context length error in Open WebUI.

The server default was increased to 8192 tokens
using the systemd override configuration.

| Metric | 4096 Context | 8192 Context |
|---|---:|---:|
| Observed VRAM Usage (MiB) | 3761 | 3992 |
| GPU Offloading | 100% | 100% |

These measurements were taken under different
inference conditions.

## 7. Validation

Verified:

- Windows browser access to Open WebUI
- Local administrator account
- Ollama API integration
- Korean response generation
- 8192-token GPU inference
- Existing account and chat history persistence
- Startup script execution
- OpenAI API disabled
- Web search disabled
- Git exclusion of runtime data

Configured:

- User signup enabled
- Community sharing disabled

Recheck saved administrator settings after restart.

## 8. Known Limitations

- Some model responses contain factual inaccuracies.
- Occasional incomplete responses were observed.
- The exact cause of incomplete responses is unconfirmed.
- Full offline operation has not been verified.
- Document retrieval and citation quality have not
  yet been evaluated.

Use synthetic documents for initial RAG testing.

## 9. References

- https://docs.openwebui.com/
- https://docs.openwebui.com/reference/env-configuration/
- https://docs.astral.sh/uv/
- https://docs.ollama.com/
