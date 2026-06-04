import os
import log

class Session:
    def __init__(self, path):
        self.path = path

    def append(self, message):
        log.log(self.path, message)

    def get_messages(self):
        return log.read(self.path)

def test():
    disambiguator = os.urandom(32).hex()
    session = Session(f"/tmp/session_{disambiguator}.jsonl")
    session.append({"foo": "bar"})
    session.append({"x": "y"})
    assert session.get_messages() == [{"foo": "bar"}, {"x": "y"}]

if __name__ == "__main__":
    test()
