
# Shortcut functions for coding and working with PAN devices   

### Retrieve PAN API key from file in user home directory

  Get API key from .panconfkeystore file in user home directory.  Input file format has one entry per line.  

    <apikey>:<ip>

  Code example

    import retrievepankey
    apikey = retrievepankey.read_key_file("192.168.1.1")    

### Retrieve device info from file in user home directory

  Use shortcut name in scripts to retrieve info about device.

  Will return device 'ip' field by default

  Input file format for 'fetch_deviceinfo_file()' is below.  The function reads in a YAML format from .pandevice file, in user home directory, by default.  All sub fields (serial, ip, type, etc) can be customized and returned.  If there is no match, the input string to the function is returned.      

    DEMOFW1:
      serial: 09870100089
      ip: 192.168.50.100
      type: panos
      panorama: 192.168.100.100
      panorama2: 192.168.100.101
      hapair: 192.168.50.101
    DEMOFW2:
      serial: 098001000597
      ip: 192.168.50.101
      type: panos
      panorama: 192.168.100.100
      panorama2: 192.168.100.101
      hapair: 192.168.50.101

  Code example

    import retrievepankey

    firewallip = retrievepankey.fetch_deviceinfo_file("DEMO-FW")
    panoip = retrievepankey.fetch_deviceinfo_file("DEMO-FW", field='panorama')
