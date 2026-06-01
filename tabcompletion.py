import os
import readline

def tab_completion(text, state):
    path_parts = text.rsplit('/', 1)
    if len(path_parts) == 1:
        dir_path = '.'
        partial = text
    else:
        dir_path, partial = path_parts

    try:
        files = os.listdir(dir_path)
    except FileNotFoundError:
        return None

    matches = [f for f in files if f.startswith(partial)]
    matches = [
        f + '/' if os.path.isdir(os.path.join(dir_path, f)) else f
        for f in matches
    ]

    if state < len(matches):
        return matches[state]
    return None

def activate():
    readline.set_completer(tab_completion)
    readline.parse_and_bind("tab: complete")
