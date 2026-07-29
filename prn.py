termcolors = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "lightwhite": "\033[97m",
    "orange": "\033[38;5;208m",
}

def _print(color, text, **kwargs):
    print(termcolors[color] + text + "\033[0m", **kwargs)

def black(text, **kwargs):
    _print("black", text, **kwargs)

def red(text, **kwargs):
    _print("red", text, **kwargs)

def green(text, **kwargs):
    _print("green", text, **kwargs)

def yellow(text, **kwargs):
    _print("yellow", text, **kwargs)

def blue(text, **kwargs):
    _print("blue", text, **kwargs)

def magenta(text, **kwargs):
    _print("magenta", text, **kwargs)

def cyan(text, **kwargs):
    _print("cyan", text, **kwargs)

def white(text, **kwargs):
    _print("white", text, **kwargs)

def lightwhite(text, **kwargs):
    _print("lightwhite", text, **kwargs)

def orange(text, **kwargs):
    _print("orange", text, **kwargs)
