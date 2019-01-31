#!/usr/bin/python
from ansible.module_utils.basic import *
from configobj import ConfigObj
import yaml
import re

defaults = dict(); stackname = dict(); volumes = dict();  volumes_defaults = dict(); values = dict()
tenant = list()
node = list()

def grepDefaultsValue(keys,config):
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
                else:
                    defaults.update({key: config.get(i)})

def grepNodeNameAndTenant(keys,config):
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

def grepValuesForNode(keys,config):
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
        if volumes.__len__() > 0:
            try:
                stackname[nodename]["volumes"].update(volumes.items())
            except KeyError:
                stackname[nodename]["volumes"] = {}
                stackname[nodename]["volumes"].update(volumes.items())
            volumes.clear()

def conver(path,path_yaml):
    stream = file(path_yaml, 'w')
    config = ConfigObj(path, write_empty_values=False)
    yamlfile = dict()
    keys = config.viewkeys()

    grepDefaultsValue(keys,config)
    grepNodeNameAndTenant(keys, config)
    grepValuesForNode(keys,config)

    yamlfile["defaults"] = {}
    yamlfile["defaults"].update(defaults.items())
    for i in volumes_defaults:
        yamlfile["defaults"]["volumes"][i] = {}
        if volumes_defaults[i].__len__() > 0:
            yamlfile["defaults"]["volumes"] = {}
            yamlfile["defaults"]["volumes"][i].update(volumes_defaults[i].items())

    yaml.dump({"tenant": tenant[0]},stream, default_flow_style=False)
    yaml.dump(yamlfile, stream, default_flow_style=False)
    yaml.dump({"deployCI": stackname}, stream, default_flow_style=False)
    return True

def main():
  module = AnsibleModule(
    argument_spec=dict(
        path=dict(required=True, type='str'),
        path_yaml=dict(required=True, type='str'),
        stack_name=dict(required=True, type='str')
    ),
    supports_check_mode=True
  )
  if module.check_mode:
    module.exit_json(changed=False)

  path = module.params['path']
  stack_name = module.params['stack_name']
  path_yaml = module.params['path_yaml']

  if conver(path,path_yaml):
      msg = "box succesefull convert"
      module.exit_json(changed=False, msg=msg)
  else:
      msg = "error convert"
      module.fail_json(failed=True,changed=False,msg=msg)

if __name__ == '__main__':
  main()