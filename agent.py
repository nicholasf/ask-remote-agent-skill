#!/usr/bin/env python3
"""
ask-foreign-agent: delegate tasks to a remote autonomous agent runtime.

Peer mode:
  The remote node runs an agent runtime (Hermes, Goose, etc.). The
  orchestrating agent sends a task and receives an autonomous result.
  Gateway URL and Bearer token are read from topology.md and $SKILLS_HOME/.env.

  python3 agent.py --peer-node <hostname> "Your task"

Environment:
  SKILLS_HOME    Root directory for skills and topology (default: ~/.agents/skills)
  TOPOLOGY_PATH  Override path to topology.md
"""

import argparse
import os
import sys

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI


def _load_skills_env() -> dict[str, str]:
    skills_home = os.environ.get('SKILLS_HOME', os.path.expanduser('~/.agents/skills'))
    result: dict[str, str] = {}
    try:
        with open(os.path.join(skills_home, '.env')) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, _, v = line.partition('=')
                    result[k.strip()] = v.strip()
    except FileNotFoundError:
        pass
    return result


def _topology_node(hostname: str) -> dict[str, str]:
    skills_home = os.environ.get('SKILLS_HOME', os.path.expanduser('~/.agents/skills'))
    topology_path = os.environ.get('TOPOLOGY_PATH', os.path.join(skills_home, 'topology.md'))
    try:
        with open(topology_path) as f:
            rows = [l.strip() for l in f if l.strip().startswith('|')]
    except FileNotFoundError:
        return {}
    if len(rows) < 3:
        return {}
    headers = [h.strip() for h in rows[0].strip('|').split('|')]
    for row in rows[2:]:  # skip separator line
        values = [v.strip() for v in row.strip('|').split('|')]
        node = dict(zip(headers, values))
        if node.get('hostname') == hostname:
            return node
    return {}


def print_prefixed(text: str, prefix: str) -> None:
    for line in str(text).splitlines():
        print(f'[{prefix}] {line}')


def run_peer(message: str, peer_node: str, prefix: str) -> str:
    node = _topology_node(peer_node)
    gateway = node.get('hermes_gateway', '').replace('—', '').strip()
    key_env = node.get('hermes_key_env', '').replace('—', '').strip()

    if not gateway:
        print(f'[{prefix}] error: no hermes_gateway entry for {peer_node!r} in topology.md', file=sys.stderr)
        sys.exit(1)

    api_key = _load_skills_env().get(key_env, '') if key_env else ''

    llm = ChatOpenAI(
        base_url=f'{gateway}/v1',
        api_key=api_key or 'none',
        model='hermes-agent',
        temperature=0,
    )

    print(f'\n[{prefix}] peer → {gateway}\n', flush=True)
    response = llm.invoke([HumanMessage(content=message)])
    output = str(response.content)

    print_prefixed(output, prefix)
    print(flush=True)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description='ask-foreign-agent: delegate to a remote agent runtime')
    parser.add_argument('message', nargs='+', help='Task to send to the remote agent')
    parser.add_argument('--peer-node', required=True, help='Remote node hostname (must have Hermes or Goose running)')
    args = parser.parse_args()

    run_peer(' '.join(args.message), args.peer_node, args.peer_node)


if __name__ == '__main__':
    main()
