# Ask Foreign Agent

Delegate a task to a remote autonomous agent runtime (Hermes, Goose). The
remote agent receives the task, executes it using its own local tools, and
returns the result. No tool proxying — the agent is fully autonomous.

All output is prefixed with `[node-name]`.

## Agent naming convention

Refer to agents by their **agent handle** — `<machine>-<llm>-<agent>`, e.g.
`pond-qwen-hermes`, `pond-qwen-goose`, `gollum-mistral-hermes`. This makes it
unambiguous which machine, model, and agent is acting. The node argument to
both subcommands follows this convention — omit parts you don't need and
defaults are applied.

## Before invoking

1. Load the topology (load-topology-skill) — this sources `$SKILLS_HOME/.env`
   and reads `topology.md`.
2. Confirm the target node has a `hermes_gateway` or `goose_acp_url` entry.
3. Verify the gateway is reachable:

```bash
# Hermes
curl -s -H "Authorization: Bearer $<NODE>_HERMES_KEY" http://<hostname>:8642/v1/models

# Goose — a 404 with acp headers confirms the server is up
curl -sv http://<hostname>:3284/ 2>&1 | grep "acp-connection-id"
```

---

## Subcommands

### run — delegate a task

```bash
"${SKILLS_HOME:-$HOME/.agents/skills}/ask-remote-agent-skill/.venv/bin/python3" \
  "${SKILLS_HOME:-$HOME/.agents/skills}/ask-remote-agent-skill/peer.py" \
  run <node> "<task>"
```

`<node>` is an agent handle — `<machine>[-<llm>[-<agent>]]`, e.g. `pond`,
`pond-qwen-hermes`, `pond-qwen-goose`. The gateway URL and Bearer token are
read automatically from `topology.md` and `$SKILLS_HOME/.env`.

### sync — negotiate repo and language state

```bash
"${SKILLS_HOME:-$HOME/.agents/skills}/ask-remote-agent-skill/.venv/bin/python3" \
  "${SKILLS_HOME:-$HOME/.agents/skills}/ask-remote-agent-skill/peer.py" \
  sync <node> [--repo /path/to/repo] [--lang python=3.11]
```

`--repo` defaults to the git root of the current working directory. `--lang`
defaults to auto-detection from indicator files (`pyproject.toml`, `go.mod`,
`package.json`, etc.) and locally installed versions — no flags required for
the common case.

Reads the local repo's current branch and HEAD SHA1, sends them to the remote
agent along with detected language versions, and returns a JSON report:

```json
{
  "repo_path": "/home/user/repo",
  "sha1_present": true,
  "remote_sha1": "<HEAD at repo_path>",
  "git_commands": [],
  "languages": {
    "python": {"requested": "3.11", "found": "3.12.0", "match": false}
  }
}
```

If `sha1_present` is false, `git_commands` contains the steps to bring the
remote up to date. The remote agent can act on the report autonomously.

---

## Topology subcommand

When configuring an agent handle for the first time, or after switching between thinking-enabled and standard model modes, set `reasoning_buffer` in topology.md:

```bash
"${SKILLS_HOME:-$HOME/.agents/skills}/ask-remote-agent-skill/.venv/bin/python3" \
  "${SKILLS_HOME:-$HOME/.agents/skills}/ask-remote-agent-skill/peer.py" \
  topology <node> --reasoning-buffer <N>
```

`--reasoning-buffer N` sets the `reasoning_buffer` column in the `## Agent State` table of `topology.md` for the agent handle. This value is read by track-tasks-skill during pre-flight token estimation to determine whether an estimated task fits the remote context window.

**When to set it:**
- When configuring a new agent handle for the first time
- When switching the model between thinking-enabled (e.g. Qwen3 with `<think>` blocks) and standard modes
- After a benchmark reveals the default estimate overflows consistently

**Guidance:**
- Qwen3 with extended thinking enabled: `12000`
- Qwen2.5 or models without extended thinking: `0`

The value is preserved across `load-topology discover` runs; only this command changes it.

---

## Supported agents

| Agent | Setup guide | topology columns |
|---|---|---|
| Hermes | `docs/agents/hermes.md` | `hermes_gateway`, `hermes_key_env` |
| Goose | `docs/agents/goose.md` | `goose_acp_url` |

Both agent types share the `reasoning_buffer` column in `## Agent State` (set via the `topology` subcommand above).

---

## Output format

- `[node-name] ...` — agent response

## Triggers

Invoke when the user says "ask [node]", "delegate to [node]", "let [node]
handle this", or "what does [node] think". For direct LLM interaction without
a raw LLM, use ask-foreign-llm-skill instead.
