import os.path
import yaml
import ipaddress


def read_key_file(host, keyfile='.panconfkeystore', splitchar=":", searchpos=0, retpos=1, includehomedir=True):
    if includehomedir == True:
        pathstring = os.path.expanduser('~') + "/" + str(keyfile)
    else:
        pathstring = keyfile
    with open(pathstring) as f:
        for line in f.readlines():
            if line.split(splitchar)[searchpos] == host:
                return line.split(":")[retpos].strip()
    raise Exception("Unable to find firewall in file, exiting now.")


def fetch_deviceinfo_file(fwstr, field='ip', devicemap={}, devicefile='.pandevice', includehomedir=True):
    if includehomedir == True:
        pathstring = os.path.expanduser('~') + "/" + str(devicefile)
    else:
        pathstring = devicefile

    if devicemap == {}:
        try:
            with open(pathstring, "r") as ch:
                devicemap = yaml.safe_load(ch.read())
        except:
            print("Unable to read %s" % devicefile)

    if fwstr in devicemap and field in devicemap[fwstr]:
        fwstr = str(devicemap[fwstr][field])

    if field == 'ip':
        return str(ipaddress.IPv4Address(fwstr))
    else:
        return fwstr
