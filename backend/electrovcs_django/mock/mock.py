#!/usr/binenv python
import requests
from requests.auth import HTTPBasicAuth
import getpass
import json

"""
user = "doutriaux1"
passwd = getpass.getpass()
s = requests.session()
r = s.get('http://localhost:8000/django-pam/login/', auth=HTTPBasicAuth(user, passwd))
csrf = s.cookies["csrftoken"]

payload = {"csrfmiddlewaretoken" : csrf}
r = s.post('http://localhost:8000/django-pam/login/', auth=HTTPBasicAuth(user, passwd), data = payload)
print r.raw.read()
"""

script = "import vcs\nx=vcs.init()\nx.plot([1,2,3,4,3,2,1])"
r = requests.post('http://localhost:8000/viz/new/',data= {'name':"testit",'script':json.dumps(script), 'user':'doutriaux1'})
r = requests.post('http://localhost:8000/viz/run/',data= {'name':"testit", 'user':'doutriaux1'})

print r.raw.read()
