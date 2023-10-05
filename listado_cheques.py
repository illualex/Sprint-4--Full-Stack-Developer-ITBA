import csv
import os
import time
from datetime import datetime

# FUNCIÓN LIMPIAR PANTALLA
def limpiar_pantalla():
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')

# VALIDADOR DNI
def validar_dni(dni):
    with open('cheques.csv', mode='r') as file:
        csv_reader = csv.DictReader(file, delimiter=';')
        for row in csv_reader:
            if row['DNI'] == dni:
                return True
    return False

# VALIDADOR DE FECHA
def validar_fechas(fecha_inicio):
    try:
        fecha_inicio_unix = int(fecha_inicio)
        # Validar que la fecha de inicio se encuentre en el archivo CSV
        with open('cheques.csv', mode='r') as file:
            csv_reader = csv.DictReader(file, delimiter=';')
            for row in csv_reader:
                if fecha_inicio_unix == int(row['FechaOrigen']):
                    return True
        return False
    except ValueError:
        return False


# FORMATEO DE FECHA
def formatear_fecha(fecha_unix):
    fecha = datetime.utcfromtimestamp(fecha_unix)
    return fecha.strftime('%Y-%m-%d %H:%M:%S')

# MOSTRAR MENU PRINCIPAL
def mostrar_menu():
    limpiar_pantalla()
    print("------ MENU CHEQUES ------\n")
    print("1) Procesar Cheque")
    print("2) Consultar Cheque")
    print("3) Salir del Programa")

# MOSTRAR MENU DNI
def escribir_dni():
    limpiar_pantalla()
    print("--- CONSULTAR CHEQUE ---\n")
    print("1) Escribir DNI")
    print("2) Volver atrás")

# MOSTRAR MENU SALIDA
def mostrar_menu_salida():
    print("\nSeleccione una opción de salida:")
    print("1) PANTALLA")
    print("2) CSV")
    print("3) Volver atrás")

# FUNCIÓN PARA CONSULTAR EL CHEQUE
def consultar_estado_cheque():
    limpiar_pantalla()
    print("----- ESTADO DEL CHEQUE -----\n")
    print("Desea consultar el Estado del Cheque?")
    print("Escriba 'Y' para Sí o 'N' para No")
    respuesta_estado = input("Esperando la respuesta: ")

    if respuesta_estado == 'Y' or respuesta_estado == 'y':
        while True:

            # PREGUNTAR ESTADO DEL CHEQUE
            limpiar_pantalla()
            print("Seleccione el Estado del Cheque:")
            print("1) PENDIENTE")
            print("2) APROBADO")
            print("3) RECHAZADO")
            print("4) Volver atrás")
            opcion_estado_cheque = input("Esperando la Operación: ")

            if opcion_estado_cheque == '1':
                limpiar_pantalla()
                print("Ha seleccionado PENDIENTE")
                preguntar_fechas()
                volver_al_menu()
            elif opcion_estado_cheque == '2':
                limpiar_pantalla()
                print("Ha seleccionado APROBADO")
                preguntar_fechas()
                volver_al_menu()
            elif opcion_estado_cheque == '3':
                limpiar_pantalla()
                print("Ha seleccionado RECHAZADO")
                preguntar_fechas()
                volver_al_menu()
            elif opcion_estado_cheque == '4':
                break
            else:
                input("Opción no válida. Presione Enter para continuar.")
    elif respuesta_estado == 'N' or respuesta_estado == 'n':
        print("SE ELEGIO NO")
    else:
        input("Opción no válida. Presione Enter para continuar.")

# FUNCIÓN PARA PREGUNTAR FECHA
def preguntar_fechas():
    limpiar_pantalla()
    print("Desea introducir un rango de fechas?")
    print("Escriba 'Y' para Sí o 'N' para No")
    respuesta_fechas = input("Esperando la respuesta: ")

    if respuesta_fechas == 'Y' or respuesta_fechas == 'y':
        limpiar_pantalla()
        print("---- FECHA DE ORIGEN ----\n")
        fecha_inicio = input("Ingrese la fecha de inicio: ")

        if validar_fechas(fecha_inicio):
            fecha_inicio_formateada = formatear_fecha(int(fecha_inicio))
            print("Fechas válidas: {fecha}")
        else:
            print("Datos incorrectos. Las fechas no coinciden con los registros.")
    elif respuesta_fechas == 'N' or respuesta_fechas == 'n':
        print("NO SE ELIGIÓ FECHAS")
    else:
        input("Opción no válida. Presione Enter para continuar.")

# FUNCIÓN PARA VOLVER AL MENU
def volver_al_menu():
    input("\nPresione Enter para volver al menú principal.")
    mostrar_menu()

# FUNCIÓN PRINCIPAL
def main():
    while True:

        # MENU INICIO
        mostrar_menu()
        opcion = input("\nElige una opción: ")
        if opcion == '1':
            limpiar_pantalla()
            input("Ha seleccionado Procesar Cheque")
            mostrar_menu()
            # LÓGICA PARA PROCESAR CHEQUE

        elif opcion == '2':

            # PREGUNTA DNI
            while True:
                limpiar_pantalla()
                escribir_dni()
                opcion_consultar = input("\nSeleccione una opción: ")

                if opcion_consultar == '1':
                    limpiar_pantalla()
                    print ("----- DNI -----\n")
                    dni = input("Ingrese el DNI: ")
                    if validar_dni(dni):
                        while True:

                            #TIPO DE SALIDA
                            limpiar_pantalla()
                            print(f"El DNI {dni} es válido.")
                            mostrar_menu_salida()
                            opcion_menu = input("\nEsperando la Operación: ")
                            if opcion_menu == '1':
                                limpiar_pantalla()
                                print("Ha seleccionado PANTALLA")
                                consultar_estado_cheque()
                            elif opcion_menu == '2':
                                limpiar_pantalla()
                                print("Ha seleccionado CSV")

                                # LÓGICA PARA EL CSV

                            elif opcion_menu == '3':
                                break
                            else:
                                input("\nOpción no válida. Presione Enter para continuar.")
                    else:
                        input("\nDNI no válido. Presione Enter para continuar.")
                elif opcion_consultar == '2':
                    break
                else:
                    input("\nOpción no válida. Presione Enter para continuar.")
        elif opcion == '3':
            limpiar_pantalla()
            print("Saliendo del programa...")
            input("\nPresione Enter.")
            limpiar_pantalla()
            break
        else:
            input("Opción no válida. Presione Enter para continuar.")

if __name__ == "__main__":
    main()
