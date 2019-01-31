from cerberus import Validator
import yaml


to_bool = lambda v: v.lower() in ('true', '1')

print to_bool
v.schema = {'flag': {'type': 'boolean', 'coerce': (str, to_bool)}}
v.validate({'flag': 'true'})