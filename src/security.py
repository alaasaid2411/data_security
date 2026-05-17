import hashlib


class PasswordHasher:
    def hash(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
