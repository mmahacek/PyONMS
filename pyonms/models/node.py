# models.node.py


class assetRecord:
    def __init__(self, data):
        for key, value in data.items():
            setattr(self, key, value)

    # def __repr__(self):
    #    return self.label


class snmpInterface:
    def __init__(self, data: dict):
        for key, value in data.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"< SnmpInterface {self.id}: {self.ifAlias} >"


class ipInterface:
    def __init__(self, data: dict):
        for key, value in data.items():
            setattr(self, key, value)
            if key == "id":
                self.id = int(value)
        if data.get("snmpInterface"):
            self.snmpInterface = snmpInterface(data["snmpInterface"])

    def __repr__(self):
        return f"< IP {self.id}: {self.ipAddress} >"


class serviceType:
    def __init__(self, data: dict):
        self.id = data["id"]
        self.name = data["name"]

    def __repr__(self):
        return f"< ServiceType {self.id}: {self.name} >"


class service:
    def __init__(self, data: dict):
        for key, value in data.items():
            setattr(self, key, value)
        self.serviceType = serviceType(data["serviceType"])

    def __repr__(self):
        return f"< Service {self.id}: {self.name} >"


class metadata:
    def __init__(self, context: str, key: str, value: str):
        self.context = context
        self.key = key
        self.value = value

    def __repr__(self):
        return f"< Metadata: {self.context}:{self.key}:{self.value} >"


class Node:
    def __init__(self, data: dict):
        for key, value in data.items():
            setattr(self, key, value)
            if key == "id":
                self.id = int(value)
        if data["assetRecord"]:
            self.assetRecord = assetRecord(data["assetRecord"])
        if data["categories"]:
            self.categories = [id["name"] for id in data["categories"]]

    def __repr__(self):
        return f"< Node {self.id}: {self.label} >"
