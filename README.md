# GupPyCode

This is mostly for my own use on Lubuntu 24.04 with weird defaults.
It will probably not work on your system and might contain bugs.

But perhaps there is something interesting in the code that you find useful.
Consider this repository mostly educational.

# Installation

Go to whichever directory you want to install it in and run

```
git clone https://github.com/99991/GupPyCode.git
cd GupPyCode
ln -s "$PWD/gup.py" ~/.local/bin/guppy
```

Or just run `python gup.py`. For usage, see `guppy --help`

By default, `guppy` currently uses DeepSeek-V4-Flash through OpenRouter (`export GUPPY_KEY='your API key here').
If you want to use a local model with [llama-server](https://github.com/ggml-org/llama.cpp#quick-start), run

```
guppy --url http://127.0.0.1:8080/v1/chat/completions
```

# Features

* Tool calls are executed in a sandboxed environment within a Docker container that only allows access to the current directory and some NVIDIA files (see `run_bash.py`)
* NVIDIA GPU passthrough (this probably opens up a container escape somewhere, but better than no sandbox at all)
    * Notably, this does not use NVIDIA container toolkit, which failed to install on my system.
    * Might not work on your system. Can be disabled with `guppy --no-nvidia`
* Fuzzy matching for `str_replace` tool with Levenshtein distance
* No weird TUI that hides most of what's going on and messes up scrolling
* Tab file name completion
* Readline input (i.e. Ctrl + W, Home and End keys work)
* Small codebase that can be read in a few minutes (<700 lines including blank lines)
* No external dependencies (one of the main motivations for this project due to the recent increase in supply chain attacks)
