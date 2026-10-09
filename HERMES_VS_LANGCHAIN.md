# Hermes Agent vs. LangChain Agents

## 1. Architecture and Execution Loop

**Hermes Agent** ships with a built-in tool registry and execution loop. The `AIAgent` class (in `run_agent.py`) orchestrates provider selection, prompt construction, tool execution, retries, fallback, and persistence. Tools are registered centrally in `tools/registry.py` — over 70 tools across ~28 toolsets — and self-register at import time. The loop is synchronous and interruptible, with callbacks that surface every tool call to the user.

**LangChain Agents** use `create_agent`, which builds a harness around a model. The current API is backed by **LangGraph primitives**: the agent runs as a state graph where each step appends messages to `AgentState.messages`. Middleware hooks (`before_model`, `after_model`, etc.) let you intercept the loop at specific points. The model calls tools in a loop until the task is complete.

## 2. Tool Definition and Execution

**Hermes:** Tools are Python functions that self-register into the central registry. They are grouped into toolsets (e.g., `web`, `terminal`, `browser`, `memory`) that can be enabled or disabled per platform. Dispatch is centralized: the registry collects schemas, checks availability, and wraps errors. Terminal tools support 7 backends (local, Docker, SSH, Daytona, Modal, Singularity, Vercel Sandbox).

**LangChain:** Tools are Python callables, LangChain tools, or tool dicts passed to `create_agent`. Middleware like `ModelRetryMiddleware` and `ToolRetryMiddleware` handle fault tolerance. Deep Agents pre-assemble stacks with filesystem tools, summarization, subagents, and memory.

## 3. State and Memory Management

| Concept | Hermes Agent | LangChain Agents |
|---|---|---|
| **Session state** | SQLite + FTS5 session storage with lineage tracking (parent/child across compressions). Injected into system prompt as a frozen snapshot at session start. | `AgentState.messages` — append-only list of `BaseMessage`. Persisted via a checkpointer (`InMemorySaver`, Postgres, MongoDB, Redis, Oracle) keyed by `thread_id`. |
| **Long-term memory** | Bounded, curated files (`MEMORY.md`, `USER.md`) in `~/.hermes/memories/`. Agent manages via the `memory` tool (add/replace/remove). Strict char limits (2,200 / 1,375). | LangGraph's `BaseStore` for long-term memory. `thread_id` scopes conversation; `context` carries per-run data. External stores via `langgraph-checkpoint-*` packages. |
| **Session vs. memory** | Session state = conversation history (searchable via FTS5). Memory = curated facts (preferences, environment, lessons). Memory is injected at session start and frozen for prefix caching. | Short-term memory = thread-level checkpoints (multi-turn conversations). Long-term memory = cross-session data via `BaseStore`. |

## 4. Strengths and Trade-offs

**Hermes Agent**
- *Strengths:* Out-of-the-box tool registry (70+ tools), 25+ platform adapters, profile isolation, plugin system for memory providers and context engines, first-class cron, ACP integration for IDEs.
- *Trade-offs:* Tightly coupled to its own ecosystem; less flexible for custom graph-based workflows; memory is bounded and manually curated.

**LangChain Agents**
- *Strengths:* Highly configurable harness via middleware; composable with LangGraph's state graphs; rich ecosystem of checkpointers and stores; Deep Agents provide prebuilt stacks for long-running tasks.
- *Trade-offs:* More moving parts; requires understanding of LangGraph primitives; tool registry is not built-in — you supply tools explicitly.

**Neither is universally better.** Hermes excels as a ready-to-use agent platform with minimal setup. LangChain offers deeper customization for complex, stateful workflows at the cost of more configuration.

## 5. Suitability for This Assignment

This assignment builds a **single-agent tool-using system** that inspects directories, counts files by extension, identifies largest files, and produces a summary report. The task is simple, stateless, and file-bound.

**Hermes Agent is the better fit here** because:
- It provides a built-in tool registry and execution loop out of the box.
- The `terminal` and `execute_code` tools can run the Python utility directly.
- No custom graph or middleware is needed for a one-shot analysis task.

**LangChain would be overkill** for this use case — you would need to define tools, configure a checkpointer, and set up state schemas for a task that requires none of that complexity.

## Official Documentation

- [Hermes Architecture](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture)
- [Hermes Tools & Toolsets](https://hermes-agent.nousresearch.com/docs/user-guide/features/tools)
- [Hermes Persistent Memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory)
- [LangChain Agents](https://docs.langchain.com/oss/python/langchain/agents)
- [LangGraph Memory](https://docs.langchain.com/oss/python/langgraph/add-memory)