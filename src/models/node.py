# models.node.py

""" Model classes for Node-related objects.
    All fields are being dynamically detected based on the data
    returned from the API, to provide flexibility as fields are
    added in future versions.
"""


class assetRecord():
    def __init__(self, data):
        for key in data.keys():
            setattr(self, key, data[key])

#    def __repr__(self):
#        return self.label


class snmpInterface():
    def __init__(self, data):
        for key in data.keys():
            setattr(self, key, data[key])

    def __repr__(self):
        return self.ifAlias


class ipInterface():
    def __init__(self, data):
        for key in data.keys():
            setattr(self, key, data[key])
        if data.get('snmpInterface'):
            self.snmpInterface = snmpInterface(data['snmpInterface'])

    def __repr__(self):
        return self.ipAddress


class serviceType():
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']

    def __repr__(self):
        return self.name


class service():
    def __init__(self, data):
        for key in data.keys():
            setattr(self, key, data[key])
        self.serviceType = serviceType(data['serviceType'])

    def __repr__(self):
        return self.serviceType.name


class Node():
    def __init__(self, data):
        for key in data.keys():
            setattr(self, key, data[key])
        if data['assetRecord']:
            setattr(self, 'assetRecord', assetRecord(data['assetRecord']))
        if data['categories']:
            setattr(self, 'categories', [id['name'] for id in data['categories']])

    def __repr__(self):
        return self.label
