import requests
import json

class NovaClass(object):
    def __init__(self,UserID,ProjectName,token):
        self.nova_url = "http://10.20.12.48:8774/v2.1"
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
    def crearVM(self,nombreVM,flavor,imagen,red,llave,securityGroup):
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
    def listarVMs(self):
        response = requests.get(self.nova_url + '/servers', headers=self.headers)

        if response.status_code == 200:
            print(response.json()['servers'])
            print("[*] Instancias listadas correctamente\n")
            
        else:
            print("[*] Ha ocurrido un error al listar las VMS\n")
    
#Funcion para crear la keypair
    def crearLLave(self,nombreLlave, rutaLlave):
        keypair_data = {
            'keypair': {
                'name': nombreLlave,
                #'type':'ssh'
            }
        }
        response = requests.post(self.nova_url + '/os-keypairs', json=keypair_data, headers=self.headers)

        if response.status_code == 200:
            keypair = response.json().get('keypair', {})
            public_key = keypair.get('public_key', '')

            if public_key:
                # Guardar la llave pública en el archivo
                with open(rutaLlave, 'w') as f:
                    f.write(public_key)
                print("Keypair creada exitosamente. La llave pública se ha guardado en:", rutaLlave)
            else:
                print("La respuesta de la API no contiene la llave pública.")
        else:
            print("Error al crear el keypair:", response.status_code)

            
    
#Listar keypairs
    def listarKeyPair(self, user):
        url = f"{self.nova_url}/os-keypairs"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            keypairs = response.json().get('keypairs', [])
            if len(keypairs) == 0:
                print("No cuenta con ninguna keypair, por favor cree una")
                return None
            else:
                keypair_names = []
                for keypair in keypairs:
                    keypair_name = keypair['keypair']['name']
                    info = self.infoKeyPair(keypair_name, user)
                    if info[5] == user:
                        keypair_names.append(keypair_name)

                if len(keypair_names) == 0:
                    print("No se encontraron keypairs para el usuario:", user)
                else:
                    print("Keypairs del usuario", user, ":")
                    for name in keypair_names:
                        print("- Nombre del Keypair:", name)

                return keypair_names
        else:
            print("Error al listar los Keypairs:", response.status_code)

#Crear securitygroup
    def crearSecurityGroup(self,name,descripcion):
        url = f"{self.nova_url}/os-security-groups"
        data = {
            'security_group': {
                'name': name,
                'description': descripcion
            }
        }

        response = requests.post(url, json=data, headers=self.headers_security)

        if response.status_code == 200:
            security_group = response.json().get('security_group', {})
            print("Grupo de seguridad creado exitosamente:", security_group['name'])
        else:
            print("Error al crear el Grupo de seguridad:", response.status_code)

#Listar securitygroup
    def listarSecurityGroup(self):
    
        url = f"{self.nova_url}/os-security-groups"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            security_groups = response.json().get('security_groups', [])
            print("Lista de Grupos de Seguridad:")
            lista_sg = []
            for index,sg in enumerate(security_groups):
                print(f"{index + 1}. Nombre: {sg['name']}")
                print("   Descripción:", sg['description'])
                #print("ID:", sg['id'])
                print("----------")
                lista_sg.append([sg['name'], sg['description']])
            return lista_sg
        else:
            print("Error al listar los Grupos de Seguridad:", response.status_code)

#Agregar regla
    def agregarRegla(self,nombre,protocol_ip,from_port,dest_port,cidr):
        
        id_security=self.obtenerIDSecurityGroup(nombre)

        url = f"{self.nova_url}/v2.1/os-security-group-rules"
        data = {
            'security_group_rule': {
                'parent_group_id': id_security,
                'ip_protocol': protocol_ip,
                'from_port': from_port,
                'to_port': dest_port,
                'cidr': cidr
            }
        }
        response = requests.post(url, json=data, headers=self.headers_security_rule)
        if response.status_code == 200:
            security_group_rule = response.json().get('security_group_rule', {})
            print("Regla de seguridad agregada exitosamente:")
            print("Nombre del grupo de seguridad:", nombre)
            print("Protocolo:", security_group_rule['ip_protocol'])
            print("Puerto origen:", security_group_rule['from_port'])
            print("Puerto destino:", security_group_rule['to_port'])
            print("CIDR:", security_group_rule['ip_range']['cidr'])
        else:
            print("Error al agregar la regla de seguridad:", response.status_code)

#Obtener ID de securitygroup
    def obtenerIDSecurityGroup(self,securitygroup):
        url = f"{self.nova_url}/v2.1/os-security-groups"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            security_groups = response.json().get('security_groups', [])
            for sg in security_groups:
                if sg['name'] == securitygroup:
                    print("ID del Grupo de seguridad:", sg['id'])
                    return sg['id']
            #print("No se encontró el Grupo de seguridad especificado")
            return None
        else:
            print("Error al obtener el ID del Grupo de seguridad:", response.status_code)