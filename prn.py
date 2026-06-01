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

def black(text, **kwargs):
    print(termcolors["black"] + text + "\033[0m")

def red(text, **kwargs):
    print(termcolors["red"] + text + "\033[0m")

def green(text, **kwargs):
    print(termcolors["green"] + text + "\033[0m")

def yellow(text, **kwargs):
    print(termcolors["yellow"] + text + "\033[0m")

def blue(text, **kwargs):
    print(termcolors["blue"] + text + "\033[0m")

def magenta(text, **kwargs):
    print(termcolors["magenta"] + text + "\033[0m")

def cyan(text, **kwargs):
    print(termcolors["cyan"] + text + "\033[0m")

def white(text, **kwargs):
    print(termcolors["white"] + text + "\033[0m")

def lightwhite(text, **kwargs):
    print(termcolors["lightwhite"] + text + "\033[0m")

def orange(text, **kwargs):
    print(termcolors["orange"] + text + "\033[0m")