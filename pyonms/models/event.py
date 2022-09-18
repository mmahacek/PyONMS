# models.event.py


class Event_Parameter:
    def __init__(self, data):
        for key, value in data.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"{self.value}"


class Event:
    def __init__(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        if data["parameters"]:
            self.parameters = [
                Event_Parameter(parameter) for parameter in data["parameters"]
            ]

    def __repr__(self):
        return self.uei
