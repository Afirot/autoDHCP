#Autor Ignacio Sánchez Pérez
import sys

def leer(archivo): #Esta funcion leera el archivo que se haya transmitido como argumento y almacenara su contenido en una lista, siendo dividido el texto por los saltos de linea
    global lista

    with open(archivo, "r") as file:
        cadena = file.read()
        lista = cadena.split("\n")
        del lista[0]
    

    
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
        
def repre(grupo, lis1, lis2, lis4): # Esta funcion sirve para escribir todo en el archibo de configuracion

    with open(RUT_CONF, "a") as file:
        file.write(f"group {grupo}{{\n")
        for i in range(0, len(lis1)):
            file.write(f"\t#HOST {lis1[i]}\n")
            file.write(f"\t{lis1[i]} {{ \n")
            file.write(f"\thardware ethernet {lis2[i]} ; \n")
            file.write(f"\tfixed-address {lis4[i]};\n")
            file.write("\t}\n\n")
        file.write("}\n")
                


def asig_ip(dir_red, minimo, maximo): #Esta funcion crea las ips en el rango especificado, en caso de ser una ip </24 debera añadirse otro for
    ip_list = []
    for i in range (minimo, maximo):
        if i < 255:
            
            new_ip = str(dir_red)+str(i)
            ip_list.append(new_ip)
    return ip_list


def main(): # Esta funcion llama al resto
    global fichero, lista, dispositivo, mac, tipo, wireless, desktop, server, RUT_CONF
    
    RUT_CONF = "/etc/dhcp/dhcpd.conf"
    lista = []
    dispositivo = []
    mac = []
    tipo = []
    mascara = "10.1.0."

    wireless = []
    desktop = []
    server = []

    try:
    #if compr_arg() and compr_fichero(): #Si los dos comprobadores son True, se inicia main.
        fichero = sys.argv[1]

        print("Iniciando script ...")
        leer(fichero)
        sep_list(lista)

        cre_list(wireless)
        ip_wireless = asig_ip(mascara, 12, 40)
        repre("wireless", dispositivo, mac, ip_wireless)

        cre_list(desktop)
        ip_desktop = asig_ip(mascara, 50, 80)
        repre("desktop", dispositivo, mac, ip_desktop)

        cre_list(server)
        ip_server = asig_ip(mascara, 230, 240)
        repre("server", dispositivo, mac, ip_server)

        print("Configuracion finalizada")

    except IndexError:
        print('Error de sintaxis. \n  python3 autoDHCP.py [Archivo csv]')

    except FileNotFoundError:
        print('Error\nEl archivo no existe')
    
    
    
main()
