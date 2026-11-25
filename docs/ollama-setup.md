# Ollama Environment Setup

## 1. Development Environment

| Component | Specification |
|---|---|
| Host OS | Windows |
| Development OS | WSL2 Ubuntu 26.04 LTS |
| CPU | AMD Ryzen 9 8945HS |
| Host RAM | 32 GB |
| WSL RAM | 15 GiB |
| GPU | NVIDIA RTX 4060 Laptop |
| VRAM | 8 GB |
| Ollama Version | 0.40.17 |

## 2. Prerequisites

Verify GPU availability and systemd:

    nvidia-smi
    ps -p 1 -o comm=

Install required packages:

    sudo apt update
    sudo apt install -y curl zstd

The zstd package is required to extract the
Ollama installation archive.

## 3. Installation

Install Ollama using the official Linux installer:

    curl -fsSL https://ollama.com/install.sh | sh

Verify the installation:

    ollama --version
    systemctl status ollama --no-pager
    curl http://127.0.0.1:11434

## 4. Local-only Configuration

Configuration file:

    config/ollama/override.conf

Environment variables:

- OLLAMA_NO_CLOUD=1
- OLLAMA_HOST=127.0.0.1:11434
- OLLAMA_CONTEXT_LENGTH=8192

Apply the configuration from the repository root:

    sudo install -D -m 644 config/ollama/override.conf /etc/systemd/system/ollama.service.d/override.conf
    sudo systemctl daemon-reload
    sudo systemctl restart ollama

## 5. Verification

    systemctl is-active ollama
    systemctl cat ollama --no-pager
    systemctl show ollama --property=Environment --no-pager
    journalctl -u ollama -n 50 --no-pager | grep -i cloud
    ss -ltnp | grep 11434
    curl http://127.0.0.1:11434

Expected results:

- Service status: active
- Cloud disabled: true
- Listening address: 127.0.0.1:11434
- API response: Ollama is running

## 6. Troubleshooting

### Missing zstd

If the installer fails because zstd is missing:

    sudo apt install -y zstd

Run the official installer again.

## 7. Security Notes

- Ollama cloud features are disabled.
- The API is bound to the loopback interface.
- Model downloads may require internet access.
- Model weights and confidential documents must not
  be committed to the repository.
- GPU inference must be verified separately.

## 8. References

- https://docs.ollama.com/linux
- https://docs.ollama.com/faq
