import os
import prn
import argparse

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
parser.add_argument("--no-nvidia", action="store_true", default=False, help="Disable NVIDIA GPU passthrough")
parser.add_argument("--prompt", "-p", help="Prompt to run in single-shot non-interactive mode")
args = parser.parse_args()

if args.model == "pro":
    args.model = "deepseek/deepseek-v4-pro"

prn.green("Config")
for arg in vars(args):
    value = getattr(args, arg)
    if value is not None:
        print(f"    {arg:15}: {value}")

api_key = os.environ.get("GUPPY_KEY")
