Run the ask-foreign-agent (remote LLM on a topology node) with the following message and display its output in this session.

Message: $ARGUMENTS

Steps:
1. Run the agent via Bash using the command below. Use the current project working directory as `--cwd`.
2. All output is prefixed with `[pond-qwen]` — display it verbatim.
3. After the agent finishes, briefly relay its final answer to the user in plain text.

```bash
"${SKILLS_HOME:-$HOME/.agents/skills}/ask-foreign-agent-skill/.venv/bin/python3" \
  "${SKILLS_HOME:-$HOME/.agents/skills}/ask-foreign-agent-skill/agent.py" \
  --cwd <current working directory> \
  "<message>"
```

Do not summarise or paraphrase the agent's tool calls — show them as-is. If the agent errors, show the error and stop.
