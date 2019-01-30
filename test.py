from configobj import ConfigObj
import yaml
values = {'ip': '10.103.0.60', 'keypair': 'tmp_key', 'image_name': 'rhel7.2', 'flavor': 'IaaS.Vcpu_4.ram_6', 'internal_network_name': 'inner-net_NC_ENG_IT_DPL'}
volumes = {'volume1': [{'volume_type': 'ceph_nc_eng_it_dpl'}, {'mount_point': '/dev/vdb'}, {'size': '5'}], 'volume2': [{'volume_type': 'ceph_nc_eng_it_dpl'}, {'mount_point': '/dev/vdb'}, {'size': '6'}]}

stream = file('streem.yaml', 'w')

stackname = dict()


stackname.update({"instance1": volumes})
stackname.update({"instance1": values})


print stackname.values()
yamlfile = dict()
yamlfile.setdefault("deployCI",[]).append(stackname)




yaml.dump(yamlfile, stream, default_flow_style=False)