import secrets

class RandomUtil:
    @staticmethod
    def generate_random_code(length: int = 12) -> str:
        return secrets.token_hex(length)  