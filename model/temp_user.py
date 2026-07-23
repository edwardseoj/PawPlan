import tempfile
import os

class UserIdStore:
    def __init__(self):
        self.filepath = os.path.join(tempfile.gettempdir(), "current_user_id.txt")

    def set(self, uid):
        with open(self.filepath, "w") as f:
            f.write(uid)

    def get(self):
        if not os.path.exists(self.filepath):
            return None
        with open(self.filepath, "r") as f:
            return f.read().strip()

    def clear(self):
        if os.path.exists(self.filepath):
            os.remove(self.filepath)