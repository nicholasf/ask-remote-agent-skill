# Hermes Setup — Session Notes

## Context

These notes pick up from a yggd development session (2026-06-07) where we:

1. Refactored `ask-foreign-agent-skill` to cleanly define three modes (see PR `bridge-ssh-peer-mode-split`)
2. Installed Hermes on pond (completed, not yet configured)
3. Confirmed gollum already has Hermes installed

The goal now is to configure Hermes on pond and gollum, run independent tests, and validate peer mode (agent-to-agent) works end-to-end.

---

## Three modes (as refactored)

- **Bridge (local)** — `agent.py --cwd <path>`. Tool calls run on dtv. Use for local codebase tasks.
- **Bridge (SSH)** — `agent.py --ssh-node <host> --ssh-cwd <path>`. Tool calls run on remote node via SSH. Use when the node has the repo/toolchain but no Hermes.
- **Peer** — agent-to-agent. dtv-claude-agent sends a task to a Hermes instance running pond-qwen-agent or gollum-qwen-agent. The remote agent executes autonomously and returns a result. **This is what we're setting up.**

## Agent naming convention

`<machine>-<llm>-agent` — e.g. `dtv-claude-agent`, `pond-qwen-agent`, `gollum-qwen-agent`.

---

## Pond

- **Hermes**: installed at `~/.hermes/`, not yet configured
- **LLM**: `qwen3-coder-30b.gguf` running on `llama-server` at `http://localhost:9337`
- **Next**: run `hermes setup` on pond, point it at `http://localhost:9337`

```bash
ssh pond
hermes setup
# When prompted for API base URL: http://localhost:9337
# Model: qwen3-coder-30b.gguf
```

After setup, verify:
```bash
ssh pond "hermes --version && curl -s http://localhost:9337/v1/models | python3 -m json.tool"
```

---

## Gollum

- **Hermes**: already installed and previously configured
- **LLM**: check what's running — likely `qwen2.5-coder:14b` or `qwen2.5-coder:7b` via Ollama
- **Next**: confirm Hermes is configured and responsive, check which model it's using

```bash
ssh gollum "hermes config"
ssh gollum "curl -s http://localhost:11434/api/tags | python3 -m json.tool"
```

---

## Peer mode — what needs to happen

Once Hermes is configured on both nodes:

1. Understand how Hermes accepts tasks programmatically (HTTP API or CLI)
2. Update `command.md` in this repo with the real peer mode invocation
3. Implement peer mode in `agent.py` — send task to Hermes endpoint, receive result
4. Test with a simple task on gollum first (smaller model, less risk), then pond

Key question: does Hermes expose an HTTP API for receiving tasks, or is it CLI-only? Check `hermes --help` and the Hermes docs at https://hermes-agent.nousresearch.com/.

---

## Open PR

`bridge-ssh-peer-mode-split` — refactors bridge/SSH/peer modes, waiting for review before merge.
