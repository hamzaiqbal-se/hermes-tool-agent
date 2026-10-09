# Collaborative Workflow — Task 2 (Sequential Researcher → Writer)

## What this is
A sequential two-role workflow using separate Hermes Desktop turns (not concurrent subagents). The Researcher analyzes `sample-data/`; the Writer reads `research_notes.md` and produces `final_report.md`. This demonstrates collaboration via file handoff and persistent memory, not successful `delegate_task` delegation.

## Verified limitation (documented, not fixed)
- `delegate_task` (delegation ID `deleg_2c084f95`) started but failed with `HTTP 401: User not found` (OpenRouter) even with `credentials_cfg={"provider":"nous"}`.
- Manifest recorded `provider: null`, `model: null`; subagent did not select `nous`.
- Source (`delegate_tool_config.py` L421-440) supports routing overrides, but inheritance proved unreliable in this session/environment.
- No retry, auth change, or provider switch made.

## Turn 1 — Researcher
**Role:** Analyze safe directory.
**Instruction (copy into Hermes Desktop / execute_code / terminal):**
```
Inspect E:\hermes-tool-agent\sample-data. Report each file's name, extension, and size in bytes.
Write findings to E:\hermes-tool-agent\research_notes.md.
Save a project fact using the memory tool (add, target="memory").
Do not modify sample-data/ or source/test files.
```
**Verification steps:**
- Confirm `research_notes.md` exists and lists 3 files with correct sizes.
- Confirm memory entry exists (`MEMORY.md` contains the largest-file fact).
- Confirm `delegate_task` was not used (or report failure if attempted).

## Turn 2 — Writer (later session/turn)
**Role:** Produce report from verified findings.
**Instruction (copy into Hermes Desktop):**
```
Read E:\hermes-tool-agent\research_notes.md. Produce E:\hermes-tool-agent\final_report.md
based only on those findings. Identify the largest file clearly.
Do not invent data. Reference research_notes.md as source.
```
**Verification steps:**
- Confirm `final_report.md` exists.
- Confirm it references `data.json` (37 bytes) and does not invent other facts.
- Confirm `sample-data/` unmodified.

## Memory retrieval (verified mechanism)
- Memory tool actions: `add`, `replace`, `remove`. No `list`/`search`.
- Retrieval mechanism: frozen snapshot injected into session system prompt at session start + direct `MEMORY.md` file inspection.
- Cross-session retrieval requires a new session; not fully proven in this session (details saved to `MEMORY.md` at `C:\Users\hamza\AppData\Local\hermes\memories\MEMORY.md`).

## Supported alternatives instead of delegation
- Sequential turns with file handoff (this workflow).
- Same session using `terminal`/`execute_code` to run `file_analysis_agent.py`.
- Memory save via `memory` tool for persistence across turns.

## Explicit distinction
This is a **sequential two-role workflow**, not successful delegated subagent collaboration. It demonstrates Researcher → Writer handoff using files and memory. Concurrent multi-agent requires working `delegate_task`, which is blocked by an unauthenticated OpenRouter fallback in this installed version.

## References
- `HERMES_VS_LANGCHAIN.md`
- `README.md`
- `file_analysis_agent.py`
- `test_file_analysis.py`
- `research_notes.md`
- `final_report.md`
- `MEMORY.md` (memory persistence)
