def levenshtein_distance(s: str, t: str) -> int:
    if not s or not t:
        return max(len(s), len(t))
    prev = list(range(len(t) + 1))
    for i, c in enumerate(s):
        curr = [i + 1]
        for p, q, r, d in zip(prev, prev[1:], curr, t):
            curr.append(min(p + (c != d), q + 1, r + 1))
        prev = curr
    return prev[-1]

def test():
    assert levenshtein_distance("kitten", "sitting") == 3

if __name__ == "__main__":
    test()
