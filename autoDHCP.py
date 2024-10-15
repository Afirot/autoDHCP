#Autor : Ignacio Sánchez Pérez
#Descripcion: Este script sirve para configurar automaticamente los hosts en DHCPD en linux mediante una lista de direcciones mac e ip en formato txt.

import re

##--------------------------------Cambie estas variables--------------------------------------------------------------

rut_conf = "/etc/dhcp/dhcpd.conf" #Ruta hacia el archivo de configuracion, normalmente es /etc/dhcp/dhcpd.conf
rut_lista = "lista.txt" #Ruta hacia la lista de direcciones, para que el programa funcione, por cada IP debe haber una MAC
dns = "8.8.8.8" #Servidor DNS

##---------------------------------------------------------------------------------------------------------------------

ip = []
mac = []
patron = r"HOST \d+" #Este patron se usara para saber el ultimo host ya registrado en el archivo de configuracion en la funcion ultimo_num
patron_ip = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
patron_mac = r'\b(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}\b'

#Listas

#Esta parte lee el archivo con la lista de ips y macs y lo mete todo a lo bruto en una lista
with open(rut_lista, "r") as file:
    cadena = file.read()
    lista = cadena.split()

#Esta parte divide las ips y las macs en dos listas distintas
for i in range(0, len(lista)):
    if re.search(patron_ip, lista[i]):
        ip.append(lista[i])
    elif re.search(patron_mac, lista[i]):
        mac.append(lista[i])

#Definicion de funciones

#Esta funcion buscara el ultimo numero del archivo de configuracion

def ultimo_num():
    with open(rut_conf, "r") as file:
        lista1 = re.findall(patron, file.read())
        if len(lista1) > 0: #Es necesario usar un if, ya que si el archivo esta vacio, dara un fallo al intentar buscar un elemento de una lista que no existe
            return(int(re.findall(r"\d+", lista1[-1])[0]))
        else:
            return(0)


#Este comparador se asegura de que la lista este en formato correcto, es decir, una mac por cada ip, si no es asi, saltara un mensaje de error

def comp(comando):
    if len(ip) != len(mac):
        print("ERROR, CORRIJA EL FORMATO DE LA LISTA")
    else:
        comando

#Esta parte escribe todo en el archivo de configuracion

def escritura():
    with open(rut_conf, "a") as file:
        for i in range(0, len(ip)):
            file.write(f"#HOST {ultimo_num() + i + 1} \n")
            file.write(f"host {ultimo_num() + i + 1} {{ \n")
            file.write(f"hardware ethernet {mac[i]} ; \n")
            file.write(f"fixe-address {ip[i]};\n")
            file.write(f"option domain-name-server {dns};\n")
            file.write("}\n\n")
    print("La configuracion ha finalizado correctamente")

#Llamada de funciones

comp(escritura())
