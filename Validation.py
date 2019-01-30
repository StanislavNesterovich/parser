from jsonschema import validate
from cerberus import Validator
import yaml


def __load_doc():
    with open("document.yaml", 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exception:
            raise exception

schema = eval(open('schema', 'r').read())
v = Validator(schema)
doc = __load_doc()
print v.validate(doc, schema)
print v.errors