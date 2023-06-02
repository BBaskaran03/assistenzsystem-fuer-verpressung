import os
import pathlib
import sys
import requests
import json
import time

from requests.auth import HTTPDigestAuth
from requests import Session


def main() -> int:  
    return 0

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded;v=2.0'
}

data = {
    'axis1': '90',
    'axis2': '0',
    'axis3': '0',
    'axis4': '0',
    'axis5': '0',
    'axis6': '0',
    'ccount': '0',
    'inc-mode': 'Large'
}

dataPriv = {
    'privilege': 'modify'
}

dataLocal = {
    'type': 'local'
}

with requests.Session() as session:
    session.auth = requests.auth.HTTPDigestAuth("Default User", "robotics")
    time.sleep(2)
    response = requests.post("http://localhost:80/users?action=set-locale", auth=session.auth, data=dataLocal)
    print(response.status_code)
    time.sleep(2)
    # request write access
    response = requests.post("http://localhost/users/rmmp/", auth=session.auth, headers=headers, data=dataPriv)
    print(response.status_code)
    time.sleep(6)
    #request mastership
    response = requests.post("http://localhost/rw/mastership?action=request", auth=session.auth, headers=headers)
    print(response.status_code)
    # movement
    response = requests.post("http://localhost/rw/motionsystem?action=jog", auth=session.auth, headers=headers, data=data)
    print(response.status_code)
    print(response.text)
    print(response.json)


#def logIn(base_url=, username='Default User', password='robotics'):
#    base_url = base_url
#    username = username
#    password = password
#    session = Session() # create persistent HTTP communication
#    session.auth = HTTPDigestAuth(username, password)

#    print(response.content)



if __name__ == "__main__":
    # Change directory to script location
    os.chdir(pathlib.Path(__file__).parent)

    # Run main()
    sys.exit(main())
