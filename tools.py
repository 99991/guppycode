from run_bash import run_bash
from read_file import read_file
from write_file import write_file
from str_replace import str_replace

def tool_call(tool, names):
    def wrapper(args):
        # Complain if LLM hallucinated parameter names
        if args.keys() != set(names):
            return f"ERROR: Got args {list(args.keys())} but need args {names}"
        return tool(*[args[name] for name in names])
    return wrapper

TOOL_MAP = {
    "bash": tool_call(run_bash, ["command"]),
    "read_file": tool_call(read_file, ["path"]),
    "write_file": tool_call(write_file, ["path", "content"]),
    "str_replace": tool_call(str_replace, ["path", "old_str", "new_str"]),
}

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "bash",
            "description": "Runs a bash command inside a container.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string"}
                },
                "required": ["command"]
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads text, png or jpg files.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"}
                },
                "required": ["path"]
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Writes content to a file and creates it and its parent directories if they do not exist yet. Prefer str_replace for editing.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["path", "content"]
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "str_replace",
            "description": "Replaces a string in a file. String must start and end at line boundaries. More efficient for small changes in big files.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "old_str": {"type": "string"},
                    "new_str": {"type": "string"},
                },
                "required": ["path", "old_str", "new_str"]
            },
        },
    },
]
