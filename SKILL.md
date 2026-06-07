---
name: ask-foreign-agent
description: Delegate tasks to a remote autonomous agent runtime (Hermes, Goose). Peer mode sends a task to the agent's HTTP gateway; the remote agent executes autonomously and returns a result. Depends on load-topology-skill to identify available nodes and their gateway URLs.
depends_on:
  - load-topology-skill
---

Read the topology (load-topology-skill) to find the node hostname and verify its agent gateway is running before invoking. Invoke `/ask-foreign-agent` for the full workflow.
