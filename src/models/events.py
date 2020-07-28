# models.events.py


class Parameter():
    def __init__(self, data):
        for key in data.keys():
            setattr(self, key, data[key])

    def __repr__(self):
        return f'{self.value}'


class Event():
    def __init__(self, data):
        for key in data.keys():
            setattr(self, key, data[key])
        if data['parameters']:
            setattr(self, 'parameters', [Parameter(parameter) for parameter in data['parameters']])

    def __repr__(self):
        return self.uei
