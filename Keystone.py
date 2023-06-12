import requests
import json

class KeystoneClass(object):
    def __init__(self,username, password):
        self.auth_url = "http://10.20.12.39:5000/v3"
        self.username = username
        self.password = password
        self.token = None
        self.headers = {'Content-Type': 'application/json'}
        self.UserID = None
        self.ProjectName = "tel141"
        
    def getToken(self):
        return self.token
         
    def getUserID(self):
        return self.UserID
    
    def setUserID(self,UserID):
        self.UserID = UserID
    
    def getProjectName(self):
        return self.ProjectName
         
    #Funcion para obtener y setear el token 
    def Token(self):
        auth_data = {
            'auth': {
                'identity': {
                    'methods': ['password'],
                    'password': {
                        'user': {
                            'name': self.username, 
                            'password': self.password, 
                            'domain': {'id': 'default'}
                        }
                    }
                },
                "scope": {
                    "project": {
                        "domain": {
                            "id": "default"
                        },
                        "name": self.ProjectName
                    }
                }
            }
        }
        
        response = requests.post(self.auth_url+"/auth/tokens",
                                 json=auth_data,
                                 headers=self.headers)

        if response.status_code == 201:
            self.token = response.headers['X-Subject-Token']
            self.UserID = response.json()["token"]["user"]['id']
            return 1
            
        else:
            return 0
