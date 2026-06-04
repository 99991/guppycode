import os
import json


class Session:
    def __init__(self, path):
        self.path = path

    def _open_file(self, mode):
        parent = os.path.dirname(self.path)

        if parent:
            os.makedirs(parent, exist_ok=True)

        return open(self.path,mode)

    def append(self, message):
        with self._open_file("a") as f:
            f.seek(0, os.SEEK_END)
            f.write(json.dumps(message) + "\n")

    def get_messages(self):
        with self._open_file("r") as f:
            f.seek(0)
            return [json.loads(line) for line in f if line]

def test():
    disambiguator = os.urandom(32).hex()
    session = Session(f"/tmp/session_{disambiguator}.jsonl")
    session.append({"foo": "bar"})
    session.append({"x": "y"})
    assert session.get_messages() == [{"foo": "bar"}, {"x": "y"}]

if __name__ == "__main__":
    test()