#Autor : Ignacio Sánchez Pérez
#Descripcion: Este script sirve para configurar automaticamente los hosts en DHCPD en linux mediante una lista de direcciones mac e ip en formato txt.
import sys
import os
import re

def leer(archivo): #Esta funcion leera el archivo que se haya transmitido como argumento y almacenara su contenido en una lista, siendo dividido el texto por los saltos de linea
    global lista
    with open(archivo, "r") as file:
        cadena = file.read()
        lista = cadena.split("\n")
        del lista[0]

def compr_arg(): #Esta funcion comprueba que el numero de argumentos es correcto, en caso de serlo, almacenara el nombre del fichero en fichero, en caso de no serlo, enviara un error y devolbera false
    global fichero
    if len(sys.argv) == 2:
        fichero = sys.argv[1]
        return True
    else:
        print("ERROR, DEBE DE AÑADIR SOLO EL NOMBRE DEL ARCHIVO")
        return False

def compr_fichero(): #Esta funcion comprueba si el archivo transmitido como argumento existe, en caso de existir, devuelve True, en caso de no existir, enviara un mensaje de error y devolbera False.
    if os.path.isfile(fichero):
        return True
    else:
        print("ERROR, EL ARCHIVO NO EXISTE")
        return False
    
def sep_list(lista): #Esta funcion busca separar las listas en distintos array en funcion del tipo de dispositivos
    global wireless, desktop, server
    for i in lista:
        listaRota = i.split(";")
        
        if listaRota[2] == "Wireless":
            wireless.append(i)
        elif listaRota[2] == "Desktop":
            desktop.append(i)
        elif listaRota[2] == "Server":
            server.append(i)

def cre_list(lista): #Esta funcion tomara la lista creada en la funcion leer() y dividira su contenido en las listas dispositivo, mac, tipo.
    global dispositivo, mac, tipo, ip
    dispositivo = []
    mac = []
    tipo = []
    ip = []
    for i in lista:
        listaFinal = i.split(";")
        dispositivo.append(listaFinal[0])
        mac.append(listaFinal[1])
        tipo.append(listaFinal[2])
        
def repre(grupo, lis1, lis2, lis3, exis): # Esta funcion sirve para escribir todo en el archibo de configuracion

    with open(RUT_CONF, "a") as file:
        file.write(f"group {grupo} {{\n")
        for i in range(0, len(lis1)):
            if lis2[i] not in exis: #Aqui compruebo si la mac que quiero introducir ya existe en el archivo, y si ese es el caso, da un mensaje indicandolo y no la imprime en el archivo
                file.write(f"\t#HOST {lis1[i]}\n")
                file.write(f"\t{lis1[i]} {{\n")
                file.write(f"\thardware ethernet {lis2[i]} ; \n")
                file.write(f"\tfixed-address {lis3[i]};\n")
                file.write("\t}\n\n")
            else:
                print(f"La direccion mac {lis2[i]} ya existe")
        file.write("}\n")

def existen(rut_conf): #Esta funcion extrae una lista de las macs que esisten en el archivo de configuracion

    with open(rut_conf, "r") as file:
        #for l in file:
        cadena = file.read()
        macs = (re.findall(r"(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})", cadena))
        
    return macs

def asig_ip(dir_red, minimo, maximo): #Asignar ip
    ip_list = []
    for i in range (minimo, maximo):
        if i < 255:
            
            new_ip = str(dir_red)+str(i)
            ip_list.append(new_ip)
    return ip_list


def main(): # Esta funcion llama al resto
    global fichero, lista, dispositivo, mac, tipo, wireless, desktop, server, RUT_CONF
    
    RUT_CONF = "/etc/dhcp/dhcpd.conf"
    fichero = sys.argv[1]
    lista = []
    dispositivo = []
    mac = []
    tipo = []
    mascara = "10.1.0."

    wireless = []
    desktop = []
    server = []


    if compr_arg() and compr_fichero(): #Si los dos comprobadores son True, se inicia main.
        existentes = existen(RUT_CONF)
        print("Iniciando script ...")
        leer(fichero)
        sep_list(lista)

        cre_list(wireless)
        ip_wireless = asig_ip(mascara, 12, 40)
        repre("Wireless",dispositivo, mac, ip_wireless, existentes)

        cre_list(desktop)
        ip_desktop = asig_ip(mascara, 50, 80)
        repre("Desktop",dispositivo, mac, ip_desktop, existentes)

        cre_list(server)
        ip_server = asig_ip(mascara, 230, 240)
        repre("Server",dispositivo, mac, ip_server, existentes)

        print("Configuracion finalizada")
    
    
main()

