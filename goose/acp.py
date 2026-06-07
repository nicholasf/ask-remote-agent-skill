import asyncio
import json

import websockets

_PROTOCOL_VERSION = "2025-05-12"


async def _run(base_url: str, message: str, cwd: str) -> str:
    url = base_url.rstrip("/") + "/acp"

    async with websockets.connect(url) as ws:
        _id = 0

        async def call(method: str, params: dict) -> int:
            nonlocal _id
            _id += 1
            await ws.send(json.dumps({"jsonrpc": "2.0", "method": method, "id": _id, "params": params}))
            return _id

        async def recv_result(expected_id: int) -> dict:
            while True:
                frame = json.loads(await ws.recv())
                if frame.get("id") == expected_id:
                    if "error" in frame:
                        raise RuntimeError(frame["error"]["message"])
                    return frame.get("result", {})

        await recv_result(await call("initialize", {"protocolVersion": _PROTOCOL_VERSION}))

        new_id = await call("session/new", {"cwd": cwd, "mcpServers": []})
        session_id = None
        while True:
            frame = json.loads(await ws.recv())
            if frame.get("id") == new_id:
                session_id = frame["result"]["sessionId"]
                break
            if frame.get("method") == "session/update" and not session_id:
                session_id = frame.get("params", {}).get("sessionId")

        prompt_id = await call("session/prompt", {
            "sessionId": session_id,
            "prompt": [{"type": "text", "text": message}],
        })

        chunks: list[str] = []
        while True:
            frame = json.loads(await ws.recv())
            if frame.get("method") == "session/update":
                update = frame.get("params", {}).get("update", {})
                if update.get("sessionUpdate") == "agent_message_chunk":
                    text = update.get("content", {}).get("text", "")
                    if text:
                        chunks.append(text)
            elif frame.get("id") == prompt_id:
                if "error" in frame:
                    raise RuntimeError(frame["error"]["message"])
                break

        return "".join(chunks)


def prompt(url: str, message: str, *, cwd: str = "/tmp") -> str:
    """Send a task to a remote Goose ACP server and return the response text."""
    return asyncio.run(_run(url, message, cwd))
