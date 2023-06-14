import requests
import json

class GlanceClass(object):
    def __init__(self,UserID,ProjectName,token):
        self.glance_url = "http://10.20.12.48:9292/v2.1"
        self.headers = { 'Content-Type': 'application/json','X-Auth-Token': token }
        self.UserID = UserID
        self.ProjectName = ProjectName
        
    #Funcion para listar imagenes 
    def listarImagenes(self):
        url = f"{self.glance_url}/images"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            imagenes = response.json().get('images', [])
            print(imagenes)
            print("[*] Imagenes listadas correctamente\n")
            
        else:
             print("[*] Ha ocurrido un error al listar las imagenes\n")
        