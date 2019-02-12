from configobj import ConfigObj
from validate import Validator
import yaml, sys
import re

stack = "deploy"
stream = file('boxes.yaml', 'w')

configspec = ConfigObj("configspec.ini", interpolation=False, list_values=False, _inspec=True)
config = ConfigObj("boxes.txt", configspec=configspec, write_empty_values=False)

validator = Validator()
result = config.validate(validator)

if result != True:
    print 'Config file validation failed!'
    sys.exit(1)

keys = config.viewkeys()

yamlfile = dict()
defaults = dict()
stackname = dict()
volumes = dict()
volumes_defaults = dict()
values = dict()

tenant = list()
node = list()

def grepDefaultsValue():
    for i in keys:
       if ".defaults." in re.findall("[.]defaults[.]", i):
            for key in re.findall("^\w+.\w+.(\w+)", i):
                if key.find("volume") != -1:
                    for key_volume in re.findall("^\w+.\w+.\w+.(\w+)", i):
                        try:
                            volumes_defaults[key].update({key_volume: config.get(i)})
                        except KeyError:
                            volumes_defaults[key] = {}
                            volumes_defaults[key].update({key_volume: config.get(i)})
                else:
                    defaults.update({key: config.get(i)})

def grepNodeNameAndTenant():
    for i in keys:
        if "." + stack + "." in re.findall("[.]" + stack + "[.]", i):
            for key in re.findall("^\w+.\w+.(\w+)", i):
                if key in node:
                    pass
                else:
                    node.append(key)
        elif "TenantName" in i:
            if config.get(i) in tenant:
                pass
            else:
                tenant.append(config.get(i))

def grepValuesForNode():
    for nodename in node:
        for i in keys:
            if i.find(nodename) != -1:
                for key in re.findall("^\w+.\w+.\w+.(\w+)", i):
                    if key.find("volume") != -1:
                        for key_volume in re.findall("^\w+.\w+.\w+.\w+.(\w+)", i):
                            try:
                                volumes[key].update({key_volume: config.get(i)})
                            except KeyError:
                                volumes[key] = {}
                                volumes[key].update({key_volume: config.get(i)})
                    else:
                        values.update({key: config.get(i)})

        if values.__len__() > 0:
            try:
                stackname[nodename].update(values.items())
            except KeyError:
                stackname[nodename] = {}
                stackname[nodename].update(values.items())
        if volumes.__len__() > 0:
            try:
                stackname[nodename]["volumes"].update(volumes.items())
            except KeyError:
                stackname[nodename]["volumes"] = {}
                stackname[nodename]["volumes"].update(volumes.items())
            volumes.clear()

grepDefaultsValue()
grepNodeNameAndTenant()
grepValuesForNode()

yamlfile["defaults"] = {}
yamlfile["defaults"].update(defaults.items())
yamlfile["defaults"]["volumes"] = {}
for i in volumes_defaults:
    yamlfile["defaults"]["volumes"][i] = {}
    yamlfile["defaults"]["volumes"][i].update(volumes_defaults[i].items())
yaml.dump({"tenant": tenant[0]}, stream, default_flow_style=False)
yaml.dump(yamlfile, stream, default_flow_style=False)
yaml.dump({stack: stackname}, stream, default_flow_style=False)