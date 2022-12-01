# pyonms.models.exceptions.py

from typing import List


class StringLengthError(Exception):
    def __init__(self, length: int, value: str = None):
        self.max_length = length
        self.value = value
        self.message = f"String length must be under {self.max_length} characters."
        if self.value:
            self.message += f" Value '{self.value}' was {len(self.value)} characters."
        super().__init__(self.message)


class DuplicateEntityError(Exception):
    def __init__(self, name: str, model):
        self.name = name
        self.model = model
        if isinstance(self.model, str):
            model_type = self.model
        else:
            model_type = type(self.model)
        self.message = f"A {model_type} object named {self.name} already exists."
        super().__init__(self.message)


class InvalidValueError(Exception):
    def __init__(self, name: str, value: str, valid: List[str] = None):
        self.name = name
        self.value = value
        self.valid = valid
        self.message = f"{self.name} received an invalid value of {self.value}."
        if valid:
            self.message += f" Valid options are {self.valid}."
        super().__init__(self.message)


class AuthenticationError(Exception):
    def __init__(self):
        self.message = "Verify login credentials are correct."
        super().__init__(self.message)
