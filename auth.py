import hashlib


class User:
    def __init__(self, username, password):
        self.username = username
        self.password_hash = self._hash_password(password)

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.password_hash == self._hash_password(password)
