from configobj import ConfigObj
import yaml
import re


stream = file('document.yaml', 'w')
config = ConfigObj("boxes.txt",  write_empty_values=True)

yamlfile = dict()
keys = config.viewkeys()

defaults = dict()
stackname = dict()

for i in keys:
    if "TenantName" in i:
        yamlfile = {"tenant": config.get(i)}
    elif "deployCI" in i:
        print i
        for e in re.findall("^\w+.\w+.\w+.(\w+)", i):
            stackname.update({e: config.get(i)})
    elif "defaults" in i:
        for a in re.findall("^\w+.\w+.(\w+)", i):
            defaults.update({a: config.get(i)})

print (defaults)
print (stackname)
yamlfile.setdefault("defaults", []).append(defaults)
yamlfile.setdefault("deployCI", []).append(stackname)


print (yamlfile)
yaml.dump(yamlfile, stream, default_flow_style=False)