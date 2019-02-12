import pysftp

myHostname = "ftpcn.netcracker.com"
myUsername = "seko0313"
myPassword = "wup69tyUb"
path = "MANO_DVM_Release_10.1_rc004_6.tar.gz"
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword,cnopts=cnopts) as sftp:

        sftp.cwd('/Corp/SandboxBS.Builds/Release/product/prod.inmrnd.mano/deployment-vm/release_10.1_20190131-102258/generic1.0/')
        print sftp.listdir_attr()
        a = sftp.sftp_client.stat(path)
        print a.st_size
