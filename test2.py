#!/usr/bin/python

from ansible.module_utils.basic import *
import subprocess
import re

def validation(path,pattern,path_stack):
  result_array = []
  file = open(path, 'r')
  file_stack = open(path_stack, 'w')
  for line in file:
      result = re.search(pattern, line)
      if result != None:

          file_stack.write(line)
          result_array.append(line)
          return True

def main():
  module = AnsibleModule(
    argument_spec=dict(
        path=dict(required=True, type='str'),
        path_stack=dict(required=True, type='str'),
        stack_name=dict(required=True, type='str')
    ),
    supports_check_mode=True
  )

  if module.check_mode:
    module.exit_json(changed=False)

  path = module.params['path']
  path_stack = module.params['path_stack']
  stack_name = module.params['stack_name']

  pattern_check_stack_name = "^box\." + stack_name + "\."
  pattern_check_tenant_name = "^TenantName="
  pattern_check_default = "^box\.defaults\."

  if validation(path,pattern_check_stack_name,path_stack):
      msg = "Stack Name defined"
  else:
      msg = "Please ensure that value of variable stack_name is correct and matches with name from stack description in boxes-file and you are correctly set config_file_path variable"
      module.fail_json(failed=True,changed=False,msg=msg)

  if validation(path, pattern_check_tenant_name,path_stack):
      msg = "Tenant Name defined"
  else:
      msg = "Please ensure that there is TenantName described in file and there only one."
      module.fail_json(failed=True, changed=False, msg=msg)

  if validation(path, pattern_check_default,path_stack):
      msg = "default defined"
      module.exit_json(changed=False, msg=msg)
  else:
      msg = "Defaults description shouldn't contain empty parameters, please specify value(s)."
      module.fail_json(failed=True, changed=False, msg=msg)

if __name__ == '__main__':
  main()