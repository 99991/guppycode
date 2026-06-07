import os
import prn
import argparse
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument("--model", "-m", default="deepseek/deepseek-v4-flash", help="Model to use")
parser.add_argument("--provider", default="deepseek", help="Provider to use")
parser.add_argument("--url", default="https://openrouter.ai/api/v1/chat/completions", help="OpenAI-compatible API URL")
parser.add_argument("--max-tokens", type=int, default=32768, help="Max output tokens per LLM response")
parser.add_argument("--max-steps", type=int, default=100, help="Max agent loop steps")
parser.add_argument("--max-lines", type=int, default=5000, help="Max lines to read from file or run_bash tool. Longer files are truncated")
parser.add_argument("--max-line-length", type=int, default=1000, help="Max characters per line to read from file or run_bash tool. Longer lines are truncated")
parser.add_argument("--system-prompt", default="You are inside an Ubuntu 24.04 docker container. Current directory is /work", help="System prompt")
parser.add_argument("--no-network", action="store_false", default=False, help="Disallow agent to access the network (default: allowed)")
parser.add_argument("--nvidia", action="store_true", default=False, help="Enable NVIDIA GPU passthrough (default: disabled)")
parser.add_argument("--prompt", "-p", help="Prompt to run in single-shot non-interactive mode")
parser.add_argument("--docker-image", default="torchimage", help="Docker image to use for sandboxed execution")
parser.add_argument("--dangerous-no-sandbox", action="store_true", default=False, help="Enable NVIDIA GPU passthrough (default: sandboxed)")
parser.add_argument("--user-agent", default="GupPyCode/0.1 (https://github.com/99991/guppycode)", help="User-Agent for API requests")
parser.add_argument("--request-dir", default="~/.local/share/guppycode/requests/", help="Directory for HTTP requests")
parser.add_argument("--session-dir", default="~/.local/share/guppycode/sessions/", help="Directory for sessions")
parser.add_argument("--session", help="Full path to session file, ignores session dir")
args = parser.parse_args()

if args.model == "pro":
    args.model = "deepseek/deepseek-v4-pro"

args.session_dir = os.path.expanduser(args.session_dir)
args.request_dir = os.path.expanduser(args.request_dir)

def timestamped_file(directory, ext="jsonl"):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
    disambiguator = os.urandom(32).hex() # avoid collisions (most of the time)
    name = f"{timestamp}_{disambiguator}.{ext}"
    return os.path.join(directory, name)

if not args.session:
    args.session = timestamped_file(args.session_dir)

prn.green("Config")
for arg in vars(args):
    value = getattr(args, arg)

    if value is not None:
        if arg == "dangerous_no_sandbox":
            if args.dangerous_no_sandbox:
                prn.orange("WARNING: SANDBOX IS TURNED OFF!")
        else:
            print(f"    {arg:15}: {value}")

log_path = timestamped_file(args.request_dir)

api_key = os.environ.get("GUPPY_KEY")
