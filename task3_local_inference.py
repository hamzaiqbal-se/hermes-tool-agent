#!/usr/bin/env python3
"""Task 3 — minimal local open-weight inference via Ollama.
Verified: Ollama 0.40.1; model qwen2.5:3b (1.9 GB); response LOCAL_MODEL_OK.
Cloud endpoint: not tested (openrouter free tier exists but not configured/verified).
No paid APIs; no secrets exposed.
Usage: set OLLAMA_HOST=http://localhost:11434 or use full binary path if not in PATH."""
import subprocess, time, sys, os
OLLAMA_BIN = os.getenv("OLLAMA_BIN", "C:/Users/hamza/AppData/Local/Programs/Ollama/ollama.exe")
MODEL = "qwen2.5:3b"
start = time.time()
r = subprocess.run([
    OLLAMA_BIN, "run", MODEL,
    "Return exactly LOCAL_MODEL_OK and nothing else."
], capture_output=True, text=True)
elapsed = time.time() - start
print("exit:", r.returncode)
print("time_s:", round(elapsed, 2))
print("output_snippet:", (r.stdout or r.stderr)[:200].strip())
