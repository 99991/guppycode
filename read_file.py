from run_bash import run_bash

def read_file(path: str) -> str:
    return run_bash(f"cat {path}")
