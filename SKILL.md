---
name: ask-foreign-agent
description: Run a remote LLM node as an interactive agent inside the Claude Code session. The foreign agent can read files, run bash commands, and reason about the codebase — Claude executes its tool calls locally and relays output prefixed with [pond-qwen].
depends_on:
  - load-topology-skill
---

# Foreign Agent

Invoke a remote LLM node (e.g. qwen3-coder on pond) as a peer agent. All output appears prefixed with `[pond-qwen]`.

## When to use

- Delegating a reasoning or research task you want visible in this session
- Getting a second opinion on a design decision
- Letting the user speak to the foreign agent interactively through you as mediator

## How to invoke

```bash
"${SKILLS_HOME:-$HOME/.agents/skills}/ask-foreign-agent-skill/.venv/bin/python3" \
  "${SKILLS_HOME:-$HOME/.agents/skills}/ask-foreign-agent-skill/agent.py" \
  --cwd <current working directory> \
  "<message>"
```

Override the target node via environment:
- `FOREIGN_AGENT_URL` — default `http://pond:9337/v1`
- `FOREIGN_AGENT_MODEL` — default `qwen3-coder-30b.gguf`

Read the topology (load-topology-skill) to find which nodes are available and what models they are running before choosing a target.

## Output format

- `[pond-qwen] ...` — text response
- `[pond-qwen:tool:tool_name] ...` — tool call
- `[pond-qwen:result] ...` — tool result (truncated if long)

## Available tools

| Tool | Description |
|---|---|
| `read_file` | Read a file by path (absolute or relative to `--cwd`) |
| `write_file` | Write content to a file |
| `edit_file` | Replace an exact string in a file |
| `bash` | Run a bash command in the working directory |
| `find_files` | Find files by name pattern |
| `grep` | Search for a pattern across files |
| `list_directory` | List directory tree |
| `git_diff` | Show unstaged and staged working-tree changes |

## Triggers

Invoke when the user says "ask qwen", "ask pond", "what does pond think", or "let qwen look at this".
