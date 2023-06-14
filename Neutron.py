import requests
import json
import random

class NeutronClass(object):
    def __init__(self,UserID,ProjectName,token):
        self.neutron_url = "http://10.20.12.48:9696/v2.0"
        self.token=token
        self.headers = {
            'Content-Type': 'application/json',
            'X-Auth-Token': self.token
        }
        self.UserID = UserID
        self.ProjectName = ProjectName
        self.NetworkID = None
        
        
#Funcion para crear red provider 
    def crearRedProvider(self, red,subred,cidr,gateway):
        print(self.token)
        network_data = {
                "network": {
                "admin_state_up": True,
                "name": red,
                "shared": True,
                "provider:physical_network": "provider",
                "provider:network_type": "vlan",
                "provider:segmentation_id": random.randint(1, 1000)
            }
        }
       
        response = requests.post(self.neutron_url + '/networks', json=network_data, headers=self.headers)

        if response.status_code == 201:
            network_id = response.json()['network']['id']
            print("Network creada existosamente. ID:", network_id)
        else:
            print("Fallo al crear la red. Status code:", response.status_code)

        if response.status_code == 201:
            network_id = response.json()['network']['id']
            
            subnet_data = {
                'subnet': {
                    'network_id': network_id,
                    "ip_version": 4,
                    'cidr': cidr,
                    #'gateway_ip': gateway
                }
            }
            
            response = requests.post(self.neutron_url + 'subnets', json=subnet_data, headers=self.headers)
            print(response.json())
            if response.status_code == 201:
                self.NetworkID = network_id
                print("[*] Red Provider creada exitosamente\n")
            else:
                print("[*] Ha ocurrido un error al crear la redProvider\n")
        else:
            print("[*] Ha ocurrido un error al crear la redProvider\n")
        
    #Funcion para listar redes 
    def listarRedes(self):
        response = requests.get(self.neutron_url + 'networks', headers=self.headers)

        if response.status_code == 200:
            networks = response.json()['networks']
            print(networks)
            #COMPLETAR
            
        else:
            print("[*] Ha ocurrido un problema al listar las redes\n")
    
   
        