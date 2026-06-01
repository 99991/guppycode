import config

def truncate_line(line: str, max_length: int = config.args.max_line_length) -> str:
    if len(line) < max_length:
        return line

    message = f"...[Line truncated to {max_length} chars]..."

    assert max_length > len(message)

    a = max_length//2 - len(message) // 2
    b = max_length - a - len(message)

    line = line[:a] + message + line[-b:]

    return line

def truncate_lines(lines: list[str], max_lines: int = config.args.max_lines) -> list[str]:
    lines = [truncate_line(line) for line in lines]

    if len(lines) > max_lines:
        half = max_lines // 2
        hidden = len(lines) - 2 * half
        lines = lines[:half] + [f"...[{hidden} lines truncated]..."] + lines[-half:]

    return lines

def truncate(text: str) -> str:
    lines = text.split("\n")

    lines = truncate_lines(lines)

    text = "\n".join(lines)

    return text

def test():
    for max_length in [35, 100, 123]:
        line = truncate_line("0123456789" * 100, max_length)

        assert len(line) == max_length

    assert truncate_lines([f"line {i}" for i in range(1, 11)], 6) == [
        "line 1",
        "line 2",
        "line 3",
        "...[4 lines truncated]...",
        "line 8",
        "line 9",
        "line 10",
    ]

    # Test with odd max_lines
    assert truncate_lines([f"line {i}" for i in range(1, 11)], 5) == [
        "line 1",
        "line 2",
        "...[6 lines truncated]...",
        "line 9",
        "line 10",
    ]

if __name__ == "__main__":
    test()
