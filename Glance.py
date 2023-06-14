import requests
import json

class GlanceClass(object):
    def __init__(self,UserID,ProjectName,token):
        self.glance_url = "http://10.20.12.48:9292/v2"
        self.headers = { 'Content-Type': 'application/json','X-Auth-Token': token }
        self.UserID = UserID
        self.ProjectName = ProjectName
        
    #Funcion para listar imagenes 
    def listarImagenes(self):
        url = f"{self.glance_url}/images"
        response = requests.get(url, headers=self.headers)
        listado=[]

        if response.status_code == 200:
            imagenes = response.json().get('images', [])
            for imagen in imagenes:
                listado.append([imagen['name'],imagen['id']])
            return listado
           
            
        else:
             print("[*] Ha ocurrido un error al listar las imagenes\n")
    
    def obtenerDetallesImagen(self, image_id):
        
        url = f"{self.glance_url}/images/{image_id}"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
    
            
            image_name = response.json().get('name', '')
            image_size = response.json().get('size', '')
            image_status = response.json().get('status', '')

            print("Detalles de la Imagen:")
            print("     Nombre:", image_name)
            print("     Tamaño:", image_size)
            print("     Estado:", image_status)
        else:
            print("Error al obtener los detalles de la Imagen:", response.status_code)