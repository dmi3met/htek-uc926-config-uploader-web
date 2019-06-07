import requests
import base64
import re

ip = '172.16.0.100'
url = 'http://'+ip
user = 'admin'
password = 'admin'

credentials64 = base64.b64encode(bytes('%s : %s' % (user, password),
                                       'utf-8')).decode('ascii')
headers = {'Authorization': 'Basic %s' % credentials64}

with requests.Session() as session:
    r = session.get(url+'/index.htm', headers=headers)

    mac_address = re.findall(r'..:..:..:..:..:..', r.text)[0]
    print(mac_address)
    mac_with_minus = re.sub(':', '-', mac_address)

    config_filename = '%s.xml' % mac_with_minus
    with open(config_filename, 'rb') as f:
        r = session.post(url+'/HLCFG_XML_configuration.htm',
                         headers=headers, files={config_filename: f})
        print(r)
