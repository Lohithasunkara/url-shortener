import random
import string

class Shortener:
    def __init__(self, code_length=6):
        self.code_length = code_length
        self.characters = string.ascii_letters + string.digits  # a-z, A-Z, 0-9

    def generate_code(self):
        return ''.join(random.choices(self.characters, k=self.code_length))
