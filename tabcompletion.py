import os
import readline

def tab_completion(text, state):
    dir_path = os.path.dirname(text)
    partial = os.path.basename(text)

    if not dir_path:
        dir_path = '.'

    try:
        entries = os.listdir(dir_path)
    except (FileNotFoundError, NotADirectoryError, PermissionError):
        return None

    matches = [name for name in entries if name.startswith(partial)]

    matches = [
        name + '/' if os.path.isdir(os.path.join(dir_path, name)) else name
        for name in matches
    ]

    if dir_path != '.':
        prefix = dir_path if dir_path.endswith('/') else dir_path + '/'
        matches = [prefix + name for name in matches]

    if state < len(matches):
        return matches[state]
    return None

def activate():
    # Enable tab completion after 'subdir/'
    delims = readline.get_completer_delims()
    readline.set_completer_delims(delims.replace('/', ''))

    readline.set_completer(tab_completion)
    readline.parse_and_bind("tab: complete")
