from levenshtein_distance import levenshtein_distance
from read_file import read_file
from write_file import write_file
import collections
import os

def expandtabs(text):
    return text.replace("\t", " " * 4)

def indentation(line):
    return len(line) - len(line.lstrip())

def dedent(lines):
    min_indentation = min((indentation(line) for line in lines), default=0)
    return [line[min_indentation:] for line in lines]

def compute_dist(lines1, lines2):
    assert len(lines1) == len(lines2)
    return sum(levenshtein_distance(expandtabs(a), expandtabs(b))
        for a, b in zip(dedent(lines1), dedent(lines2)))

def str_replace(path: str, old_str: str, new_str: str):
    text = read_file(path)

    # fast path for exact match
    if text.count(old_str) == 1:
        text = text.replace(old_str, new_str)
        return write_file(path, text)

    lines = text.split("\n")

    old_lines = old_str.split("\n")
    new_lines = new_str.split("\n")

    dists = collections.defaultdict(list)

    m = len(old_lines)

    for i in range(len(lines) - m + 1):
        dist = compute_dist(lines[i:i + m], old_lines)
        dists[dist].append(i)

    min_dist = min(dists)
    indices = dists[min_dist]

    if len(indices) > 1:
        # TODO line numbers
        line_numbers = ", ".join(str(i + i) for i in indices)
        return f"ERROR: Multiple possible match positions at lines {line_numbers} with levenshtein distance {min_dist}"

    i, = indices
    lines = lines[:i] + new_lines + lines[i + m:]

    text = "\n".join(lines)

    return write_file(path, text) + f"\nReplaced {m} old lines with {len(new_lines)} new lines at line {i + 1}"

def test():
    path = "c81b845e1853077bb42f.txt"

    with open(path, "w") as f:
        f.write("""import numpy as np

if 1:
    def sub(a, b):
        return a + b

def mul(x, y):
    return x * y

""")

    result = str_replace(path, "def sab(a,b):\n\treturn a+b", "    def sub(a, b):\n        return a - b")

    assert result.startswith("Wrote ")

    with open(path) as f:
        text = f.read()

    expected_text = """import numpy as np

if 1:
    def sub(a, b):
        return a - b

def mul(x, y):
    return x * y

"""

    assert text == expected_text

    result = str_replace(path, "", "\n\n")

    assert result.startswith("ERROR: Multiple")

    os.remove(path)

if __name__ == "__main__":
    test()
