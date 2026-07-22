from run_bash import run_bash
import os

def write_file(path: str, content: str) -> str:
    # Create parent directories if they don't exist
    parent_dir = os.path.dirname(path)

    if parent_dir:
        run_bash(f"mkdir -p '{parent_dir}'")

    # Use cat with heredoc to write the file
    # Use a unique unpredictable delimiter that is probabilistically impossible to appear in output
    delimiter = os.urandom(32).hex()

    # Always add line break at end of file since delimiter is not recognized otherwise
    if not content.endswith("\n"):
        content += "\n"

    run_bash(f"cat << '{delimiter}' > {path}\n{content}{delimiter}")
    return f"Wrote file: {path}"

def test():
    from read_file import read_file

    path = "a4a96638dcb.txt"
    text = "line 1\nline 2"
    # TODO how to write file without adding new line?
    expected_text = text + "\n"

    write_file(path, text)

    for _ in range(2):
        text = read_file(path)
        write_file(path, text)

    text = read_file(path)

    assert text == expected_text

    os.remove(path)

if __name__ == "__main__":
    test()
