from run_bash import run_bash

def read_file(path: str) -> dict[str, str] | str:
    ext = path.rsplit(".")[-1].lower().replace("jpg", "jpeg")
    if ext in ["png", "jpeg"]:
        data = run_bash(f"cat '{path}' | base64 -w 0", limit=False)
        return {
            "type": "image",
            "data": f"data:image/{ext};base64," + data,
        }
    else:
        return run_bash(f"cat '{path}'")
