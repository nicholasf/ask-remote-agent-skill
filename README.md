# ask-remote-agent-skill

Delegate tasks to a remote autonomous agent (Hermes, Goose ACP). 

Depends on [load-topology-skill](https://github.com/nicholasf/load-topology-skill) to discover available machines, llm nodes and the agents running on them. The topology also defines **agent handles** — the `<machine>-<llm>-<agent>` names used to address a specific agent, e.g. `pond-qwen-hermes`, `gollum-mistral-goose`.

The remote agent receives the task, executes it using its own local tools, and returns the result. No tool proxying — the agent is fully autonomous.

---

## Examples

Each command takes an **agent handle** — a `<machine>[-<llm>[-<agent>]]` address that identifies exactly which agent to talk to. Start with just the machine name and add specificity as needed; unspecified parts are filled in from the topology.

### Recommended workflow: sync then run

Before delegating a task, sync to verify the remote agent is on the same branch, sha1, and language versions. If it is not, the sync output tells you what needs to change and the remote agent can act on it autonomously.

**Step 1 — sync**

```
/ask-foreign-agent sync pond-qwen-hermes
```

The repo is detected from the current git root; language versions are auto-detected from indicator files (`pyproject.toml`, `go.mod`, `package.json`, etc.). Returns structured JSON:

```json
{
  "repo_path": "/home/nicholasf/code/github/nicholasf/yggd",
  "sha1_present": true,
  "remote_sha1": "4f9a2c1d8e3b...",
  "git_commands": [],
  "languages": {
    "node":   {"requested": "20.11.0", "found": "20.11.0", "match": true},
    "python": {"requested": "3.11.0",  "found": "3.12.0",  "match": false}
  }
}
```

If `sha1_present` is `false`, `git_commands` lists the steps to bring the remote up to date.

With an explicit repo path:

```
/ask-foreign-agent sync pond-qwen-hermes --repo /home/user/code/my-project
```

**Step 2 — run**

```
/ask-foreign-agent run pond-qwen-hermes "Execute the task at tasks/pending/2026-06-13T12-00-00-add-logging.md"
```

`run` automatically prepends a **state fingerprint** to every message — a 12-character hex digest of the local branch, HEAD sha1, and language versions. The remote agent is instructed to compute its own fingerprint via `peer.py sync` and compare. If the fingerprints differ, it stops and reports the mismatch rather than proceeding with stale state.

This means `run` is self-verifying: you do not need to inspect the sync output manually before every delegation, but running `sync` first is still recommended to align state proactively.

### Agent handle variants

```
/ask-foreign-agent run pond "Summarise how the auth module works"
```
Machine only — agent and model auto-selected from topology.

```
/ask-foreign-agent run pond-qwen-hermes "Refactor the retry logic and open a PR"
```
Fully qualified: machine `pond`, LLM `qwen`, agent `hermes`.

---

## How it works

The local agent delegates a task to a remote agent handle and waits for the result. The remote agent executes autonomously — no tool calls are proxied back.

```
local-claude-agent
  │
  └─ delegates ─────────────────► pond-qwen-hermes
                                        │
                                   [reads files]
                                   [runs bash]
                                   [generates diffs or opens PRs]
                                        │
                                   own tools, own machine
                                        │
  [pond-qwen-hermes] response ◄─────────┘
```

Compare with [ask-remote-llm](https://github.com/nicholasf/ask-remote-llm-skill), where the remote LLM calls tools that execute on the local machine. Here the remote agent is fully autonomous.

---

## Supported agents

| Agent | Protocol | Topology columns | Setup |
|---|---|---|---|
| Hermes | HTTP (OpenAI-compatible) | `hermes_gateway`, `hermes_key_env` | `docs/agents/hermes.md` |
| Goose ACP | JSON-RPC 2.0 over WebSocket | `goose_acp_url` | `docs/agents/goose.md` |

---

## Topology dependency

The topology file (managed by [load-topology-skill](https://github.com/nicholasf/load-topology-skill)) is the source of truth for which nodes are available and how to reach them. Before invoking a foreign agent, load the topology to confirm the target node is online.

Example topology entry for `pond`:

```
| pond | http://pond:8642 | POND_HERMES_KEY | ws://pond:3284 |
```

Gateway URLs and API keys are read automatically from `topology.md` and `$SKILLS_HOME/.env`.

---

## Security

Delegating to a remote agent grants it autonomous execution on the target node. Before use:

- The LLM is not sandboxed. Adversarial prompt content (including content read from source files) could cause destructive commands to execute on the remote node.
- Review all results — diffs, branches, PRs — before merging or applying. Never auto-merge remote agent output.
- Use a dedicated agent user with restricted permissions where possible. Prefer nodes that are not shared with production workloads.

---

## Setup

```bash
cd "${SKILLS_HOME:-$HOME/.agents/skills}/ask-foreign-agent-skill"
uv sync
```

Dependencies: `langchain-core`, `langchain-openai`, `websockets`.
