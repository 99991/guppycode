import prn
import tools
import config
import log
import json
import log
import collections
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

    if config.args.stream:
        payload["stream"] = True

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
            if config.args.stream:
                result = assemble_streaming_response(response)
            else:
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

def assemble_streaming_response(lines):
    result = {}
    tool_calls = {}
    message = collections.defaultdict(str)
    message["content"] = ""
    finish_reason = None

    for line in lines:
        line = line.decode("utf-8").strip()
        if not line: continue
        data_str = line.removeprefix("data: ")
        if data_str.startswith(":"): continue
        if data_str == "[DONE]": break
        chunk = json.loads(data_str)
        choices = chunk.pop("choices")
        result.update(chunk)
        if not choices: continue
        choice, = choices
        if choice.get("finish_reason"):
            finish_reason = choice["finish_reason"]
        delta = choice.get("delta")
        if not delta: continue

        for key, value in delta.items():
            if value is None: continue
            if key in ["content", "reasoning", "reasoning_content"]:
                message[key] += value
                prn.white(value, end="", flush=True)
            elif key == "role":
                message["role"] = value
            elif key == "tool_calls":
                for tool_call in value:
                    index = tool_call.pop("index")
                    arguments = tool_call["function"]["arguments"]
                    if index not in tool_calls:
                        name = tool_call["function"]["name"]
                        prn.orange(f"\nTool call: {name}", end="\n\t", flush=True)
                        tool_calls[index] = tool_call
                    else:
                        tool_calls[index]["function"]["arguments"] += arguments
                    prn.orange(arguments, end="", flush=True)
            elif key == "reasoning_details":
                pass # ignored
            else:
                raise NotImplementedError(f"delta streaming not implemented for {key=}, {value=}")

    message = dict(message)
    prn.white("\n")
    if tool_calls:
        message["tool_calls"] = [tool_calls[i] for i in sorted(tool_calls)]

    result["object"] = "chat.completion"
    result["choices"] = [
        {
            "index": 0,
            "message": message,
            "finish_reason": finish_reason,
        }
    ]
    return result
