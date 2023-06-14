from getpass import getpass
from Keystone import KeystoneClass
from Neutron import NeutronClass
from Nova import NovaClass
from Glance import GlanceClass

#Funciones
def crearProviderNetwork(Neutron):
    nombreRed = input("| Ingrese el nombre de la red: ")
    nombreSubred = input("| Ingrese el nombre de la subred: ")
    CIDR = input("| Ingrese el CIDR de la red: ")
    GatewayIP = input("| Ingrese la IP del Gateway: ")
    Neutron.crearRedProvider(nombreRed, nombreSubred, CIDR, GatewayIP) 

def crearKeyPair(Nova):
    nombreLlave= input("| Ingrese el nombre de la llave: ")
    rutaLlave = input("| Ingrese la ruta en el equipo de la llave pública: ")
    Nova.crearLLave(nombreLlave, rutaLlave)

#Funcion que permite configurar un SecurityGroup
def configurarGrupoSeguridad(nova):
    while True:
        print("|------------------------------------|")
        print("|1. Crear otro grupo de seguridad    |")
        print("|2. Añadir regla de seguridad        |")
        print("|3. Salir                            |")
        print("|------------------------------------|")
        opcion = input("| Ingrese una opción: ")
        if opcion == "1":
            nombre = input("| Ingrese un nombre: ")
            description = input("| Ingrese una description: ")
            Nova.crearSecurityGroup(nombre,description)
        elif opcion == "2":
            print("Selecciona uno de los security groups")
            Nova.listarSecurityGroup()
            nombre_security = input("| Ingrese el nombre del security group: ")
            protocol_ip= input("| Ingrese el Protocolo (tcp/udp/icmp): ")
            if protocol_ip=='icmp':
                from_port=0
                dest_port=8
            else:
                from_port= input("| Ingrese el nombre del Puerto: ")
                dest_port= input("| Ingrese el nombre del Puerto de destino: ")


            cidr= input("| Ingrese el CIDR: ")
            Nova.agregarRegla(nombre_security,protocol_ip,from_port,dest_port,cidr)
        elif opcion == "3":
            print("Saliendo...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

#Funcion que permite obtener el ID de un Flavor   
def getFlavorsID(nova):
    listado = nova.listarFlavors()
    while True:
        print("|--------------------Lista de Flavors------------------------|")
        i = 0
        for flavor in listado:
            flavor_details = flavor[0][0]  # Obtiene los detalles del flavor de la sublista
            flavor_name = flavor_details[0]
            flavor_vcpus = flavor_details[1]
            flavor_ram = flavor_details[2]
            flavor_disk = flavor_details[3]

            print("|- Flavor "+str(i+1)+" -> "+str(flavor_name)+"| RAM: "+ str(flavor_vcpus)+ "   | DISK: "+ str(flavor_ram)+" | VCPUS: "+ str(flavor_disk))
            i = i + 1
        print("|--------------------------------------------------------------|")
        opcionFlavor = int(input("| Ingrese el # del flavor que desea usar: "))
        if opcionFlavor > len(listado):
            print("[*] Ingrese el # de un flavor válido\n")
        else:
            idFlavor = listado[int(opcionFlavor)-1][1]
            break
    return idFlavor

#Funcion que permite obtener el ID de una Imagen
def getImagenesID(glance):   
    listado = glance.listarImagenes() 
    while True:
        print("|--------------------Lista de Imagenes------------------------|")
        i = 0
        for imagen in listado:
            print("|- Imagen "+str(i+1)+" -> "+str(imagen[0]))
            i = i + 1
        print("|--------------------------------------------------------------|")
        opcionImagen = int(input("| Ingrese el # de la imagen que desea usar: "))
        if opcionImagen > len(listado):
            print("[*] Ingrese el # de una imagen válida\n")
        else:
            idImagen = listado[int(opcionImagen)-1][1]

            break
    return idImagen

#Funcion que permite obtener el ID de una red
def getRedID(Neutron):
    listado = Neutron.listarRedes()

    while True:
        print("|--------------------Lista de Redes------------------------|")
        i = 0
        for red in listado:
            print("|- Red "+str(i+1)+" -> "+str(red[0]) + "  |  CIDR -> "+ str(red[1]))
            i = i + 1
        print("|--------------------------------------------------------------|")
        opcionImagen = int(input("| Ingrese el # de la red que desea usar: "))
        if opcionImagen > len(listado):
            print("[*] Ingrese el # de una red válida\n")
        else:
            idImagen = listado[int(opcionImagen)-1][2]

            break
    return idImagen

#Funcion que permite obtener el ID de una keypair
def getKeyPairID(nova,keystone):
    listado = nova.listarKeyPair()
    while True:
        print("\n|-----------------------------------------------------|")
        i = 1
        for key in listado:
            print("| KeyPair "+str(i)+": "+str(key)+ "  |")
            i = i + 1
        print("|-----------------------------------------------------|")
        opcionKeyPair = int(input("| Ingrese el # de la keypair que desea usar: "))
        if opcionKeyPair > len(listado):
            print("[*] Ingrese el # de una keypair válida\n")
        else:
            keypair = listado[int(opcionKeyPair)-1]

            break

    return keypair

#Funcion que permite obtener el ID de un SecurityGroup
def getSecurityGroupID(nova):
    listado = nova.listarSecurityGroup()
    while True:
        print("\n|-----------------------------------------------------|")
        for SG in listado:
            print("| SecurityGroup "+str(SG[0])+" |  Descripcion : "+str(str(SG[1]))+ "  |")
        print("|-----------------------------------------------------|")    
        opcionSecurityGroup = int(input("| Ingrese el # del securitygroup que desea usar: "))
        if opcionSecurityGroup > len(listado):
            print("[*] Ingrese el # de un securitygroup válido\n")
        else:
            securitygroup = listado[int(opcionSecurityGroup)-1][0]
            break
    return securitygroup

def crearVM(Neutron, Nova, Glance, username):
    nombreVM = input("| Ingrese el nombre de la VM: ")
    print("\n")
    flavorID = getFlavorsID(Nova)
    print("\n")

    imagenID = getImagenesID(Glance)
    print("\n")

    redID = getRedID(Neutron)
    print("\n")

    llave = getKeyPairID(Nova,Keystone)
    print("\n")

    securityGroup = getSecurityGroupID(Nova)
    print("\n")
    Nova.crearVM(nombreVM,flavorID,imagenID,redID,llave,securityGroup)


def listarVMs(Nova):
    Nova.listarVMs()

def  Menu(Neutron, Nova, Glance, username):
    while True:
        print("|- Opción 1 -> Crear provider network            |")
        print("|- Opción 2 -> Crear keypair                     |")
        print("|- Opción 3 -> Crear o editar grupo de seguridad |")
        print("|- Opción 4 -> Crear VM                          |")
        print("|- Opción 5 -> Listar VMs                        |")
        print("|- Opcion 6 -> Salir                             |")
        opcion = input("| Ingrese una opción: ")

        if int(opcion) == 1:
            crearProviderNetwork(Neutron)
            
        elif int(opcion) == 2:
            crearKeyPair(Nova)
        
        elif int(opcion) == 3:
            configurarGrupoSeguridad(Nova)
            
        elif int(opcion) == 4:
            crearVM(Neutron, Nova, Glance,username)
            
        elif int(opcion) == 5:
            listarVMs(Nova)
            
        elif int(opcion) == 6:
            break
            
        else:
            print("[*] Ha ingresado una opción incorrecta\n")    
           
#Main
while True:
    username = input("| Ingrese su nombre de usuario: ")
    password = getpass("| Ingrese su contraseña: ")

    if ((username != "") and (password != "")):
        Keystone = KeystoneClass(username,password)
        acceso = Keystone.Token() 
             
        if acceso == 1:
            Neutron = NeutronClass(Keystone.getUserID(),Keystone.getProjectName(),Keystone.getToken())
            Nova = NovaClass(Keystone.getUserID(),Keystone.getProjectName(),Keystone.getToken())
            Glance = GlanceClass(Keystone.getUserID(),Keystone.getProjectName(),Keystone.getToken())
            
            print("[*] Login exitoso\n")
            Menu(Neutron, Nova, Glance,username)
            break
            
        else:
            print("[*] Credenciales incorrectas\n")      
        
    else:
        print("[*] Credenciales incorrectas\n")   
        
print("[*] Fin de la aplicación\n")