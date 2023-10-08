import argparse
import csv
import time
from datetime import datetime

# FUNCIÓN PARA VALIDAR Y CONVERSION DE LAS FECHAS EN UN RANGO
def validar_rango_fechas(rango_str):
    try:
        fechas = rango_str.split(':')
        if len(fechas) != 2:
            raise argparse.ArgumentTypeError("El formato del rango de fechas debe ser 'yyyy-MM-dd:yyyy-MM-dd'")
        
        fecha_inicio = datetime.strptime(fechas[0], '%Y-%m-%d')
        fecha_fin = datetime.strptime(fechas[1], '%Y-%m-%d')
        return fecha_inicio, fecha_fin
    except ValueError:
        raise argparse.ArgumentTypeError("El formato de fecha debe ser 'yyyy-MM-dd'")

# FUNCIÓN PARA FORMATEAR LA FECHA DEL CSV (yyyy-MM-dd HH:mm:ss)
def formatear_fecha(timestamp):
    fecha_utc = datetime.utcfromtimestamp(timestamp)
    return fecha_utc.strftime('%Y-%m-%d %H:%M:%S')

# FUNCIÓN PARA VERIFICAR INGRESO DEL TIPO DE CHEQUE (EMITIDO O DEPOSITADO)
def validar_accion(value):
    if value.upper() in ["EMITIDO", "DEPOSITADO"]:
        return value
    else:
        raise argparse.ArgumentTypeError("Ingrese un Tipo de Cheque: (EMITIDO o DEPOSITADO)")

# FUNCIÓN PARA VERIFICAR INGRESO DEL TIPO DE SALIDA (PANTALLA O CSV)
def validar_formato(value):
    if value.upper() in ["PANTALLA", "CSV"]:
        return value
    else:
        raise argparse.ArgumentTypeError("Ingrese un Tipo de salida: (PANTALLA o CSV)")

# FUNCIÓN PARA VERIFICAR INGRESO DEL ESTADO DEL CHEQUE (PENDIENTE, APROBADO, RECHAZADO)
def validar_estado(value):
    if value.upper() in ["PENDIENTE", "APROBADO", "RECHAZADO"]:
        return value
    else:
        raise argparse.ArgumentTypeError("Ingrese el Estado del Cheque: (PENDIENTE, APROBADO o RECHAZADO)")

# PARSE DE ARGUMENTOS
parser = argparse.ArgumentParser(description="Consulta de cheques bancarios en un archivo CSV.")
parser.add_argument("archivo_csv", help="Nombre del archivo CSV")
parser.add_argument("DNI", type=int, help="Número de DNI (entre 7 y 8 dígitos)")
parser.add_argument("formato", type=validar_formato, metavar="FORMATO", help="Formato de salida (PANTALLA o CSV)")
parser.add_argument("accion", type=validar_accion, metavar="ACCION", help="Tipo de cheque (EMITIDO o DEPOSITADO)")
parser.add_argument("--estado", type=validar_estado, metavar="ESTADO", help="Filtrar por estado (opcional)")
parser.add_argument("--fecha", type=validar_rango_fechas, metavar="FECHA", help="Filtrar por rango de fechas (opcional)")

# OBTENER LOS ARGUMENTOS
args = parser.parse_args()

# VALIDAR CANTIDAD DE DÍGITOS PARA EL DNI
if not (7 <= len(str(args.DNI)) <= 8):
    print("Error: El número de DNI debe tener entre 7 y 8 dígitos.")
    exit()

# RASTREADOR DE DUPLICADOS EN NUMERO DE CHEQUE
numeros_de_cheque_duplicados = set()

# ABRE EL CSV Y PROCESA LOS DATOS SEPARADOS POR ';'
with open(args.archivo_csv, newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    resultados = []
    for row in reader:
        numero_cheque = int(row["NroCheque"])
        cuenta_origen = row["NumeroCuentaOrigen"]
         # VERIFICA EL NUMERO DE CHEQUE Y QUE NO HAYA DUPLICADOS
        if (numero_cheque, cuenta_origen) in numeros_de_cheque_duplicados:
            print(f"Error: Número de cheque duplicado ({numero_cheque}) en la cuenta {cuenta_origen}.")
        else:
            numeros_de_cheque_duplicados.add((numero_cheque, cuenta_origen))
            if int(row["DNI"]) == args.DNI:
                if args.estado is None or row["Estado"].lower().strip() == args.estado.lower().strip():
                    fecha_pago = datetime.utcfromtimestamp(int(row["FechaPago"])).date()
                    if args.fecha is None or (args.fecha[0].date() <= fecha_pago <= args.fecha[1].date()):
                        resultados.append(row)

# MUESTRA EL PRINT EN PANTALLA DE LOS DATOS DADO POR ARGUMENTOS
if args.formato.upper() == "PANTALLA":
    if resultados:
         # GENERA UNA TABLA PARA QUE LA SALIDA DE PANTALLA SEA VISUALMENTE MAS ORDENADA
        print("NroCheque | CodigoBanco | CodigoSucursal | NumeroCuentaOrigen | NumeroCuentaDestino | Valor | FechaOrigen | FechaPago | DNI | Estado")
        print("-" * 115)
        for resultado in resultados:
            fecha_origen = formatear_fecha(int(resultado['FechaOrigen']))
            fecha_pago = formatear_fecha(int(resultado['FechaPago']))
            print(f"{resultado['NroCheque']:9} | {resultado['CodigoBanco']:12} | {resultado['CodigoSucursal']:14} | {resultado['NumeroCuentaOrigen']:19} | {resultado['NumeroCuentaDestino']:19} | {resultado['Valor']:8} | {fecha_origen:19} | {fecha_pago:17} | {resultado['DNI']:10} | {resultado['Estado']}")
        print("-" * 115)
    else:
        print("No se encontraron resultados.")

 # MUESTRA LA EXPORTACIÓN DE LOS DATOS DADO POR ARGUMENTOS
elif args.formato.upper() == "CSV":
     # EXPORTA EL ARCHIVO CSV CON EL 'DNI_HORAACTUAL.CSV'
    nombre_archivo_salida = f"{args.DNI}_{int(time.time())}.csv"
    with open(nombre_archivo_salida, mode='w', newline='') as csvfile:
        fieldnames = ["NroCheque", "CodigoBanco", "CodigoSucursal", "NumeroCuentaOrigen", "NumeroCuentaDestino", "Valor", "FechaOrigen", "FechaPago", "DNI", "Estado"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,  delimiter=';')
        writer.writeheader()
        for resultado in resultados:
            resultado["FechaOrigen"] = formatear_fecha(int(resultado["FechaOrigen"]))
            resultado["FechaPago"] = formatear_fecha(int(resultado["FechaPago"]))
            writer.writerow(resultado)

    print(f"Resultados guardados en '{nombre_archivo_salida}' en formato CSV.")