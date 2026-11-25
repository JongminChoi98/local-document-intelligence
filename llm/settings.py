from dataclasses import dataclass
import json
from urllib.request import Request, urlopen


OLLAMA_URL = "http://127.0.0.1:11434"
DEFAULT_MODEL = "qwen3.5:4b-q4_K_M"


@dataclass(frozen=True)
class GenerationSettings:
    model: str = DEFAULT_MODEL
    think: bool | None = False
    num_ctx: int = 16384
    temperature: float = 0.1
    num_predict: int = 1024


def list_generation_models() -> dict:
    with urlopen(
        f"{OLLAMA_URL}/api/tags",
        timeout=10,
    ) as response:
        models = json.load(response)["models"]

    available = {}

    for model in models:
        name = model["name"]

        if (
            name.endswith(("-cloud", ":cloud"))
            or model.get("remote_model")
            or model.get("remote_host")
        ):
            continue

        request = Request(
            f"{OLLAMA_URL}/api/show",
            data=json.dumps({
                "model": name,
            }).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(request, timeout=10) as response:
            details = json.load(response)

        capabilities = details.get("capabilities", [])

        if "completion" in capabilities:
            available[name] = capabilities

    return dict(sorted(available.items()))
