# Goose Agent Setup

[Goose](https://block.goose.ai/) is an agent runtime for peer mode. When running
on a remote node as an ACP server, it receives tasks over WebSocket, executes them
autonomously using its own local tools, and returns results.

---

## ACP Integration Design

Goose exposes an ACP (Agent Client Protocol) server via `goose serve`. The
protocol is JSON-RPC 2.0 over WebSocket, with all messages sent to and received
from a single `/acp` endpoint.

### Connection flow

```
client                            goose serve (:3284)
  │                                      │
  ├─ GET /acp (WebSocket upgrade) ───────►│
  │◄── 101 Switching Protocols ──────────┤
  │    Acp-Connection-Id: <uuid>         │
  │                                      │
  ├─ initialize {protocolVersion} ───────►│
  │◄── agentCapabilities ────────────────┤
  │                                      │
  ├─ session/new {cwd, mcpServers:[]} ───►│
  │◄── session/update (available_cmds)   │
  │◄── result {sessionId} ───────────────┤
  │                                      │
  ├─ session/prompt {sessionId, prompt} ─►│
  │◄── session/update (message chunks)   │
  │◄── result {stopReason: end_turn} ────┤
```

### Message format

User messages in `session/prompt` use a typed content array:

```json
{
  "jsonrpc": "2.0",
  "method": "session/prompt",
  "id": 3,
  "params": {
    "sessionId": "20260607_1",
    "prompt": [{"type": "text", "text": "your task here"}]
  }
}
```

Valid content types: `text`, `image`, `audio`, `resource_link`, `resource`.

### Response events

The server streams `session/update` notifications while processing. The response
text arrives in `agent_message_chunk` updates. Processing ends when the method
call returns `{"stopReason": "end_turn"}`.

```json
{"method": "session/update", "params": {
  "sessionId": "...",
  "update": {"sessionUpdate": "agent_message_chunk", "content": {"type": "text", "text": "..."}}
}}
```

### Topology column

| column | value |
|---|---|
| `goose_acp_url` | `ws://<hostname>:3284` |

---

## Installation

Install Goose on the remote node using the official install script:

```bash
curl -fsSL https://github.com/block/goose/releases/latest/download/install.sh | bash
```

This installs the `goose` binary to `~/.local/bin/goose`. Verify:

```bash
goose --version
```

---

## Step 1 — Verify llama-server is running

Goose delegates inference to the local llama-server. Confirm it is healthy:

```bash
curl -s http://localhost:9337/health
# Expected: {"status":"ok"}
```

If not running, start it (see hermes.md Step 1 for context size requirements).

---

## Step 2 — Start the ACP server

Start `goose serve` with the OpenAI-compatible provider pointing at the local
llama-server:

```bash
OPENAI_HOST=http://localhost:9337 \
OPENAI_API_KEY=none \
GOOSE_PROVIDER=openai \
GOOSE_MODEL=<model-name> \
nohup ~/.local/bin/goose serve --host 0.0.0.0 --port 3284 \
  > ~/.goose/logs/serve.log 2>&1 &
```

Replace `<model-name>` with the model identifier the llama-server is running
(e.g. `qwen3:32b`).

Verify the server is up:

```bash
curl -s http://localhost:3284/          # returns 404 (expected — no REST routes)
```

A 404 with `access-control-expose-headers: acp-connection-id,acp-session-id` in
the response confirms the ACP server is listening correctly.

---

## Step 3 — Register in topology

On the orchestrating machine, add `goose_acp_url` to the node's row in
`$SKILLS_HOME/topology.md`:

| column | value |
|---|---|
| `goose_acp_url` | `ws://pond:3284` |

No API key is needed — the ACP server does not require authentication by default.

---

## Step 4 — Verify end-to-end

From the orchestrating machine:

```bash
python3 peer.py --peer-node <hostname> "say hello in one word"
```

Expected output:

```
[pond] peer → ws://pond:3284

[pond] Hello!
```

---

## Notes

- `goose serve` binds to `127.0.0.1` by default. Pass `--host 0.0.0.0` to allow
  remote connections.
- The ACP server is not the same as `goose acp`, which is a stdio-based interface
  for local subprocess use.
- The `/acp` path is the WebSocket endpoint. All other HTTP paths return 404 by
  design — this is not an error.
- To auto-start on reboot, create a systemd unit or add to your shell's startup
  file with the required env vars.
