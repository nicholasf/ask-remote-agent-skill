---
name: ask-foreign-agent
description: Delegate tasks to a remote autonomous agent runtime (Hermes, Goose). Peer mode sends a task to the agent's HTTP gateway; the remote agent executes autonomously and returns a result. Depends on load-topology-skill to identify available nodes and their gateway URLs.
depends_on:
  - load-topology-skill
---

## NOTE

**Always invoke this skill via its slash command — never construct the shell commands manually.**

When the user asks to delegate a task to pond or another node via natural language, invoke `/ask-foreign-agent`. The skill's own logic handles topology verification, agent health checks, and the correct peer.py invocation. Constructing the shell command manually bypasses these safeguards and leads to silent failures or hangs.

Read the topology (load-topology-skill) to find the node hostname and verify its agent gateway is running before invoking. Invoke `/ask-foreign-agent` for the full workflow.
