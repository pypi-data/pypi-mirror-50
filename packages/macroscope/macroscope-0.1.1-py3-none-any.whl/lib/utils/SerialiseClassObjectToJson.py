# Standard library
import json


class SerialiseClassObjectToJson:
    # TODO: remove items that are None
    """JSON serializer for objects not serializable by default json code"""
    def __init__(self, obj):
        self.obj = obj
        self.json = json.dumps(self.obj, default=self.__serialise, indent=4)

    def __serialise(self, obj):
        return obj.__dict__


def printObjAsJson(obj):
    serialiser = SerialiseClassObjectToJson(obj)

    print(serialiser.json)
