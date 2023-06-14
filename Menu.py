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
        list_sg=Nova.listarSecurityGroup()
        print("|------------------------------------|")
        print("|1. Añadir Regla                     |")
        print("|2. Elimnar Regla                    |")
        print("|4. Crear otro grupo de seguridad    |")
        print("|3. Salir                            |")
        print("|------------------------------------|")
        opcion = input("| Ingrese una opción: ")
        if int(opcion) == 1:
            while True:
                nombre = input("| Ingrese un nombre de securitygroup: ")
                if(nombre != ''):
                    if(nombre == "ESC"):
                        print("[*] Ha salido de la opción de -Añadir Regla-\n")
                        return
                    while True:
                        protocol_ip = input("| Ingrese el protocolo IP: ")
                        if(protocol_ip != ''):
                            if(protocol_ip == "ESC"):
                                print("[*] Ha salido de la opción de -Añadir Regla-\n")
                                return
                            while True:
                                from_port = input("| Ingrese el from port: ")
                                if(from_port != ''):
                                    if(from_port == "ESC"):
                                        print("[*] Ha salido de la opción de -Añadir Regla-\n")
                                        return
                                    while True:
                                        dest_port = input("| Ingrese el dest port: ")
                                        if(dest_port != ''):
                                            if(dest_port == "ESC"):
                                                print("[*] Ha salido de la opción de -Añadir Regla-\n")
                                                return 
                                            verificar = input("| ¿Desea agregar un CIDR?[Y/N]: ")
                                            cidr = None
                                            if verificar == "Y" or verificar == "y":
                                                cidr = input("| Ingrese un CIDR: ")
                                                if(cidr == "ESC"):
                                                    print("[*] Ha salido de la opción de -Añadir Regla-\n")
                                                    return        
                                            elif(verificar == "ESC"):
                                                print("[*] Ha salido de la opción de -Añadir Regla-\n")
                                                return
                                            nova.agregarRegla(nombre,protocol_ip,from_port,dest_port,cidr)
                                            return
                                        else:
                                            print("[*] Ingrese un puerto válido\n")
                                            continue
                                else:
                                    print("[*] Ingrese un puerto válido\n")
                                    continue
                        else:
                            print("[*] Ingrese un protocolo IP válido\n")
                            continue
                else:
                    print("[*] Ingrese un nombre de securitygroup válido\n")
                    continue
        elif int(opcion) == 2:
            while True:
                id = input("| Ingrese el ID de la regla: ")
                if(id != ''):
                    if(id == "ESC"):
                        print("[*] Ha salido de la opción de -Eliminar Regla-\n")
                        return
                    nova.eliminarRegla(id)
                    break
                else:
                    print("[*] Ingrese un ID válido\n")
                    continue
        elif int(opcion) == 3:
            break
        else:
            print("[*] Ingrese una opción correcta\n")

#Funcion que permite obtener el ID de un Flavor   
def getFlavorsID(nova):
    listado = nova.list_flavors()
    while True:
        print("|--------------------Lista de Flavors------------------------|")
        i = 0
        for flavor in listado:
            print("|- Flavor "+str(i+1)+" -> "+str(flavor[1])+"| RAM: "+ str(flavor[2])+ "   | DISK: "+ str(flavor[3])+" | VCPUS: "+ str(flavor[4]))
            i = i + 1
        print("|--------------------------------------------------------------|")
        opcionFlavor = input("| Ingrese el # del flavor que desea usar: ")
        if opcionFlavor > len(listado):
            print("[*] Ingrese el # de un flavor válido\n")
        else:
            idFlavor = listado[int(opcionFlavor)-1][0]
            break
    return idFlavor

#Funcion que permite obtener el ID de una Imagen
def getImagenesID(glance):   
    listado = glance.listar_imagenes() 
    while True:
        print("|--------------------Lista de Imagenes------------------------|")
        i = 0
        for imagen in listado:
            print("|- Imagen "+str(i+1)+" -> "+str(imagen[1]))
            i = i + 1
        print("|--------------------------------------------------------------|")
        opcionImagen = input("| Ingrese el # de la imagen que desea usar: ")
        if opcionImagen > len(listado):
            print("[*] Ingrese el # de una imagen válida\n")
        else:
            idImagen = listado[int(opcionImagen)-1][0]
            break
    return idImagen

#Funcion que permite obtener el ID de una red
def getRedID(Neutron):
    listado = Neutron.listarRedes()
    while True:
        print("|--------------------Lista de Redes------------------------|")
        i = 0
        for red in listado:
            print("|- Red "+str(i+1)+" -> "+str(red[1]) + "  |  CIDR -> "+ str(red[2]))
            i = i + 1
        print("|--------------------------------------------------------------|")
        opcionImagen = input("| Ingrese el # de la red que desea usar: ")
        if opcionImagen > len(listado):
            print("[*] Ingrese el # de una red válida\n")
        else:
            idImagen = listado[int(opcionImagen)-1][0]
            break
    return idImagen

#Funcion que permite obtener el ID de una keypair
def getKeyPairID(nova,keystone):
    listado = nova.listarKeyPair(keystone.getUserID())
    while True:
        print("\n|-----------------------------------------------------|")
        i = 1
        for key in listado:
            print("| KeyPair "+str(i)+": "+str(key)+ "  |")
            i = i + 1
        print("|-----------------------------------------------------|")
        opcionKeyPair = input("| Ingrese el # de la keypair que desea usar: ")
        if opcionKeyPair > len(listado):
            print("[*] Ingrese el # de una keypair válida\n")
        else:
            keypair = listado[int(opcionKeyPair)-1][0]
            break
    return nova.obtenerIDKeyPair(keypair)

#Funcion que permite obtener el ID de un SecurityGroup
def getSecurityGroupID(nova):
    listado = nova.listarSecurityGroup()
    while True:
        print("\n|-----------------------------------------------------|")
        for SG in listado:
            print("| SecurityGroup "+str(SG[0])+" |  Descripcion : "+str(str(SG[1]))+ "  |")
        print("|-----------------------------------------------------|")    
        opcionSecurityGroup = input("| Ingrese el # del securitygroup que desea usar: ")
        if opcionSecurityGroup > len(listado):
            print("[*] Ingrese el # de un securitygroup válido\n")
        else:
            securitygroup = listado[int(opcionSecurityGroup)-1][0]
            break
    return nova.obtenerIDSecurityGroup(securitygroup)

def crearVM(Neutron, Nova, Glance):
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

def  Menu(Neutron, Nova, Glance):
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
            crearVM(Neutron, Nova, Glance)
            
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
            Menu(Neutron, Nova, Glance)
            break
            
        else:
            print("[*] Credenciales incorrectas\n")      
        
    else:
        print("[*] Credenciales incorrectas\n")   
        
print("[*] Fin de la aplicación\n")