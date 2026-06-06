# Ask Foreign Agent

Invoke an LLM node from the topology as a peer agent. All output is prefixed with `[node-name]`.

## Before invoking

Read the topology (load-topology-skill) to:
- Find the node hostname
- Confirm the node is online (`ssh: yes`)
- Verify its inference server is active (`curl -s http://<hostname>:9337/v1/models`)

Set `$FOREIGN_AGENT_URL` and `$FOREIGN_AGENT_MODEL` to target the node.

## Bridge mode

The remote agent uses proxied tools to access the local filesystem. Tool calls execute on the orchestrating agent's machine. Use for inspection, question, or execution tasks where the remote agent works against the local codebase.

```bash
"${SKILLS_HOME:-$HOME/.agents/skills}/ask-foreign-agent-skill/.venv/bin/python3" \
  "${SKILLS_HOME:-$HOME/.agents/skills}/ask-foreign-agent-skill/agent.py" \
  --cwd <working directory> \
  "<message>"
```

## Peer mode

The remote agent clones the repository to its own machine and works against it directly. Tool calls execute on the remote node via SSH. The orchestrating agent's working copy is untouched. Results are returned via `git diff`, a pushed branch, or a pull request.

```bash
"${SKILLS_HOME:-$HOME/.agents/skills}/ask-foreign-agent-skill/.venv/bin/python3" \
  "${SKILLS_HOME:-$HOME/.agents/skills}/ask-foreign-agent-skill/agent.py" \
  --node <hostname> \
  --repo <git-url> \
  "<message>"
```

`$AGENT_SSH_USER` must be set for SSH connections. `--remote-path` overrides the default clone location (`/tmp/ask-foreign-agent/<repo-name>`).

## Output format

- `[node-name] ...` — text response
- `[node-name:tool:tool_name] ...` — tool call
- `[node-name:result] ...` — tool result (truncated if long)

## Bridge mode toolset

| Tool | Description |
|---|---|
| `read_file` | Read a file by path |
| `write_file` | Write content to a file |
| `edit_file` | Replace an exact string in a file |
| `bash` | Run a bash command in the working directory |
| `find_files` | Find files by name pattern |
| `grep` | Search for a pattern across files |
| `list_directory` | List directory tree |
| `git_diff` | Show unstaged and staged changes |

In peer mode only `bash` is exposed — the remote agent has full shell access on its own machine.

## Triggers

Invoke when the user says "ask [node]", "what does [node] think", or "let [node] look at this".
