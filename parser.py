from configobj import ConfigObj
import collections
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
                        volumes_defaults.setdefault(key, []).append({key2: config.get(i)})
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
                            volumes.setdefault(key, []).append({key2: config.get(i)})
                    else:
                        values.update({key: config.get(i)})


                           # print key2
                            # values.setdefault()


        if values.__len__() > 0:
            print values.values()
            stackname.setdefault(nodename, []).append(values.copy())
            values.clear()
        else:
            pass

        if volumes.__len__() > 0:
            stackname.setdefault(nodename, []).append(volumes.copy())
            volumes.clear()
        else:
            pass





# for i in keys:
#     if "TenantName" in i:
#         yamlfile = {"tenant": config.get(i)}
#     elif "deployCI" in i:
#         for key in re.findall("^\w+.\w+.(\w+)", i):
#             node.setdefault(key,[])
#             if key.find("instance1") != -1:
#                 for key3 in re.findall("^\w+.\w+.\w+.\w+.(\w+)", i):
#                     pass
#                 for key in re.findall("^\w+.\w+.\w+.(\w+)", i):
#                     if key.find("volume") != -1:
#                         for key2 in re.findall("^\w+.\w+.\w+.\w+.(\w+)",i):
#                             volumes.setdefault(key,[]).append({key2:config.get(i)})
#                     else:
#                         for e in re.findall("^\w+.\w+.\w+.(\w+)", i):
#                             stackname.update({e: config.get(i)})



grepDefaultsValue()
grepNodeNameAndTenant()
grepValuesForNode()

yamlfile.update({"tenant": tenant[0]})
yamlfile.setdefault("deployCI",[]).append(stackname)
yamlfile.setdefault("defaults", []).append(defaults)
yamlfile.setdefault("defaults", []).append(volumes_defaults)



yaml.dump(yamlfile, stream, default_flow_style=False)