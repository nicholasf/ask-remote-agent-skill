# Ask Foreign Agent

Delegate a task to a remote autonomous agent runtime (Hermes, Goose). The
remote agent receives the task, executes it using its own local tools, and
returns the result. No tool proxying — the agent is fully autonomous.

All output is prefixed with `[node-name]`.

## Agent naming convention

Refer to agents as `<machine>-<llm>-agent`, e.g. `dtv-claude-agent`,
`pond-qwen-agent`. This makes it clear which machine and model is acting.

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

## Peer mode

```bash
"${SKILLS_HOME:-$HOME/.agents/skills}/ask-foreign-agent-skill/.venv/bin/python3" \
  "${SKILLS_HOME:-$HOME/.agents/skills}/ask-foreign-agent-skill/peer.py" \
  --peer-node <hostname> \
  "<task>"
```

The gateway URL and Bearer token are read automatically from `topology.md`
and `$SKILLS_HOME/.env`. No flags needed beyond `--peer-node`.

---

## Supported agent runtimes

| Runtime | Setup guide | topology columns |
|---|---|---|
| Hermes | `docs/agents/hermes.md` | `hermes_gateway`, `hermes_key_env` |
| Goose | `docs/agents/goose.md` | `goose_acp_url` |

---

## Output format

- `[node-name] ...` — agent response

## Triggers

Invoke when the user says "ask [node]", "delegate to [node]", "let [node]
handle this", or "what does [node] think". For direct LLM interaction without
an agent runtime, use ask-foreign-llm-skill instead.
