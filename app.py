#Se importan las librerias necesarias, y se inicializan las listas. 
import seaborn as sns
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import time
import Crear
import funciones 
import schedule 
from flask import Flask
import threading

app = Flask(__name__)






def Loop(): 
    fecha_inicio = datetime(2023, 11, 5, 0, 0)
    #Se crean las listas si es que no existen
    # Comprobar si la lista existe
    try:
        print(tiempo)
    except NameError:
        tiempo= Crear.CrearTiempo(fecha_inicio)
        print("se creo la lista tiempo")
        for element in tiempo:
            print(element)

    try:
        print(PL_list)
    except NameError:
        PL_list= Crear.CrearParametro(tiempo,0,30)
        print("se creo la lista Pluviosidad")
        print(PL_list)

    try:
        print(UV_list)
    except NameError:
        UV_list= Crear.CrearParametro(tiempo,0,14)
        print("se creo la lista Radiacion ")
        print(UV_list)


    datos = {
        'Fecha': tiempo,
        'Pluviosidad': PL_list,
        'Radiación UV': UV_list,
    }


    #Actualizamos la base de datos AL COMENZAR.
    import funciones
    funciones.DataBase(datos)

    #Se crean las imagenes. 
    tabla= 'tabla_excel.xlsx'
    funciones.Todo(tabla)



    # Programar las actualizaciones automaticas
    schedule.every().day.at("00:00:03").do(funciones.Todo,tabla)

    # Programar la tarea cada 5 minutos
    schedule.every(5).minutes.do(funciones.Hora,tabla)
    schedule.every(5).minutes.do(funciones.DataBase,datos)
    # Programar la tarea cada media hora
    schedule.every(30).minutes.do(funciones.Hoy,tabla)

    while True:
        schedule.run_pending()
        time.sleep(1)
if __name__ == '__main__':
    
    script_thread = threading.Thread(target=Loop())
    script_thread.start()

    # Inicia el servidor Flask
    app.run(debug=True, use_reloader=False)