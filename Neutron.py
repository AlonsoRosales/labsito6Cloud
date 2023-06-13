import requests
import json

class NeutronClass(object):
    def __init__(self,UserID,ProjectName,token):
        self.neutron_url = "http://10.20.12.39:9696/v2.0/"
        self.headers = {
            'Content-Type': 'application/json',
            'X-Auth-Token': token
        }
        self.UserID = UserID
        self.ProjectName = ProjectName
        self.NetworkID = None
        
    #Funcion para crear red provider 
    def crearRedProvider(Red, Subred, CIDR, GatewayIP):
        network_data = {
            'network': {
                'name': Red
            }
        }
        response = requests.post(self.neutron_url + 'networks', json=network_data, headers=self.headers)

        if response.status_code == 201: 
            networkID = response.json()['networks']['id']
            self.NetworkID = networkID
            
            subnet_data = {
                'subnet': {
                    'name': Subred,
                    'network_id': self.NetworkID,
                    'cidr': CIDR,
                    'gateway_ip': GatewayIP
                }
            }
            
            response = requests.post(self.neutron_url + 'subnets', json=subnet_data, headers=self.headers)

            if response.status_code == 201:
                print("[*] Red Provider Creada exitosamente\n")
                
            else:
                print("[*] Hubo un problema al crear la Red Provider\n")
            
        else:
           print("[*] Hubo un problema al crear la Red Provider\n")
        
    #Funcion para listar redes 
    def listarRedes(self):
        response = requests.get(self.neutron_url + 'networks', headers=self.headers)

        if response.status_code == 200:
            networks = response.json()['networks']
            print(networks)
            #COMPLETAR
            
        else:
            print("[*] Ha ocurrido un problema al listar las redes\n")
    
    #Funcion para listar grupo de seguridad 
    def listarSecurityGroup(self):
        response = requests.get(self.neutron_url + 'security-groups', headers=self.headers)

        if response.status_code == 200:
            security_groups = response.json()['security_groups']
            print(security_groups)
             #COMPLETAR
             
        else:
            print("[*] Ha ocurrido un problema al listar los security groups\n")
    
    #Funcion para configurar grupo de seguridad
    def configurarSecurityGroup(self):
        pass
        