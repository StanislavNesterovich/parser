from configobj import ConfigObj
import yaml
import re

stream = file('document.yaml', 'w')
config = ConfigObj("boxes.txt", write_empty_values=False)

yamlfile = dict()
keys = config.viewkeys()

defaults = dict(); stackname = dict(); volumes = dict();  volumes_defaults = dict(); values = dict()
tenant = list()
node = list()

def grepDefaultsValue():
    for i in keys:
       if  "defaults" in i:
            for key in re.findall("^\w+.\w+.(\w+)", i):
                if key.find("volume") != -1:
                    for key2 in re.findall("^\w+.\w+.\w+.(\w+)", i):
                        try:
                            volumes_defaults[key].update({key2:config.get(i)})
                        except KeyError:
                            volumes_defaults[key] = {}
                            volumes_defaults[key].update({key2:config.get(i)})
                        #volumes_defaults.setdefault(key, []).append({key2: config.get(i)})
                else:
                    defaults.update({key: config.get(i)})

def grepNodeNameAndTenant():
    for i in keys:
        if "deployCI" in i:
            for key in re.findall("^\w+.\w+.(\w+)", i):
                if key in node:
                    pass
                else:
                    node.append(key)
        elif "TenantName" in i:
            if config.get(i) in tenant:
                print "two TenantName in config"
            else:
                tenant.append(config.get(i))

def grepValuesForNode():
    for nodename in node:
        for i in keys:
            if i.find(nodename) != -1:
                for key in re.findall("^\w+.\w+.\w+.(\w+)", i):
                    if key.find("volume") != -1:
                        for key2 in re.findall("^\w+.\w+.\w+.\w+.(\w+)", i):
                            try:
                                volumes[key].update({key2: config.get(i)})
                            except KeyError:
                                volumes[key] = {}
                                volumes[key].update({key2: config.get(i)})
                    else:
                        values.update({key: config.get(i)})

        if values.__len__() > 0:
            try:
                stackname[nodename].update(values.items())
            except KeyError:
                stackname[nodename] = {}
                stackname[nodename].update(values.items())
        else:
            pass
        if volumes.__len__() > 0:
            try:
                stackname[nodename]["volumes"].update(volumes.items())
            except KeyError:
                stackname[nodename]["volumes"] = {}
                stackname[nodename]["volumes"].update(volumes.items())
            volumes.clear()
        else:
            pass

grepDefaultsValue()
grepNodeNameAndTenant()
grepValuesForNode()


yamlfile["defaults"] = {}
yamlfile["defaults"].update(defaults.items())
yamlfile["defaults"]["volumes"] = {}

for i in volumes_defaults:
    yamlfile["defaults"]["volumes"][i] = {}
    #volumes_defaults.setdefault(key, []).append({key2: config.get(i)})
    #yamlfile["defaults"]["volumes"].setdefault(i,[].append(volumes_defaults[i].items()))
    yamlfile["defaults"]["volumes"][i].update(volumes_defaults[i].items())

yaml.dump({"tenant": tenant[0]},stream, default_flow_style=False)
#yaml.dump({"defaults":defaults},stream, default_flow_style=False)
yaml.dump(yamlfile, stream, default_flow_style=False)
yaml.dump({"deployCI": stackname}, stream, default_flow_style=False)