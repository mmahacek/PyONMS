# pyonms.models.exceptions.py

"""Custom exception model"""

from typing import List, Optional


class StringLengthError(Exception):
    """String length too long error"""

    def __init__(self, length: int, value: Optional[str] = None):
        self.max_length = length
        self.value = value
        self.message = f"String length must be under {self.max_length} characters."
        if self.value:
            self.message += f" Value '{self.value}' was {len(self.value)} characters."
        super().__init__(self.message)


class DuplicateEntityError(Exception):
    """Duplicate object exists error"""

    def __init__(self, name: str, model):
        self.name = name
        self.model = model
        if isinstance(self.model, str):
            model_type = self.model
        else:
            model_type = str(type(self.model))
        self.message = f"A {model_type} object named {self.name} already exists."
        super().__init__(self.message)


class InvalidValueError(Exception):
    """Invalid value error"""

    def __init__(self, name: str, value: str, valid: Optional[List] = None):
        self.name = name
        self.value = value
        self.valid = valid
        self.message = f"{self.name} received an invalid value of {self.value}."
        if valid:
            self.message += f" Valid options are {self.valid}."
        super().__init__(self.message)


class AuthenticationError(Exception):
    """Authentication failure error"""

    def __init__(self):
        self.message = "Verify login credentials are correct."
        super().__init__(self.message)


class ApiPayloadError(Exception):
    """API Payload error"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
