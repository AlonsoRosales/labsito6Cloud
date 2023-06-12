from getpass import getpass
from keystone import KeystoneClass
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

def configurarGrupoSeguridad(Neutron):
    Neutron.configurarSecurityGroup()

def crearVM(Neutron, Nova, Glance):
    nombreVM = input("| Ingrese el nombre de la VM: ")
    print("\n")
    
    flavor = Nova.listarFlavors()
    print("\n")
    
    imagen = Glance.listarImagenes()
    print("\n")
    
    red = Neutron.listarRedes()
    print("\n")
    
    llave = Nova.listarKeyPair()
    print("\n")
    
    securityGroup = Neutron.listarSecurityGroup()
    print("\n")

    Nova.crearVM(nombreVM,flavor,imagen,red,llave,securityGroup)


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
            configurarGrupoSeguridad(Neutron)
            
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