# GupPyCode

<div align="center">
<img width="535" height="334" alt="Orange guppy fish that looks a bit dumb" src="https://github.com/user-attachments/assets/652bed3b-a11d-44ae-acaa-3b87dc6f6315" />
</div>

This is a CLI coding agent mostly for my own use on Lubuntu 24.04 with weird defaults.
It will probably not work on your system and might contain bugs.

But perhaps there is something interesting in the code that you find useful.
Consider this repository mostly educational.

# Installation

1. Change the Python libraries in `Dockerfiles/torch/Dockerfile` to your liking.
2. Go to whichever directory you want to install in and run

```bash
git clone https://github.com/99991/guppycode.git
cd guppycode
docker build \
    --build-arg UID="$(id -u)" \
    --build-arg GID="$(id -g)" \
    -t torchimage Dockerfiles/torch
ln -s "$PWD/gup.py" ~/.local/bin/guppy
guppy
```

For usage, see `guppy --help`

Instead of `torchimage`, you can choose your own Docker image with `guppy --docker-image yourimage` or the `Dockerfile/js` or `Dockerfile/go` image (untested).

You can also run `python gup.py` directly instead of linking `guppy` into a directory on your `$PATH`.

By default, `guppy` currently uses DeepSeek-V4-Flash through OpenRouter (`export GUPPY_KEY='your API key here'`).
If you want to use a local model with [llama-server](https://github.com/ggml-org/llama.cpp#quick-start), serve your model with `llama-server` and run

```bash
guppy --url http://127.0.0.1:8080/v1/chat/completions
```

# Features

* Tool calls are executed in a sandboxed environment within a Docker container that only allows access to the current directory (and optionally some NVIDIA files, see `run_bash.py`)
* NVIDIA GPU passthrough (this probably opens up a container escape somewhere, but better than no sandbox at all)
    * Activate with `guppy --nvidia`
    * Notably, this does not use NVIDIA container toolkit, which failed to install on my system. The current method is somewhat unorthodox and might not work on your system.
* Fuzzy matching for `str_replace` tool with Levenshtein distance
* No weird TUI that hides most of what's going on and messes up scrolling
* Tab file name completion
* Readline input (i.e. Ctrl + W, Home and End keys work)
* Plays a sound when done! (surprisingly nice)
* Small codebase that can be read in a few minutes (<1000 lines)
* No external dependencies (one of the main motivations for this project due to the recent increase in supply chain attacks)

# Safety

* You should use git with your agent so you can undo undesired changes.
The agent can be disallowed from messing with the git history by starting `guppy` in a subdirectory of your git repository.

```
repository
├── .git
└── subdirectory <--- start guppy in here
    └── .git <--- (optional) local .git so your agent can still use git if it wants to
```

## SOCKS5 Proxy

Since some API providers ban certain countries, you might want to use a proxy.
First, install `tsocks` and start a SOCKS5 proxy on e.g. port 9000.

```bash
sudo apt install tsocks
ssh -D 9000 yourusername@yourserver.net
```

Then create a configuration file and use `tsocks` to start `guppy`.

```bash
export TSOCKS_CONF_FILE='/tmp/myconf' # alternatively, make permanent by writing to ~/.tsocks.conf
echo -e "server = 127.0.0.1\nserver_port = 9000\nserver_type = 5" > $TSOCKS_CONF_FILE
tsocks guppy
```

Requests will then be routed through your server.
To check that it works, the following two commands should return different IP addresses.

```bash
curl https://ip4only.me/api/
tsocks curl https://ip4only.me/api/
```
