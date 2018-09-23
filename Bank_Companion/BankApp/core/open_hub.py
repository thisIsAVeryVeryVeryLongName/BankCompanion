import requests

class OpenHub:

    TOKEN = ""    

    def connect(self):
        r=requests.post('http://tourism.opendatahub.bz.it/api/LoginApi',json={"username": "tourism@hackthealps.it","pswd": "$h4cKth34lpS"})
        if(r.status_code!=200):
            print(r.status_code)
        global TOKEN
        TOKEN=r.json()['access_token']

    def get_token(self):
        global TOKEN
        return TOKEN

    def get_gastronomy_reduced(self):
        global TOKEN
        r=requests.get('http://tourism.opendatahub.bz.it/api/GastronomyReduced',headers={"Authorization": "Bearer "+TOKEN})
        return r.json()


