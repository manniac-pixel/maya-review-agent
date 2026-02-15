"""
Shared LLM client supporting Gemini (cloud) and Ollama (local) backends.
"""

import json
import logging
import os
import re
import time
import urllib.request
import urllib.error

import config

logger = logging.getLogger(__name__)

# ── Active backend state ────────────────────────────────────────────────
_backend = "gemini"  # or "ollama"
_gemini_configured = False


def set_backend(backend: str):
    """Set the active LLM backend: 'gemini' or 'ollama'."""
    global _backend
    if backend not in ("gemini", "ollama"):
        raise ValueError(f"Unknown backend: {backend}. Use 'gemini' or 'ollama'.")
    _backend = backend
    logger.info(f"LLM backend: {backend}")


def get_model():
    """Return a model handle for the active backend."""
    if _backend == "gemini":
        return _get_gemini_model()
    return _OllamaModel()


# ── Unified call ────────────────────────────────────────────────────────

def call(model, prompt: str) -> dict:
    """Call the active LLM and return parsed JSON."""
    if _backend == "gemini":
        return _call_gemini(model, prompt)
    return _call_ollama(model, prompt)


# ── Gemini implementation ───────────────────────────────────────────────

def _get_gemini_model():
    global _gemini_configured
    import google.generativeai as genai

    if not _gemini_configured:
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        _gemini_configured = True
    model_name = config.get("llm", "gemini_model", "gemini-2.0-flash")
    return genai.GenerativeModel(model_name)


def _call_gemini(model, prompt: str) -> dict:
    import google.generativeai as genai

    max_retries = config.get("llm", "max_retries", 4)
    base_delay = config.get("llm", "gemini_base_delay_seconds", 60)

    for attempt in range(1, max_retries + 1):
        try:
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    response_mime_type="application/json",
                    temperature=0.2,
                ),
            )
            return json.loads(response.text.strip())

        except Exception as e:
            error_str = str(e)

            if "429" in error_str or "quota" in error_str.lower():
                delay_match = re.search(r"retry in (\d+(?:\.\d+)?)s", error_str)
                wait = (
                    int(float(delay_match.group(1))) + 5
                    if delay_match
                    else base_delay * attempt
                )
                if attempt < max_retries:
                    logger.warning(
                        f"  Rate limited (attempt {attempt}/{max_retries}). "
                        f"Waiting {wait}s..."
                    )
                    time.sleep(wait)
                    continue

            if attempt == max_retries:
                raise

            logger.warning(f"  Attempt {attempt} failed: {e}. Retrying...")
            time.sleep(10)

    raise RuntimeError("Exhausted all retries")


# ── Ollama implementation ───────────────────────────────────────────────

class _OllamaModel:
    """Lightweight handle so the interface matches Gemini's model object."""
    pass


def _call_ollama(model, prompt: str) -> dict:
    """Call local Ollama server and parse JSON from its response."""
    # Wrap the user prompt with a strong JSON instruction
    system_msg = (
        "You are a JSON-only assistant. You MUST respond with valid JSON and "
        "nothing else. No markdown fences, no commentary, no explanation. "
        "Just the raw JSON object."
    )

    ollama_model = config.get("llm", "ollama_model", "llama3.1:8b")
    ollama_url = config.get("llm", "ollama_url", "http://localhost:11434")
    max_retries = config.get("llm", "max_retries", 4)

    payload = json.dumps({
        "model": ollama_model,
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.2, "num_ctx": 8192},
        "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt},
        ],
    }).encode()

    req = urllib.request.Request(
        f"{ollama_url}/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
    )

    for attempt in range(1, max_retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=300) as resp:
                body = json.loads(resp.read().decode())

            text = body["message"]["content"].strip()

            # Strip markdown fences if the model added them anyway
            if text.startswith("```"):
                text = text.split("\n", 1)[1]
                if text.endswith("```"):
                    text = text[: text.rfind("```")]
                text = text.strip()

            return json.loads(text)

        except urllib.error.URLError as e:
            if attempt == 1:
                logger.error(
                    f"Cannot connect to Ollama at {ollama_url}. "
                    "Make sure Ollama is running: ollama serve"
                )
            raise RuntimeError(
                f"Ollama connection failed: {e}. "
                "Start it with: ollama serve"
            ) from e

        except json.JSONDecodeError as e:
            if attempt < max_retries:
                logger.warning(
                    f"  Ollama returned invalid JSON (attempt {attempt}). Retrying..."
                )
                time.sleep(2)
                continue
            raise RuntimeError(
                f"Ollama returned invalid JSON after {max_retries} attempts: {e}"
            ) from e

        except Exception as e:
            if attempt == max_retries:
                raise
            logger.warning(f"  Attempt {attempt} failed: {e}. Retrying...")
            time.sleep(5)

    raise RuntimeError("Exhausted all retries")
