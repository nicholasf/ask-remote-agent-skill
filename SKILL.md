---
name: ask-foreign-agent
description: Run a remote LLM node as an interactive agent. Supports bridge mode (proxied local tool calls) and peer mode (remote agent clones the repo and works autonomously via SSH). Depends on load-topology-skill to identify available nodes.
depends_on:
  - load-topology-skill
---

Read the topology (load-topology-skill) to find the node hostname and verify it is online before invoking. Invoke `/ask-foreign-agent` for the full workflow.
