import prn
import tools
import config
import log
import json
import log
import urllib.request
import urllib.error

def call_llm(messages):
    payload = {
        "model": config.args.model,
        "messages": messages,
        "tools": tools.TOOL_DEFINITIONS,
    }

    if config.args.max_tokens != -1:
        payload["max_tokens"] = config.args.max_tokens

    if config.args.provider:
        payload["provider"] = {
            "order": [config.args.provider],
            "allow_fallbacks": False,
        }

    if config.args.reasoning is not None:
        payload["reasoning"] = {"enabled": config.args.reasoning}

    headers = {
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/99991/guppycode",
        "X-OpenRouter-Title": "GupPyCode",
        "X-OpenRouter-Categories": "cli-agent,programming-app,personal-agent",
        "User-Agent": config.args.user_agent,
    }

    # Use separate dict so we do not accidentally log the API key
    headers_with_auth = headers.copy()
    if config.api_key:
        headers_with_auth["Authorization"] = f"Bearer {config.api_key}"

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(config.args.url, data=data, headers=headers_with_auth, method="POST")

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            log.log(config.log_path, {
                "request_data": payload,
                "request_headers": headers,
                "status": response.status,
                "response_headers": dict(response.getheaders()),
                "response_data": result,
            })
            return result

    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        prn.red(f"HTTP Error: {e.code} - {e.reason}\n{body}")
        log.log(config.log_path, {
            "request_data": payload,
            "request_headers": headers,
            "status": e.code,
            "response_headers": dict(e.getheaders()),
            "error": {
                "code": e.code,
                "reason": e.reason,
                "body": body,
            }
        })
        return None
