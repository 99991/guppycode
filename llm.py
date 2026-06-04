import tools
import config
import log
import json
import os
import log
import urllib.request
from datetime import datetime

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
        "HTTP-Referer": "https://github.com/99991/guppycode",
        "X-OpenRouter-Title": "GupPyCode",
        "X-OpenRouter-Categories": "cli-agent,programming-app,personal-agent",
    }

    if config.api_key:
        headers["Authorization"] = f"Bearer {config.api_key}"

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(config.args.url, data=data, headers=headers, method="POST")

    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode("utf-8"))
        log.log(config.log_path, {
            "request_data": payload,
            "request_headers": {k: v for k, v in headers.items() if k != "Authorization"}, # Don't log secrets
            "status": response.status,
            "response_headers": dict(response.getheaders()),
            "response_data": result,
        })
        return result
