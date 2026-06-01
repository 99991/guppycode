import tools
import config
import json
import urllib.request

def call_llm(messages):
    payload = {
        "model": config.args.model,
        "messages": messages,
        "tools": tools.TOOL_DEFINITIONS,
        "max_tokens": config.args.max_tokens,
    }

    if config.args.provider:
        payload["provider"] = {
            "order": [config.args.provider],
            "allow_fallbacks": False,
        }

    headers = {
        "Content-Type": "application/json",
    }

    if config.api_key:
        headers["Authorization"] = f"Bearer {config.api_key}"

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(config.args.url, data=data, headers=headers, method="POST")

    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode("utf-8"))
