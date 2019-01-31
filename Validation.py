from cerberus import Validator
import yaml

with open('schema.yaml', 'r') as f:
    style = yaml.load(f)

def oddity(field, value, error):
    if not value & 1:
        error(field, "Must be an odd number")


def load_doc():
    with open("document.yaml", 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exception:
            raise exception

schema = eval(open('schema', 'r').read())

valid = Validator(style)
doc = load_doc()

print valid.validate(doc, style)
print valid.errors