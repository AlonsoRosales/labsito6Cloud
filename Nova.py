import requests
import json

class NovaClass(object):
    def __init__(self,UserID,ProjectName,token):
        self.nova_url = "http://10.20.12.39:8774/"
        self.headers = {
            'Content-Type': 'application/json',
            'X-Auth-Token': token
        }
        self.UserID = UserID
        self.ProjectName = ProjectName
        
    #Funcion para listar flavors
    def listarFlavors(self):
        response = requests.get(self.nova_url + '/flavors', headers=self.headers)
        if response.status_code == 200:
            flavors = response.json()['flavors']
            print(flavors)
            print("[*] Flavors listados correctamente\n")
            
        else:
            print("[*] Ha ocurrido un error al listar los flavors\n")
    
    #Funcion para crear VM
    def crearVM(nombreVM,flavor,imagen,red,llave,securityGroup):
        instance_data = {
            'server': {
                'name': nombreVM,
                'flavorRef': flavor,
                'imageRef': imagen,
                'key_name': llave,
                "security_groups": [
                    {
                    "name": securityGroup
                    }
                ],
                'networks': [
                    {'uuid': red}
                ]
            }
        }
        response = requests.post(self.nova_url + '/servers', json=instance_data, headers=self.headers)

        if response.status_code == 202:
            print("[*] VM creada exitosamente\n")
            
        else:
            print("[*] Ha ocurrido un error al crear la VM\n")
    
    #Funcion listar VMs
    def listarVMs():
        response = requests.get(self.nova_url + '/servers', headers=self.headers)

        if response.status_code == 200:
            print(response.json()['servers'])
            instances = response.json()['servers']
            print(instances)
            print("[*] Instancias listadas correctamente\n")
            
        else:
            print("[*] Ha ocurrido un error al listar las VMS\n")
    
    #Funcion para crear la keypair
    def crearLLave(nombreLlave, rutaLlave):
        keypair = {
            'keypair': {
                'name': nombreLlave,
                'type': "ssh",
                'public_key': rutaLlave #VERIFICAR
            }
        }
        response = requests.post(self.nova_url + '/os-keypairs', json=keypair, headers=self.headers)

        if response.status_code == 201:
            print("[*] KeyPair creada exitosamente\n")
            
        else:
            print("[*] Ha ocurrido un problema al crear la keypair\n")
            
    
    #Funcion para listar keypair 
    def listarKeyPair(self):
        response = requests.post(self.nova_url + '/os-keypairs', json=keypair, headers=self.headers)

        if response.status_code == 201:
            keypairs =  response.json()['keypairs']
            #COMPLETAR
            
        else:
            print("[*] Ha ocurrido un problema al listar las keypairs\n")