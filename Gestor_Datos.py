from tkinter import ttk
from ttkbootstrap import *
import ttkbootstrap as ttkb
from ttkbootstrap.dialogs import Messagebox
import os
import sqlite3
from datetime import *
import string
from ttkbootstrap.validation import add_regex_validation
from dateutil.relativedelta import relativedelta
import locale
import os
import sys

# Obtén el directorio en el que se encuentra el ejecutable
directorio_ejecutable = os.path.dirname(sys.executable)

# Construye la ruta a la carpeta "multimedia" dentro del directorio del ejecutable
carpeta_multimedia = os.path.join(directorio_ejecutable, "Multimedia")

# Nombre del archivo que buscas
nombre_archivo_busqueda = "icono.ico"

# Combina la ruta de la carpeta multimedia con el nombre del archivo
ruta_archivo = os.path.join(carpeta_multimedia, nombre_archivo_busqueda)

#hasciendo lo que esta en la linea 29 puedes correrlo de forma local al icono.
# ruta_archivo= "icono.ico"


icono = ruta_archivo  #se debe escribir el path de la imagen
root = ttkb.Window(themename='darkly')
root.title('Automatización de Carga')
root.resizable(False, False)
root.iconbitmap(icono)
# Obtiene el tamaño de la pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()



# Establece el tamaño de la ventana principal
root.geometry(f"{screen_width-250}x{screen_height-250}+100+100")


# concepción DB
conn = sqlite3.connect('DBapp_GESTOR.db')
c = conn.cursor()


#   Creando base de datos.

#   TABLA Titular
c.execute("""
    CREATE TABLE IF NOT EXISTS `Titular` (
        `DNITIT` INTEGER PRIMARY KEY,
        `NOMTIT` TEXT NOT NULL,
        `APETIT` TEXT NOT NULL,
        `CUIL_CUIT_TIT` TEXT NOT NULL,
        `FNATIT` DATE NOT NULL,
        `TELTIT` TEXT NOT NULL,
        `MAILTIT` TEXT NOT NULL,
        `LOCTIT` TEXT NOT NULL,
        `FCHTIT` DATE NOT NULL,
        `NOTTIT` TEXT NULL,
        `ELITIT` TEXT NOT NULL DEFAULT 'NO'
        );
""")

#   TABLA Cónyuge
c.execute("""
    CREATE TABLE IF NOT EXISTS `Conyuge` (
        `DNICON` INTEGER PRIMARY KEY,
        `NOMCON` TEXT NOT NULL,
        `APECON` TEXT NOT NULL,
        `CUIL_CUIT_CON` TEXT NOT NULL,
        `FNACON` DATE NOT NULL,
        `TELCON` TEXT NOT NULL,
        `MAILCON` TEXT NOT NULL,
        `LOCCON` TEXT NOT NULL,
        `FCHCON` DATE NULL,
        `ELICON` TEXT NOT NULL DEFAULT 'NO',
        `Titular_DNITIT` INTEGER NOT NULL,
        FOREIGN KEY (`Titular_DNITIT`) REFERENCES `Titular` (`DNITIT`) ON DELETE NO ACTION ON UPDATE NO ACTION
        );
""")

#   TABLA Hijo
c.execute("""
    CREATE TABLE IF NOT EXISTS `Hijo` (
        `DNIHIJ` INTEGER PRIMARY KEY,
        `NOMHIJ` TEXT NOT NULL,
        `APEHIJ` TEXT NOT NULL,
        `CUIL_CUIT_HIJ` TEXT NOT NULL,
        `FNAHIJ` DATE NOT NULL,
        `LOCHIJ` TEXT NOT NULL,
        `PDSHIJ` TEXT NOT NULL,
        `FCHHIJ` DATE NOT NULL,
        `ELIHIJ` TEXT NOT NULL DEFAULT 'NO',
        `Titular_DNITIT` INTEGER NOT NULL,
        FOREIGN KEY (`Titular_DNITIT`) REFERENCES `Titular` (`DNITIT`) ON DELETE NO ACTION ON UPDATE NO ACTION
        );
""")

#   TABLA Cotización
c.execute("""
    CREATE TABLE IF NOT EXISTS `Cotizacion` (
        `IDCOT` INTEGER PRIMARY KEY AUTOINCREMENT,
        `TIPCOT` VARCHAR(15) NOT NULL,
        `TRESAPOR` INTEGER NULL,
        `SBRUT` INTEGER NULL,
        `FHINGL` DATE NOT NULL,
        `CATCOT` TEXT NULL,
        `PERAPORT` INTEGER NULL,
        `COBACTU` TEXT NULL,
        `PREPAGA` TEXT NULL,
        `PLANCOT` TEXT NULL,
        `MOTCAMB` TEXT NULL,
        `DATREF` TEXT NULL,
        `FCHCOT` DATE NOT NULL,
        `ELICOT` TEXT NOT NULL DEFAULT 'NO',
        `Titular_DNITIT` INTEGER NOT NULL,
        FOREIGN KEY (`Titular_DNITIT`) REFERENCES `Titular`
            (`DNITIT`) ON DELETE NO ACTION ON UPDATE NO ACTION
        );
""")

#   TABLA Llamados_Ventas
c.execute("""
    CREATE TABLE IF NOT EXISTS `Llamados_Ventas` (
        `IDLVEN` INTEGER PRIMARY KEY AUTOINCREMENT,
        `RESLVEN` TEXT NULL,
        `VENTLVEN` TEXT NULL,
        `FCHLVEN` DATE NULL,
        `Titular_DNITIT` INTEGER NOT NULL,
        `ELILVEN` TEXT NULL DEFAULT 'NO',
        FOREIGN KEY (`Titular_DNITIT`) REFERENCES `Titular` (`DNITIT`) ON DELETE NO ACTION ON UPDATE NO ACTION
        );
""")

#----------------------------------------------------------------#

def listAlphabetUpper():
    return list(string.ascii_lowercase.upper())


def listAlphabetLower():
    return list(string.ascii_lowercase.lower())


def definir_edad(fecha):
    # calcula la Edad según la fecha de nacimiento que le pasemos en la carga.
    fecha = fecha.replace('-', '/')
    fecha_nacimiento = datetime.strptime(fecha, "%d/%m/%Y")
    edad = relativedelta(datetime.now(), fecha_nacimiento)
    return edad.years

def validar_Enreys_Solo_Numeros(entry):
    return add_regex_validation(entry, r'^[0-9]*$')


def validar_Enreys_Solo_Letras(entry):
    return add_regex_validation(entry, r'^[a-zA-ZÀ-ÿ\s]*$')


def validar_nombre_sin_espacios(nombre):
    '''Valida que no tenga espacios en blanco o "tabs" por delante o por detrás del NOMBRE
        retorna la cadena limpia lista para ser almacenadas en la base de datos'''
    
    # Elimina espacios en blanco al principio y al final de la cadena
    nombre_limpio = nombre.strip()

    # Reemplaza espacios internos por un solo espacio
    nombre_limpio = ' '.join(nombre_limpio.split())

    return nombre_limpio



def validar_apellido_sin_espacios(apellido):
    '''Valida que no tenga espacios en blanco o "tabs" por delante o por detrás del APELLIDO.
        retorna la cadena limpia lista para ser almacenadas en la base de datos'''
    
    # Elimina espacios en blanco al principio y al final de la cadena
    apellido_limpio = apellido.strip()

    # Reemplaza espacios internos por un solo espacio
    apellido_limpio = ' '.join(apellido_limpio.split())

    return apellido_limpio





#----------------------------------------------------------------#
def insertar_Conyuge(resultados):
    """insertar datos conyuge
        hace un comit de los datos recopilados de los entry para guardarlos en la DB correspondiente
    """
    c.execute("""
        INSERT INTO Conyuge (DNICON,NOMCON,APECON,CUIL_CUIT_CON,FNACON,TELCON,MAILCON,LOCCON,FCHCON,Titular_DNITIT) VALUES(?,?,?,?,?,?,?,?,?,?)
    """, (resultados['DNICON'], resultados['NOMCON'], resultados['APECON'], resultados['CUIL_CUIT_CON'], resultados['FNACON'], resultados['TELCON'], resultados['MAILCON'], resultados['LOCCON'], resultados['FCHCON'], resultados['Titular_DNITIT']))
    conn.commit()


def insertar_Titular(resultados):
    """insertar datos titular
        hace un comit de los datos recopilados de los entry para guardarlos en la DB correspondiente
    """
    c.execute("""
            INSERT INTO Titular (DNITIT,NOMTIT,APETIT,CUIL_CUIT_TIT,FNATIT,TELTIT,MAILTIT,LOCTIT,FCHTIT,NOTTIT) VALUES(?,?,?,?,?,?,?,?,?,?)
        """, (resultados['DNITIT'], resultados['NOMTIT'], resultados['APETIT'], resultados['CUIL_CUIT_TIT'], resultados['FNATIT'], resultados['TELTIT'], resultados['MAILTIT'], resultados['LOCTIT'], resultados['FCHTIT'], resultados['NOTTIT']))
    conn.commit()


def insertar_Hijo(resultados):
    """insertar datos hijo
        hace un comit de los datos recopilados de los entry para guardarlos en la DB correspondiente
    """
    c.execute("""
        INSERT INTO Hijo (DNIHIJ,NOMHIJ,APEHIJ,CUIL_CUIT_HIJ,FNAHIJ,LOCHIJ,PDSHIJ,FCHHIJ,Titular_DNITIT) VALUES(?,?,?,?,?,?,?,?,?)
    """, (resultados['DNIHIJ'], resultados['NOMHIJ'], resultados['APEHIJ'], resultados['CUIL_CUIT_HIJ'], resultados['FNAHIJ'], resultados['LOCHIJ'], resultados['PDSHIJ'], resultados['FCHHIJ'], resultados['DNITIT_HIJO']))
    conn.commit()




#       TITULAR.
def carga_titular():
    top = Toplevel()
    top.title('Carga Titular')
    top.resizable(False, False)
    icono = ruta_archivo
    top.iconbitmap(icono)
    top.resizable(False,False)

    # top.configure(background='#304c94')
    """_summary_
        Lo que hace esta función es dar pie al carga del Titular, creando una nueva ventana, que a su vez contiene otra función la cual se encarga de exponer 
            y guardar la carga de datos 

    """

    # Datos de carga
    def datos():
        x = ttkb.LabelFrame(top, text='Titular', padding=5,
                            borderwidth=3, relief="ridge")
        x.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

        l_dni = ttkb.Label(x, text='DNI:', font=('Time New Roman', 14),
                           borderwidth=3, relief="groove", anchor=W).grid(row=0, column=0, sticky="nsew", pady=8)
        dni = ttkb.Entry(x, width=40, font=(16))
        dni.grid(row=0, column=1, pady=8, padx=10)
        validar_Enreys_Solo_Numeros(dni)

        l_nombre = ttkb.Label(x, text='Nombre/s:', font=('Time New Roman', 14),
                              borderwidth=3, relief="groove").grid(row=1, column=0, sticky="nsew", pady=8)
        nombre = ttkb.Entry(x, width=40, font=(16))
        nombre.grid(row=1, column=1, pady=8, padx=10)
        validar_Enreys_Solo_Letras(nombre)

        l_apellido = ttkb.Label(x, text='Apellido/s:', font=('Time New Roman', 14),
                                borderwidth=3, relief="groove", anchor=W).grid(row=2, column=0, sticky="nsew", pady=8)
        apellido = ttkb.Entry(x, width=40, font=(16))
        apellido.grid(row=2, column=1, pady=8, padx=10)
        validar_Enreys_Solo_Letras(apellido)

        l_cuil_cuit = ttkb.Label(x, text='CUIL / CUIT:', font=('Time New Roman', 14),
                                 borderwidth=3, relief="groove", anchor=W).grid(row=3, column=0, sticky="nsew", pady=8)
        cuil_cuit = ttkb.Entry(x, width=40, font=(16))
        cuil_cuit.grid(row=3, column=1, pady=8, padx=10)
        validar_Enreys_Solo_Numeros(cuil_cuit)

        l_fNacimiento = ttkb.Label(x, text='Fecha de Nacimiento:', font=(
            'Time New Roman', 14), borderwidth=3, relief="groove", anchor=W).grid(row=4, column=0, sticky="nsew", pady=8)
        sel = StringVar()
        fNacimiento = ttkb.DateEntry(
            x, bootstyle='solar', dateformat='%d-%m-%Y', firstweekday=0)
        fNacimiento.grid(row=4, column=1, pady=8, padx=10)

        l_telef = ttkb.Label(x, text='Teléfono:', font=('Time New Roman', 14),
                             borderwidth=3, relief="groove", anchor=W).grid(row=6, column=0, sticky="nsew", pady=8)
        telef = ttkb.Entry(x, width=40, font=(16))
        telef.grid(row=6, column=1, pady=8, padx=10)
        validar_Enreys_Solo_Numeros(telef)

        l_mail = ttkb.Label(x, text='Mail:',  font=('Time New Roman', 14),
                            borderwidth=3, relief="groove", anchor=W).grid(row=7, column=0, sticky="nsew", pady=8)
        mail = ttkb.Entry(x, width=40, font=(16))
        mail.grid(row=7, column=1, pady=8, padx=10)

        l_localidad_r = ttkb.Label(x, text='Localidad de residencia:', font=(
            'Time New Roman', 14), borderwidth=3, relief="groove", anchor=W).grid(row=8, column=0, sticky="nsew", pady=8)
        localidad_r = ttkb.Entry(x, width=40, font=(16))
        localidad_r.grid(row=8, column=1, pady=8, padx=10)
        validar_Enreys_Solo_Letras(localidad_r)

        l_nota = ttkb.Label(x, text='Nota:', font=(
            'Time New Roman', 14), borderwidth=3, relief="groove", anchor=W).grid(row=9, column=0, sticky="nsew", pady=8)
        nota = ttkb.Entry(x, width=40, font=(16))
        nota.grid(row=9, column=1, pady=8, padx=10)

        # ---------------------------------------------------------------------#

        def guardar():
            """_summary_
                Guarda los datos y aplica el button guardar el cual si un campo no esta completo se le da un mensaje al usuario.
            """
            
            
            if not dni.get():
                Messagebox.show_error(
                    'El campo "DNI" es obligatorio.', 'Error')
                top.lift()
                return
            elif not nombre.get():
                Messagebox.show_error(
                    'El campo "Nombre/s" es obligatorio.', 'Error')
                top.lift()
                return
            elif not apellido.get():
                Messagebox.show_error(
                    'El campo "Apellido/s" es obligatorio.', 'Error')
                top.lift()
                return
            elif not cuil_cuit.get:
                Messagebox.show_error(
                    'El campo "CUIL / CUIT" es obligatorio.''Error')
                top.lift()
                return
            elif not fNacimiento.entry.get():
                Messagebox.show_error(
                    'El campo "Fecha de Nacimiento" es obligatorio.', 'Error')
                top.lift()
                return
            elif not telef.get():
                Messagebox.show_error(
                    'El campo "Teléfono" es obligatorio.', 'Error')
                top.lift()
                return
            elif not mail.get():
                Messagebox.show_error(
                    'El campo "Mail" es obligatorio.', 'Error')
                top.lift()
                return
            elif not localidad_r.get():
                Messagebox.show_error(
                    'El campo "Localidad de residencia" es obligatorio.', 'Error')
                top.lift()
                return

            try:
                # si los campos fueron llenados con exito, agrupa los mismos en un diccionarios para despues usarlos para guardar en su respectiva tabla
                ahora = datetime.date(datetime.now())

                nom = validar_nombre_sin_espacios(nombre.get()) # limpia el nombre
                ape = validar_apellido_sin_espacios(apellido.get()) # limpia el apellido

                resultados = {
                    'DNITIT': int(dni.get()),
                    'NOMTIT': nom.upper(),
                    'APETIT': ape.upper(),
                    'CUIL_CUIT_TIT': int(cuil_cuit.get()),
                    'FNATIT': fNacimiento.entry.get(),
                    'TELTIT': int(telef.get()),
                    'MAILTIT': mail.get(),
                    'LOCTIT': localidad_r.get().upper(),
                    'FCHTIT': ahora,
                    'NOTTIT': nota.get()
                }

                rows = c.execute(
                    """SELECT * From Titular WHERE DNITIT = ?""", (resultados['DNITIT'], )).fetchall()

                if not rows:
                    
                    insertar_Titular(resultados)
                    top.destroy()
                else:
                    Messagebox.show_error(
                        f'Ya existe un registro con el DNI: {resultados["DNITIT"]}', 'Error')
                    top.lift()
                    return

            except ValueError:
                Messagebox.show_warning(
                    'Verifique los CAMPOS', 'Error en algun Campo')
                top.lift()

        btn_guardar = ttkb.Button(top, text='Guardar', command=guardar)
        btn_guardar.grid(column=2, row=3, padx=15, pady=15)

        top.mainloop()
    # ---------------------------------------------------------------------#

    # Llamado de la función
    Titular = datos()

#       CÓNYUGE.
def carga_conyuge():
    top = Toplevel()
    top.title('Carga Cónyuge')
    top.resizable(False, False)
    icono = ruta_archivo
    top.iconbitmap(icono)
    top.resizable(False,False)

    """carga_conyuge
        Lo que hace esta función es dar pie al carga del Conyuge, creando una nueva ventana, que a su vez contiene otra función la cual se encarga de exponer 
            y guardar la carga de datos 

    """
    # Datos de carga
    def datos():
        x = ttkb.LabelFrame(top, text='Cónyuge', padding=5,
                            borderwidth=3, relief="ridge")
        x.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

        l_dni = ttkb.Label(x, text='DNI:',  font=('Time New Roman', 14),
                           borderwidth=3, relief="groove", anchor=W).grid(row=0, column=0, sticky="nsew", pady=8)
        dni = ttkb.Entry(x, width=40, font=(16))
        dni.grid(row=0, column=1, pady=8, padx=10)
        validar_Enreys_Solo_Numeros(dni)

        l_nombre = ttkb.Label(x, text='Nombre/s:', font=('Time New Roman', 14),
                              borderwidth=3, relief="groove").grid(row=1, column=0, sticky="nsew", pady=8)
        nombre = ttkb.Entry(x, width=40, font=(16))
        nombre.grid(row=1, column=1, pady=8, padx=10)
        validar_Enreys_Solo_Letras(nombre)

        l_apellido = ttkb.Label(x, text='Apellido/s:', font=('Time New Roman', 14),
                                borderwidth=3, relief="groove", anchor=W).grid(row=2, column=0, sticky="nsew", pady=8)
        apellido = ttkb.Entry(x, width=40, font=(16))
        apellido.grid(row=2, column=1, pady=8, padx=10)
        validar_Enreys_Solo_Letras(apellido)

        l_cuil_cuit = ttkb.Label(x, text='CUIL / CUIT:', font=('Time New Roman', 14),
                                 borderwidth=3, relief="groove", anchor=W).grid(row=3, column=0, sticky="nsew", pady=8)
        cuil_cuit = ttkb.Entry(x, width=40, font=(16))
        cuil_cuit.grid(row=3, column=1, pady=8, padx=10)
        validar_Enreys_Solo_Numeros(cuil_cuit)

        l_fNacimiento = ttkb.Label(x, text='Fecha de Nacimiento:', font=(
            'Time New Roman', 14), borderwidth=3, relief="groove", anchor=W).grid(row=4, column=0, sticky="nsew", pady=8)
        sel = StringVar()
        fNacimiento = ttkb.DateEntry(
            x, bootstyle='solar', dateformat='%d-%m-%Y', firstweekday=0)
        fNacimiento.grid(row=4, column=1, pady=8, padx=10)

        l_telef = ttkb.Label(x, text='Teléfono:', font=('Time New Roman', 14),
                             borderwidth=3, relief="groove", anchor=W).grid(row=6, column=0, sticky="nsew", pady=8)
        telef = ttkb.Entry(x, width=40, font=(16))
        telef.grid(row=6, column=1, pady=8, padx=10)
        validar_Enreys_Solo_Numeros(telef)

        l_mail = ttkb.Label(x, text='Mail:', font=('Time New Roman', 14),
                            borderwidth=3, relief="groove", anchor=W).grid(row=7, column=0, sticky="nsew", pady=8)
        mail = ttkb.Entry(x, width=40, font=(16))
        mail.grid(row=7, column=1, pady=8, padx=10)

        l_localidad_r = ttkb.Label(x, text='Localidad de residencia:', font=(
            'Time New Roman', 14), borderwidth=3, relief="groove", anchor=W).grid(row=8, column=0, sticky="nsew", pady=8)
        localidad_r = ttkb.Entry(x, width=40, font=(16))
        localidad_r.grid(row=8, column=1, pady=8, padx=10)
        validar_Enreys_Solo_Letras(localidad_r)

        l_Tit_DNITIT = ttkb.Label(x, text='DNI Titular', font=(
            'Time New Roman', 14), borderwidth=3, relief="groove", anchor=W).grid(row=9, column=0, sticky="nsew", pady=8)
        Tit_DNITIT = ttkb.Entry(x, width=40, font=(16))
        Tit_DNITIT.grid(row=9, column=1, pady=8, padx=10)
        validar_Enreys_Solo_Numeros(Tit_DNITIT)
        # ---------------------------------------------------------------------#

        def guardar():
            """_summary_
                Guarda los datos y aplica el button guardar el cual si un campo no esta completo se le da un mensaje al usuario.
            """

            if not dni.get():
                Messagebox.show_error(
                    'El campo "DNI" es obligatorio.', 'Error')
                top.lift()
                return
            elif not nombre.get():
                Messagebox.show_error(
                    'El campo "Nombre/s" es obligatorio.', 'Error')
                top.lift()
                return
            elif not apellido.get():
                Messagebox.show_error(
                    'El campo "Apellido/s" es obligatorio.', 'Error')
                top.lift()
                return
            elif not cuil_cuit.get:
                Messagebox.show_error(
                    'El campo "CUIL / CUIT" es obligatorio.''Error')
                top.lift()
                return
            elif not fNacimiento.entry.get():
                Messagebox.show_error(
                    'El campo "Fecha de Nacimiento" es obligatorio.', 'Error')
                top.lift()
                return

            elif not telef.get():
                Messagebox.show_error(
                    'El campo "Teléfono" es obligatorio.', 'Error')
                top.lift()
                return
            elif not mail.get():
                Messagebox.show_error(
                    'El campo "Mail" es obligatorio.', 'Error')
                top.lift()
                return
            elif not localidad_r.get():
                Messagebox.show_error(
                    'El campo "Localidad de residencia" es obligatorio.', 'Error')
                top.lift()
                return

            try:
                # si los campos fueron llenados con exito, agrupa los mismos en un diccionarios para despues usarlos para guardar en su respectiva tabla
                ahora = datetime.date(datetime.now())

                nom = validar_nombre_sin_espacios(nombre.get()) # limpia el nombre
                ape = validar_apellido_sin_espacios(apellido.get()) # limpia el apellido

                resultados = {
                    'DNICON': int(dni.get()),
                    'NOMCON': nom.upper(),
                    'APECON': ape.upper(),
                    'CUIL_CUIT_CON': int(cuil_cuit.get()),
                    'FNACON': fNacimiento.entry.get(),
                    'TELCON': int(telef.get()),
                    'MAILCON': mail.get(),
                    'LOCCON': localidad_r.get().upper(),
                    'FCHCON': ahora,
                    'Titular_DNITIT': int(Tit_DNITIT.get())
                }
                rows = c.execute(
                    """SELECT * From Conyuge WHERE DNICON = ?""", (resultados['DNICON'], )).fetchall()

                if not rows:
                    # Messagebox.show_info(
                    #     '¡¡¡EL contenido fue Enviado con éxito 👌!!!', 'Enviado')
                    insertar_Conyuge(resultados)
                    top.destroy()
                else:
                    Messagebox.show_error(
                        f'Ya existe un registro con el DNI: {resultados["DNITIT"]}', 'Error')
                    top.lift()
                    return
            except ValueError:
                Messagebox.show_warning(
                    'Verifique los CAMPOS', 'Error en algun Campo')
                top.lift()

        btn_guardar = ttkb.Button(top, text='Guardar', command=guardar)
        btn_guardar.grid(column=2, row=3, padx=15, pady=15)
        top.mainloop()
        # ---------------------------------------------------------------------#

    # Llamado de la función
    Conyuge = datos()


#       HIJO.
def carga_hijo():
    top = Toplevel()
    top.title('Carga Hijo/s')
    top.resizable(False, False)
    icono = ruta_archivo
    top.iconbitmap(icono)
    top.resizable(False,False)

    """carga_hijo
        Lo que hace esta función es dar pie al carga del Hijo, creando una nueva ventana, que a su vez contiene otra función la cual se encarga de exponer 
            y guardar la carga de datos 

    """
    # Datos de carga
    def datos():

        x = ttkb.LabelFrame(top, text='Hijo', padding=5,
                            borderwidth=3, relief="ridge")
        x.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

        l_dni = ttkb.Label(x, text='DNI:',  font=('Time New Roman', 14),
                           borderwidth=3, relief="groove", anchor=W).grid(row=0, column=0, sticky="nsew", pady=8)
        dni = ttkb.Entry(x, width=40, font=(16))
        dni.grid(row=0, column=1, pady=8, padx=10)
        validar_Enreys_Solo_Numeros(dni)

        l_nombre = ttkb.Label(x, text='Nombre/s:', font=('Time New Roman', 14),
                              borderwidth=3, relief="groove").grid(row=1, column=0, sticky="nsew", pady=8)
        nombre = ttkb.Entry(x, width=40, font=(16))
        nombre.grid(row=1, column=1, pady=8, padx=10)
        validar_Enreys_Solo_Letras(nombre)

        l_apellido = ttkb.Label(x, text='Apellido/s:', font=('Time New Roman', 14),
                                borderwidth=3, relief="groove", anchor=W).grid(row=2, column=0, sticky="nsew", pady=8)
        apellido = ttkb.Entry(x, width=40, font=(16))
        apellido.grid(row=2, column=1, pady=8, padx=10)
        validar_Enreys_Solo_Letras(apellido)

        l_cuil_cuit = ttkb.Label(x, text='CUIL / CUIT:', font=('Time New Roman', 14),
                                 borderwidth=3, relief="groove", anchor=W).grid(row=3, column=0, sticky="nsew", pady=8)
        cuil_cuit = ttkb.Entry(x, width=40, font=(16))
        cuil_cuit.grid(row=3, column=1, pady=8, padx=10)
        validar_Enreys_Solo_Numeros(cuil_cuit)

        l_fNacimiento = ttkb.Label(x, text='Fecha de Nacimiento:', font=(
            'Time New Roman', 14), borderwidth=3, relief="groove", anchor=W).grid(row=4, column=0, sticky="nsew", pady=8)
        fNacimiento = ttkb.DateEntry(
            x, bootstyle='solar', dateformat='%d-%m-%Y', firstweekday=0)
        fNacimiento.grid(row=4, column=1, pady=8, padx=10)

        l_hijo_de = ttkb.Label(x, text='Hijo de:', font=(
            'Time New Roman', 14), borderwidth=3, relief="groove", anchor=W).grid(row=7, column=0, sticky="nsew", pady=8)
        lista_datos = ['-----------',
                       'Titular',
                       'Cónyuge',
                       'Titular y Cónyuges'
                       ]
        # value es el valor asignado de la lista desplegable
        value = StringVar()
        value.set(lista_datos[0])
        hijo_de = OptionMenu(x, value, *lista_datos)
        hijo_de.grid(row=7, column=1, pady=8, padx=10)

        l_localidad_r = ttkb.Label(x, text='Localidad de residencia:', font=(
            'Time New Roman', 14), borderwidth=3, relief="groove", anchor=W).grid(row=8, column=0, sticky="nsew", pady=8)
        localidad_r = ttkb.Entry(x, width=40, font=(16))
        localidad_r.grid(row=8, column=1, pady=8, padx=10)
        validar_Enreys_Solo_Letras(localidad_r)

        l_Tit_DNITIT = ttkb.Label(x, text='DNI Titular', font=(
            'Time New Roman', 14), borderwidth=3, relief="groove", anchor=W).grid(row=9, column=0, sticky="nsew", pady=8)
        Tit_DNITIT = ttkb.Entry(x, width=40, font=(16))
        Tit_DNITIT.grid(row=9, column=1, pady=8, padx=10)
        validar_Enreys_Solo_Numeros(Tit_DNITIT)
        # ---------------------------------------------------------------------#

        def guardar():
            """_summary_
                Guarda los datos y aplica el button guardar el cual si un campo no esta completo se le da un mensaje al usuario.
            """

            if not dni.get():
                Messagebox.show_error(
                    'El campo "DNI" es obligatorio.', 'Error')
                top.lift()
                return
            elif not nombre.get():
                Messagebox.show_error(
                    'El campo "Nombre/s" es obligatorio.', 'Error')
                top.lift()
                return
            elif not apellido.get():
                Messagebox.show_error(
                    'El campo "Apellido/s" es obligatorio.', 'Error')
                top.lift()
                return
            elif not cuil_cuit.get:
                Messagebox.show_error(
                    'El campo "CUIL / CUIT" es obligatorio.''Error')
                top.lift()
                return
            elif not fNacimiento.entry.get():
                Messagebox.show_error(
                    'El campo "Fecha de Nacimiento" es obligatorio.', 'Error')
                top.lift()
                return

            elif not value.get():
                Messagebox.show_error(
                    'El campo "Mail" es obligatorio.', 'Error')
                top.lift()
                return
            elif not localidad_r.get():
                Messagebox.show_error(
                    'El campo "Localidad de residencia" es obligatorio.', 'Error')
                top.lift()
                return

            try:
                # si los campos fueron llenados con exito, agrupa los mismos en un diccionarios para despues usarlos para guardar en su respectiva tabla
                
                ahora = datetime.date(datetime.now())

                nom = validar_nombre_sin_espacios(nombre.get()) # limpia el nombre
                ape = validar_apellido_sin_espacios(apellido.get()) # limpia el apellido

                resultados = {
                    'DNIHIJ': int(dni.get()),
                    'NOMHIJ': nom.upper(),
                    'APEHIJ': ape.upper(),
                    'CUIL_CUIT_HIJ': int(cuil_cuit.get()),
                    'FNAHIJ': fNacimiento.entry.get(),
                    'LOCHIJ': localidad_r.get().upper(),
                    'PDSHIJ': str(value.get()),
                    'FCHHIJ': ahora,
                    'DNITIT_HIJO': int(Tit_DNITIT.get())
                }
                rows = c.execute(
                    """SELECT * From Hijo WHERE DNIHIJ = ?""", (resultados['DNIHIJ'], )).fetchall()

                if not rows:
                    # Messagebox.show_info(
                    #     '¡¡¡EL contenido fue Enviado con éxito 👌!!!', 'Enviado')
                    insertar_Hijo(resultados)
                    top.destroy()
                else:
                    Messagebox.show_error(
                        f'Ya existe un registro con el DNI: {resultados["DNIHIJ"]}', 'Error')
                    top.lift()
                    return

            except ValueError:
                Messagebox.show_warning(
                    'Verifique los CAMPOS', 'Error en algun Campo')
                top.lift()

        btn_guardar = ttkb.Button(top, text='Guardar', command=guardar)
        btn_guardar.grid(column=2, row=3, padx=15, pady=15)
        top.mainloop()
        # ---------------------------------------------------------------------#
    Hijo = datos()


#   Insertar Resultado de LLamada
def insertar_resultado_llamada(resultados):
    """Inserta en la tabla Llamados_Ventas lo recopilado al guardar"""
    c.execute("""
        INSERT INTO Llamados_Ventas (RESLVEN,VENTLVEN,FCHLVEN,Titular_DNITIT) VALUES(?,?,?,?)
    """, (resultados['RESULT_LLAMADO'], resultados['VENTA'], resultados['FECHA_VENTA'], resultados['LVENT_DNITIT']))
    conn.commit()


#   Carga de Resultado de LLamada
def cargar_llamada():
    """Carga los resultados de las llamada a los clientes.
    """
    top = Toplevel()
    top.title('Carga de Resultado de LLamada')
    top.resizable(False, False)
    icono = ruta_archivo
    top.iconbitmap(icono)
    top.resizable(False,False)

    def datos():
        x = ttkb.LabelFrame(top, text='Datos Llamada', padding=5,
                            borderwidth=3, relief="ridge")
        x.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)
        #   DNI
        l_dni = ttkb.Label(x, text='DNI:',  font=('Time New Roman', 14),
                           borderwidth=3, relief="groove", anchor=W).grid(row=0, column=0, sticky="nsew", pady=8)
        dni = ttkb.Entry(x, width=40, font=(16))
        dni.grid(row=0, column=1, pady=8, padx=10)
        validar_Enreys_Solo_Numeros(dni)
        #   VENTA
        lventa = ttkb.Label(x, text='Vendido',  font=('Time New Roman', 14),
                            borderwidth=3, relief="groove", anchor=W).grid(row=1, column=0, sticky="nsew", pady=8)
        lista_datos = ['-----------',
                       'Si',
                       'No'
                       ]
        # value es el valor asignado de la lista desplegable
        resultado_vendido = StringVar()
        resultado_vendido.set(lista_datos[0])
        ventas = OptionMenu(x, resultado_vendido, *lista_datos)
        ventas.grid(row=1, column=1, pady=8, padx=10)
        #   Breve descripcion del Resultado del Llamado.
        lresult_llamado = ttkb.Label(x, text='Resultado \n     del\n Llamado ',  font=('Time New Roman', 14),
                                     borderwidth=3, relief="groove", anchor=W).grid(row=2, column=0, sticky="nsew", pady=8)
        result_llamado = ttkb.Entry(x, font=(16), width=100)
        result_llamado.grid(row=2, column=1, padx=10, pady=8)

        def guardar():
            if not dni.get():
                Messagebox.show_error(
                    'El campo "DNI" es obligatorio.', 'Error')
                top.lift()
                return
            elif not resultado_vendido.get():
                Messagebox.show_error(
                    'El campo "Vendido" es obligatorio.', 'Error')
                top.lift()
            try:
                # si los campos fueron llenados con exito, agrupa los mismos en un diccionarios para despues usarlos para guardar en su respectiva tabla
                ahora = datetime.date(datetime.now())
                resultados = {'LVENT_DNITIT': dni.get(),
                              'VENTA': str(resultado_vendido.get()),
                              'FECHA_VENTA': ahora,
                              'RESULT_LLAMADO': result_llamado.get()
                              }
                # Messagebox.show_info(
                #     '¡¡¡EL contenido fue Guardado con éxito 👌!!!', 'Guardado')
                insertar_resultado_llamada(resultados)
                top.destroy()
            except ValueError:
                Messagebox.show_warning(
                    'Verifique los CAMPOS', 'Error en algun Campo')
                top.lift()

        btn_guardar = ttkb.Button(top, text='Guardar', command=guardar)
        btn_guardar.grid(column=2, row=3, padx=15, pady=15)
    datos()
    top.mainloop()


#   Buscar Resultados de llamada
def buscar_llamadas():
    top = Toplevel()
    top.title('Buscar')
    icono = ruta_archivo
    top.iconbitmap(icono)
    top.resizable(False,False)
    estilo = ttkb.Style()
    estilo.configure("mystyle.Treeview", font=(
        'Time New Roman', 10), background='#DCE6F2', foreground='#000')

    def extraer_datos_dni(dato):
        rows = c.execute(
            '''SELECT * FROM Llamados_Ventas WHERE Titular_DNITIT = ?''', (dato['DNI'], )).fetchall()
        if not rows:
            Messagebox.show_warning(
                f'No existe ningun registro con el DNI {dato["DNI"]}', 'Error')
            top.lift()
        tree.delete(*tree.get_children())
        cont = 0  # contador
        for row in rows:
            tree.insert('', END, row[0], values=(
                row[4], row[2], row[1], row[3], row[0]))
            cont += 1
        lcont = ttkb.Label(x, text=f'Cantidad de llamadas al usuario {dato["DNI"]}: [ {cont} ] ', foreground='#000', font=('Time New Roman', 14), borderwidth=3,
                           relief="groove", anchor=W, pad=2, background='#ffd777').grid(row=2, column=3, sticky="nsew", pady=8, padx=10)

    def buscar():
        # gurada los datos en diccionarios para despues poder hacer el select correspondiente
        try:
            dato = {'DNI': dni.get()}
            extraer_datos_dni(dato)
        except ValueError:
            Messagebox.show_warning(
                'Verifique los CAMPOS', 'Error en algun Campo')
            top.lift()

    h = ttkb.Frame(top,
                   padding=5, borderwidth=3, relief="ridge")
    h.pack(pady=10, padx=4)

    # Create scrollbar Y
    tree_scroollbar_y = ttk.Scrollbar(h,bootstyle="warning-round")
    tree_scroollbar_y.pack(side=RIGHT, fill=Y)

    # Create scrollbar X
    tree_scroollbar_x = ttk.Scrollbar(h, orient='horizontal',bootstyle="warning-round")
    tree_scroollbar_x.pack(side=BOTTOM, fill=X)

    # create treeview
    tree = ttkb.Treeview(h, bootstyle='success', style="mystyle.Treeview",
                         yscrollcommand=tree_scroollbar_y.set, xscrollcommand=tree_scroollbar_x.set)
    tree.columnconfigure(0, weight=1)
    tree.rowconfigure(0, weight=1)

    # configuyara scrollbar y
    tree_scroollbar_y.config(command=tree.yview)
    tree_scroollbar_x.config(command=tree.xview)

    #   Grilla de datos
    tree['columns'] = ('DNI', 'VENTA', 'RESULT_LLAMADO', 'FECHA_VENTA', 'ID')
    tree.column('#0', width=0, stretch=NO)
    tree.column('DNI', anchor=CENTER)
    tree.column('VENTA', anchor=CENTER)
    tree.column('RESULT_LLAMADO', anchor=CENTER)
    tree.column('FECHA_VENTA', anchor=CENTER)
    tree.column('ID', anchor=CENTER)

    tree.heading('DNI', text='DNI', anchor=CENTER)
    tree.heading('VENTA', text='Vendido', anchor=CENTER)
    tree.heading('RESULT_LLAMADO', text='Resultado del Llamado', anchor=CENTER)
    tree.heading('FECHA_VENTA', text='Fecha Realizado', anchor=CENTER)
    tree.heading('ID', text='ID', anchor=CENTER)
    tree.pack()

    x = ttkb.LabelFrame(top, text='Buscar Llamado',
                        padding=5, borderwidth=3, relief="ridge")
    x.pack(before=h, pady=10, padx=4)
    l_dni = ttkb.Label(x, text='DNI TITULAR:', font=('Time New Roman', 14), borderwidth=3,
                       relief="groove", anchor=W, pad=2).grid(row=0, column=3, sticky="nsew", pady=8, padx=10)
    dni = ttkb.Entry(x, width=40, font=(16))
    dni.grid(row=0, column=4, pady=8, padx=10)
    validar_Enreys_Solo_Numeros(dni)
    btn_buscar_dni = ttkb.Button(
        x, text='Buscar', bootstyle='info-outline', command=lambda: buscar())
    btn_buscar_dni.grid(row=0, column=5, sticky='ew')
    top.mainloop()





#   Buscar Ventas en el mes
def buscar_ventas_mes():
    top = Toplevel()
    top.title('Buscar Ventas')
    icono = ruta_archivo
    top.iconbitmap(icono)
    estilo = ttkb.Style()
    top.resizable(False,False)
    estilo.configure("mystyle.Treeview", font=(
        'Time New Roman', 10), background='#DCE6F2', foreground='#000')

    def extraer_datos_dni(dato):
        rows = c.execute(
            f"""SELECT * FROM Llamados_Ventas WHERE FCHLVEN BETWEEN '{dato['ANIO']}-{dato['MES']}-01' AND '{dato['ANIO']}-{dato['MES']}-31' AND VENTLVEN LIKE 'Si'""").fetchall()
        # if not rows:
        #     Messagebox.show_warning(
        #         f'No existe ningun registro con el DNI {dato["DNI"]}', 'Error')
        tree.delete(*tree.get_children())
        cont = 0  # contador
        for row in rows:
            tree.insert('', END, row[0], values=(
                row[4], row[2], row[1], row[3], row[0]))
            cont += 1
        lcont = ttkb.Label(x, text=f'Cantidad vendidas en el Mes: [ {cont} ] ', foreground='#000', font=('Time New Roman', 14), borderwidth=3,
                           relief="groove", anchor=W, pad=2, background='#ffd777').grid(row=2, column=3, sticky="nsew", pady=8, padx=10)

    def buscar():

        # gurada los datos en diccionarios para despues poder hacer el select correspondiente
        try:
            dato = {'MES': str(MES.get()),
                    'ANIO': str(ANIO.get()),
                    'VENTA': 'Si'}
            extraer_datos_dni(dato)
        except ValueError:
            Messagebox.show_warning(
                'Verifique los CAMPOS', 'Error en algún Campo')
            top.lift()

    h = ttkb.Frame(top,
                   padding=5, borderwidth=3, relief="ridge")
    h.pack(padx=4, pady=10)

    # Create scrollbar Y
    tree_scroollbar_y = ttk.Scrollbar(h,bootstyle="warning-round")
    tree_scroollbar_y.pack(side=RIGHT, fill=Y)
    # Create scrollbar X
    tree_scroollbar_x = ttk.Scrollbar(h, orient='horizontal',bootstyle="warning-round")
    tree_scroollbar_x.pack(side=BOTTOM, fill=X)

    # create treeview
    tree = ttkb.Treeview(h, bootstyle='success', style="mystyle.Treeview",
                         yscrollcommand=tree_scroollbar_y.set, xscrollcommand=tree_scroollbar_x.set)
    tree.columnconfigure(0, weight=1)
    tree.rowconfigure(0, weight=1)

    # Configurate scrollbar
    tree_scroollbar_y.config(command=tree.yview)
    tree_scroollbar_x.config(command=tree.xview)

    #   Grilla de datos
    tree['columns'] = ('DNI', 'VENTA', 'RESULT_LLAMADO', 'FECHA_VENTA', 'ID')
    tree.column('#0', width=0, stretch=NO)
    tree.column('DNI', anchor=CENTER)
    tree.column('VENTA', anchor=CENTER)
    tree.column('RESULT_LLAMADO', anchor=CENTER)
    tree.column('FECHA_VENTA', anchor=CENTER)
    tree.column('ID', anchor=CENTER)

    tree.heading('DNI', text='DNI', anchor=CENTER)
    tree.heading('VENTA', text='Vendido', anchor=CENTER)
    tree.heading('RESULT_LLAMADO', text='Resultado del Llamado', anchor=CENTER)
    tree.heading('FECHA_VENTA', text='Fecha Realizado', anchor=CENTER)
    tree.heading('ID', text='ID', anchor=CENTER)
    tree.pack()

    x = ttkb.LabelFrame(top, text='Buscar Ventas',
                        padding=5, borderwidth=3, relief="ridge")
    x.pack(before=h, pady=10, padx=4)

    ejemplo_MES = StringVar()
    ejemplo_MES.set('Ejemplo: 07')
    l_MES = ttkb.Label(x, text='Mes a buscar:', font=('Time New Roman', 14), borderwidth=3,
                       relief="groove", anchor=W, pad=2).grid(row=0, column=3, sticky="nsew", pady=8, padx=10)
    MES = ttkb.Entry(x, textvariable=ejemplo_MES, width=12, font=(16))
    MES.grid(row=0, column=4, pady=8, padx=10)
    validar_Enreys_Solo_Numeros(MES)

    ejemplo_ANIO = StringVar()
    ejemplo_ANIO.set('Ejemplo: 2023')
    l_ANIO = ttkb.Label(x, text='Año a buscar:', font=('Time New Roman', 14), borderwidth=3,
                        relief="groove", anchor=W, pad=2).grid(row=1, column=3, sticky="nsew", pady=8, padx=10)
    ANIO = ttkb.Entry(x, textvariable=ejemplo_ANIO, width=12, font=(16))
    ANIO.grid(row=1, column=4, pady=8, padx=10)
    validar_Enreys_Solo_Numeros(ANIO)

    btn_buscar = ttkb.Button(
        x, text='Buscar', bootstyle='info-outline', command=buscar)
    btn_buscar.grid(row=1, column=5, sticky='ew')
    top.mainloop()


#   Insertar Cotizacion datos
def insertar_cot(resultados):
    """Inserta en la tabla Cotizacion lo recopilado al guardar"""
    c.execute("""
        INSERT INTO Cotizacion (TIPCOT,TRESAPOR,SBRUT,FHINGL,CATCOT,PERAPORT,COBACTU,PREPAGA,PLANCOT,MOTCAMB,FCHCOT,DATREF,Titular_DNITIT) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (resultados['TIPO_COT'], resultados['3%APORTE'], resultados['SUELDO_BRUT'], resultados['FECH_ING'], resultados['CONDICION_IVA'], resultados['PERS_APORT'], resultados['COBERT_ACTUAL'],
            resultados['PREPAGA'], resultados['PLAN'], resultados['MOTIVO'],resultados['FCHCOT'], resultados['POR_QUIEN'], resultados['DNI']))
    conn.commit()


def carga_cotizacion():
    top = Toplevel()
    top.title('Carga Cotización')
    top.resizable(False, False)
    icono = ruta_archivo
    top.iconbitmap(icono)
    top.resizable(False,False)

    def datos():
        def desactivar_widgets():
            if value.get() == 'Particular':
                personas_aportan.configure(state="disabled")
                sueldo_bruto.configure(state="disabled")
            else:
                personas_aportan.configure(state="normal")
                sueldo_bruto.configure(state="normal")

        x = ttkb.LabelFrame(top, text='Cotización Titular', padding=5,
                            borderwidth=3, relief="ridge")
        x.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

        l_dni = ttkb.Label(x, text='DNI Titular:', font=('Time New Roman', 14),
                           borderwidth=3, relief="groove", anchor=W).grid(row=0, column=0, sticky="nsew", pady=8)
        dni = ttkb.Entry(x, width=40, font=(16))
        dni.grid(row=0, column=1, pady=8, padx=10)
        validar_Enreys_Solo_Numeros(dni)

        l_cot_tipo = ttkb.Label(x, text='Tipo de Cotización: ', font=(
            'Time New Roman', 14), borderwidth=3, anchor=W, relief='groove').grid(row=1, column=0, sticky="nsew", pady=8)
        lista_datos = ['-----------',
                       'Particular',
                       'Con Aportes'
                       ]
        # value es el valor asignado de la lista desplegable
        value = StringVar()
        value.set(lista_datos[0])
        cot_tipo = OptionMenu(x, value, *lista_datos)
        cot_tipo.grid(row=1, column=1, pady=8, padx=10)
        
        lsueldo_bruto = ttkb.Label(x, text='Sueldo Bruto:', font=(
            'Time New Roman', 14), borderwidth=3, anchor=W, relief='groove').grid(row=2, column=0, sticky="nsew", pady=8)
        sueldo_bruto = ttkb.Entry(x, width=40, font=(16))
        sueldo_bruto.grid(row=2, column=1, padx=10, pady=8)

        if value.get() == 'Particular':
            personas_aportan.configure(state="disabled")
            sueldo_bruto.configure(state="disabled")

        
        # =/0.03 sueldo bruto SOBRE EL 3%   -----> pendiente
        # lTres_porciento_aporte = ttkb.Label(x, text='3% Aporte a la Obra Social:', font=(
        #     'Time New Roman', 14), borderwidth=3, anchor=W, relief='groove').grid(row=3, column=0, sticky='nsew', pady=8)
        # Tres_porciento_aporte = ttkb.Entry(x, width=40, font=(16))
        # Tres_porciento_aporte.grid(row=3, column=1, pady=8, padx=10)

        defecto = StringVar()
        defecto.set('dd-mm-aaaa')
        lfch_ing_lab = ttkb.Label(x, text='Fecha de ingreso laboral:', font=(
            'Time New Roman', 14), borderwidth=3, anchor=W, relief='groove').grid(row=4, column=0, sticky='nsew', pady=8)
        fch_ing_lab = ttkb.Entry(x, textvariable=defecto, width=40, font=(16))
        fch_ing_lab.grid(row=4, column=1, padx=10, pady=8)

        lcondicion_frente_al_IVA = ttkb.Label(x, text='Condición frente al IVA:', font=(
            'Time New Roman', 14), borderwidth=3, anchor=W, relief='groove').grid(row=5, column=0, pady=8, sticky='nsew')
        catcondicion_frente_al_IVA = ttkb.Entry(x, width=40, font=(16))
        condicion = ['-----------',
                     'Inscripto',
                     'Consumidor Final',
                     'Monotributista'
                     ]
        # value es el valor asignado de la lista desplegable
        var = StringVar()
        var.set(condicion[0])
        catcondicion_frente_al_IVA = OptionMenu(x, var, *condicion)
        catcondicion_frente_al_IVA.grid(row=5, column=1, pady=8, padx=10)

        lpersonas_aportan = ttkb.Label(x, text='Por cuantas personas aporta?', font=(
            'Time New Roman', 14), borderwidth=3, anchor=W, relief='groove').grid(row=6, column=0, sticky='nsew', pady=8)
        personas_aportan = ttkb.Entry(x, width=40, font=(16))
        personas_aportan.grid(row=6, column=1, padx=10, pady=8)

        lcob_actual = ttkb.Label(x, text='Cobertura actual:', font=(
            'Time New Roman', 14), borderwidth=3, anchor=W, relief='groove').grid(row=7, column=0, sticky='nsew', pady=8)
        cob_actual = ttkb.Entry(x, width=40, font=(16))
        cob_actual.grid(row=7, column=1, padx=10, pady=8)

        lprepaga = ttkb.Label(x, text='Prepaga:', font=('Time New Roman', 14), borderwidth=3,
                              anchor=W, relief='groove').grid(row=7, column=2, sticky='nsew', pady=8)
        opciones = ['-----------',
                    'Si',
                    'No'
                    ]
        # value es el valor asignado de la lista desplegable
        prep = StringVar()
        prep.set(opciones[0])
        prepaga = OptionMenu(x, prep, *opciones)
        prepaga.grid(row=7, column=3, pady=8, padx=10)

        lplan = ttkb.Label(x, text='Plan:', font=('Time New Roman', 14), borderwidth=3,
                           anchor=W, relief='groove').grid(row=8, column=0, sticky='nsew', pady=8)
        plan = ttkb.Entry(x, width=40, font=(16))
        plan.grid(row=8, column=1, padx=10, pady=8)

        lmotivo_cambio = ttkb.Label(x, text='Motivo por el que quiere cambiar de cobertura?', font=(
            'Time New Roman', 14), borderwidth=3, anchor=W, relief='groove').grid(row=9, column=0, sticky='nsew', pady=8)
        motivo_cambio = ttkb.Entry(x, width=40, font=(16))
        motivo_cambio.grid(row=9, column=1, padx=10, pady=8)

        lpor_quien_contacto = ttkb.Label(x, text='A traves de quien o qué llegaste a contactarme?', font=(
            'Time New Roman', 14), borderwidth=3, anchor=W, relief='groove').grid(row=10, column=0, sticky='nsew', pady=8)
        por_quien_contacto = ttkb.Entry(x, width=40, font=(16))
        por_quien_contacto.grid(column=1, row=10, padx=10, pady=8)

        def guardar():
            if not dni.get():
                Messagebox.show_warning(
                    'El campo "DNI" es obligatorio.', 'Error')
                top.lift()
                return
            if value == '-----------':
                Messagebox.show_warning(
                    'El campo "Tipo de Cotización" es obligatorio.', 'Error')
                top.lift()
            # if not Tres_porciento_aporte.get():
            #     Messagebox.show_error(
            #         'El campo "3% Aporte a la Obra Social" es obligatorio.', 'Error')
            if not sueldo_bruto.get():
                Messagebox.show_warning(
                    'El campo "Seldo Bruto" es obligatorio.', 'Error')
                top.lift()
            if var == '-----------':
                Messagebox.show_warning(
                    'El campo "Condición frente al IVA" es obligatorio.', 'Error')
                top.lift()
            if not personas_aportan.get():
                Messagebox.show_warning(
                    'El campo "Por cuantas personas aporta" es obligatorio.', 'Error')
                top.lift()
            if not cob_actual.get():
                Messagebox.show_warning(
                    'El campo "Cobertura actual" es obligatorio.', 'Error')
                top.lift()
            if prep == '-----------':
                Messagebox.show_warning(
                    'El campo "Prepaga" es obligatorio.', 'Error')
                top.lift()
            if not plan.get():
                Messagebox.show_warning(
                    'El campo "Plan" es obligatorio.', 'Error')
                top.lift()
            if not motivo_cambio.get():
                Messagebox.show_warning(
                    'El campo "Motivo por el que quiere cambiar de cobertura" es obligatorio.', 'Error')
                top.lift()
            if not por_quien_contacto.get():
                Messagebox.show_warning(
                    'El campo "A traves de quien o qué llegaste a contactarme" es obligatorio.', 'Error')
                top.lift()
            # Cálculo y redondeo
            sueldo_bruto_int :int = int(sueldo_bruto.get())
            Tres_porciento_aporte = sueldo_bruto_int * 0.0745
            Tres_porciento_aporte = round(Tres_porciento_aporte,2)
            
            
            
                # si los campos fueron llenados con exito, agrupa los mismos en un diccionarios para despues usarlos para guardar en su respectiva tabla
            try:
                ahora = datetime.date(datetime.now())
                resultados = {'DNI': dni.get(),
                              'TIPO_COT': str(value.get()),
                              '3%APORTE':Tres_porciento_aporte,
                              'SUELDO_BRUT': sueldo_bruto.get(),
                              'FECH_ING': fch_ing_lab.get(),
                              'CONDICION_IVA': str(var.get()),
                              'PERS_APORT': personas_aportan.get(),
                              'COBERT_ACTUAL': cob_actual.get(),
                              'PREPAGA': str(prep.get()),
                              'PLAN': plan.get(),
                              'MOTIVO': motivo_cambio.get(),
                              'FCHCOT': ahora,
                              'POR_QUIEN': por_quien_contacto.get()}
                # Messagebox.show_info(
                #     '¡¡¡EL contenido fue Guardado con éxito 👌!!!', 'Guardado')
                insertar_cot(resultados)
                top.destroy()
            except ValueError:
                Messagebox.show_warning(
                    'Verifique los CAMPOS', 'Error en algun Campo')
                top.lift()

        btn_guardar = ttkb.Button(top, text='Guardar', command=guardar)
        btn_guardar.grid(column=2, row=3, padx=15, pady=15)

    datos()


def buscar_Cotizacion():
    top = Toplevel()
    top.title('Buscar')
    # Obtiene el tamaño de la pantalla
    # screen_width = root.winfo_screenwidth()
    # screen_height = root.winfo_screenheight()

    # Establece el tamaño de la ventana principal
    # top.geometry(f"{screen_width-100}x{screen_height-100}")
    top.geometry('1340x612')
    icono = ruta_archivo
    top.iconbitmap(icono)
    estilo = ttkb.Style()
    estilo.configure("mystyle.Treeview", font=(
        'Time New Roman', 10), background='#DCE6F2', foreground='#000')

    def extraer_datos_dni(dato):
        # Establecer la configuración local a la convención de Argentina
        locale.setlocale(locale.LC_ALL, 'es_AR.UTF-8')
        rows = c.execute(
            """SELECT * FROM Cotizacion WHERE Titular_DNITIT=? AND ELICOT='NO'""", (dato['DNI'], )).fetchall()
        if not rows:
            Messagebox.show_warning(
                f'No existe ningun registro con el DNI: {dato["DNI"]}', 'Error')
            top.lift()
        
        for row in rows:
            tree.insert('', END, row[0], values=(
                row[14], row[1], f"${locale.format_string('%d',int(row[2]),grouping=True)}", f"${locale.format_string('%d',int(row[3]),grouping=True)}",
                        row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]))

    def buscar():
        # gurada los datos en diccionarios para despues poder hacer el select correspondiente
        try:
            dato = {'DNI': dni.get()}
            extraer_datos_dni(dato)
        except ValueError:
            Messagebox.show_warning(
                'Verifique los CAMPOS', 'Error en algún Campo')
            top.lift()

    # creando frame
    h = ttkb.Frame(top, padding=5, borderwidth=3, relief="ridge")
    h.pack(padx=4, pady=10)

    # Create scrollbar Y
    tree_scroollbar_y = ttk.Scrollbar(h,bootstyle="warning-round")
    tree_scroollbar_y.pack(side=RIGHT, fill=Y)

    # Create scrollbar X
    tree_scroollbar_x = ttk.Scrollbar(h, orient='horizontal',bootstyle="warning-round")
    tree_scroollbar_x.pack(side=BOTTOM, fill=X)

    # create Treeview
    tree = ttk.Treeview(h, bootstyle='success', style="mystyle.Treeview",
                        yscrollcommand=tree_scroollbar_y.set, xscrollcommand=tree_scroollbar_x.set)
    tree.columnconfigure(0, weight=1)
    tree.rowconfigure(0, weight=1)

    # configurate scrollbar
    tree_scroollbar_x.config(command=tree.xview)
    tree_scroollbar_y.config(command=tree.yview)

    #   Grilla de datos
    tree['columns'] = ('DNITIT_COT', 'TIPO_COT', 'TRES_POR_APORTE', 'SUELDO_BRUTO', 'FCH_ING_LAB',
                       'CATEGORIA', 'PER_APORTA', 'COB_ACTUAL', 'PREPAGA', 'PLAN', 'MOTIVO_CAMBIO', 'DAT_REF')
    tree.column('#0', width=0, stretch=NO)
    tree.column('DNITIT_COT', width=80, anchor=CENTER)
    tree.column('TIPO_COT', anchor=CENTER)
    tree.column('TRES_POR_APORTE', anchor=CENTER)
    tree.column('SUELDO_BRUTO', anchor=CENTER)
    tree.column('FCH_ING_LAB', anchor=CENTER)
    tree.column('CATEGORIA', anchor=CENTER)
    tree.column('PER_APORTA', anchor=CENTER)
    tree.column('COB_ACTUAL', anchor=CENTER)
    tree.column('PREPAGA', width=80, anchor=CENTER)
    tree.column('PLAN', width=80, anchor=CENTER)
    tree.column('MOTIVO_CAMBIO', anchor=CENTER)
    tree.column('DAT_REF', anchor=CENTER)

    tree.heading('DNITIT_COT', text='DNI Titular', anchor=CENTER)
    tree.heading('TIPO_COT', text='Tipo de Cotización', anchor=CENTER)
    tree.heading('TRES_POR_APORTE', text='3% Aporte', anchor=CENTER)
    tree.heading('SUELDO_BRUTO', text='Seldo Bruto', anchor=CENTER)
    tree.heading('FCH_ING_LAB', text='Fecha de ingreso laboral', anchor=CENTER)
    tree.heading('CATEGORIA', text='Condición frente al IVA', anchor=CENTER)
    tree.heading('PER_APORTA', text='Personas Aporta', anchor=CENTER)
    tree.heading('COB_ACTUAL', text='Cobertura actual', anchor=CENTER)
    tree.heading('PREPAGA', text='Prepaga', anchor=CENTER)
    tree.heading('PLAN', text='Plan', anchor=CENTER)
    tree.heading('MOTIVO_CAMBIO', text='Motivo de Cambio')
    tree.heading('DAT_REF', text='Medio de Contacto')
    tree.pack()

    x = ttkb.LabelFrame(top, text=f'Buscar Cotización',
                        padding=5, borderwidth=3, relief="ridge")
    x.pack(before=h, padx=4, pady=10)
    l_dni = ttkb.Label(x, text='DNI TITULAR:', font=('Time New Roman', 14), borderwidth=3,
                       relief="groove", anchor=W, pad=2).grid(row=0, column=3, sticky="nsew", pady=8, padx=10)
    dni = ttkb.Entry(x, width=40, font=(16))
    dni.grid(row=0, column=4, pady=8, padx=10)
    validar_Enreys_Solo_Numeros(dni)
    btn_buscar_dni = ttkb.Button(
        x, text='Buscar', bootstyle='info-outline', command=buscar)
    btn_buscar_dni.grid(row=0, column=5, sticky='ew')

    top.mainloop()

# Buscar registros, tanto eliminados como no eliminados
def buscar(tipo):
    """buscar_dni
        Lo que hace es tomar el DNI ingresado segun de (quien) lo solicita si es Hijo, cónyuge o  Titular.

        return: todos los datos relacionados con el individuo, no los de cotización u otros.
    """
    tipo = str(tipo)
    top = Toplevel()
    top.title('Buscar')
    icono = ruta_archivo
    top.iconbitmap(icono)
    top.resizable(False,False)

    estilo = ttkb.Style()
    estilo.configure("mystyle.Treeview", font=(
        'Time New Roman', 10), background='#DCE6F2', foreground='#000')
    
    # devuelve los registros a la lista blanca para que aparezca en la busqueda normal
    def devolver_registro(tree,quien,top2):
        if quien == 'Titular':
            id = tree.selection()[0]
            respuesta = Messagebox.okcancel('¿de querer recuperar este dato?','¿Seguro?' )
            top2.lift()
            if respuesta:
                c.execute("UPDATE  Titular SET ELITIT = 'NO' WHERE DNITIT=?", (id, ))
                c.execute("UPDATE  Conyuge SET ELICON = 'NO' WHERE Titular_DNITIT=?", (id, ))
                c.execute(
                        "UPDATE  Hijo SET ELIHIJ = 'NO' WHERE Titular_DNITIT=?",  (id, ))
                c.execute(
                        "UPDATE  Cotizacion SET ELICOT = 'NO' WHERE Titular_DNITIT=?",  (id, ))
                c.execute(
                        "UPDATE  Llamados_Ventas SET ELILVEN = 'NO' WHERE Titular_DNITIT=?",  (id, ))
                conn.commit()
            else:
                pass
        if quien =='Conyuge':
            id = tree.selection()[0]
            respuesta = Messagebox.okcancel('¿de querer recuperar este dato?','¿Seguro?' )
            top2.lift()
            if respuesta:
                c.execute("UPDATE  Conyuge SET ELICON = 'NO' WHERE DNICON=?", (id, ))
                conn.commit()
            else:
                pass
        
        if quien == 'Hijo/s':
            id = tree.selection()[0]
            respuesta = Messagebox.okcancel('¿de querer recuperar este dato?','¿Seguro?' )
            top2.lift()
            if respuesta:
                c.execute("UPDATE  Hijo SET ELIHIJ = 'NO' WHERE DNIHIJ=?", (id, ))
                conn.commit()
            else:
                pass
        tree.delete(*tree.get_children())
            
        

    def extraer_datos_dni(quien, dato, tree,tipo):
        quien = str(quien)
        '''define si es buscar o ver_papelera, para identificar si el llamado es para ver los que no estan "eliminados"(buscar)
            o si el llamado es para ver los "eliminados"(ver_papelera).'''
        tipo = str(tipo)    
        if tipo == 'buscar':
            # --------------------------------------------------#
            if quien == 'Titular':
                if len(dato['Nom']) > 0 and len(dato['Ape']) > 0:
                    rows = c.execute(
                        """SELECT * From Titular WHERE NOMTIT = ? AND APETIT = ? AND ELITIT='NO'""", (dato['Nom'], dato['Ape'])).fetchall()

                else:
                    rows = c.execute(
                        """SELECT * From Titular WHERE DNITIT=? AND ELITIT='NO'""", (dato['DNI'], )).fetchall()

            # --------------------------------------------------#
            if quien == 'TODOS':
                rows = c.execute(
                    """SELECT * From Titular WHERE ELITIT='NO'""").fetchall()

            # --------------------------------------------------#
            if quien == 'Conyuge':
                if len(dato['Nom']) > 0 and len(dato['Ape']) > 0:
                    rows = c.execute(
                        """SELECT * From Conyuge WHERE NOMCON=? AND APECON=? AND ELICON='NO'""", (dato['Nom'], dato['Ape'], )).fetchall()
                else:
                    rows = c.execute(
                        """SELECT * From Conyuge WHERE DNICON = ? AND ELICON='NO'""", (dato['DNI'], )).fetchall()

            # --------------------------------------------------#
            if quien == 'Titular_DNITIT':
                rows = c.execute(
                    """SELECT * From Conyuge WHERE Titular_DNITIT=? AND ELICON='NO'""", (dato['DNI'], )).fetchall()

            # --------------------------------------------------#
            if quien == 'Hijo/s':
                if len(dato['Nom']) > 0 and len(dato['Ape']) > 0:
                    rows = c.execute(
                        """SELECT * From Hijo WHERE NOMHIJ=? AND APEHIJ=? AND ELIHIJ='NO'""", (dato['Nom'], dato['Ape'], )).fetchall()
                else:
                    rows = c.execute(
                        """SELECT * From Hijo WHERE DNIHIJ=? AND ELIHIJ='NO'""", (dato['DNI'], )).fetchall()

            # --------------------------------------------------#
            if quien == 'DNITIT_HIJO':
                rows = c.execute(
                    """SELECT * From Hijo WHERE Titular_DNITIT=? AND ELIHIJ='NO'""", (dato['DNI'], )).fetchall()

            # --------------------------------------------------#

            if not rows:
                Messagebox.show_warning(
                    f'No existe ningun registro con ese DNI{dato["DNI"]}', 'Error')
                
            tree.delete(*tree.get_children())
            fecha_actual = datetime.now()
            if  quien == 'Conyuge' or quien == 'Titular_DNITIT' :
                for row in rows:
                    edad = definir_edad(row[4])
                    tree.insert('', END, row[0], values=(
                        row[0], row[1], row[2], row[3], row[4], edad, row[5], row[6], row[7], row[10]))
            if quien == 'Hijo/s' or quien == 'DNITIT_HIJO':
                for row in rows:
                    edad = definir_edad(row[4])
                    if edad >= 18:
                        mayor = 'Si'
                    else:
                        mayor = 'No'
                    
                    tree.insert('', END, row[0], values=(
                        row[0], row[1], row[2], row[3], row[4], edad, mayor, row[5], row[6], row[9]))
            if quien == 'Titular' or quien == 'TODOS':
                for row in rows:
                    edad = definir_edad(row[4])
                    tree.insert('', END, row[0], values=(
                        row[0], row[1], row[2], row[3], row[4], edad, row[5], row[6], row[7], row[9]))
        
        elif tipo == 'ver_papelera':
            # --------------------------------------------------#
            if quien == 'Titular':
                if len(dato['Nom']) > 0 and len(dato['Ape']) > 0:
                    rows = c.execute(
                        """SELECT * From Titular WHERE NOMTIT = ? AND APETIT = ? AND ELITIT='SI'""", (dato['Nom'], dato['Ape'])).fetchall()

                else:
                    rows = c.execute(
                        """SELECT * From Titular WHERE DNITIT=? AND ELITIT='SI'""", (dato['DNI'], )).fetchall()

            # --------------------------------------------------#
            if quien == 'TODOS':
                rows = c.execute(
                    """SELECT * From Titular WHERE ELITIT='SI'""").fetchall()

            # --------------------------------------------------#
            if quien == 'Conyuge':
                if len(dato['Nom']) > 0 and len(dato['Ape']) > 0:
                    rows = c.execute(
                        """SELECT * From Conyuge WHERE NOMCON=? AND APECON=? AND ELICON='SI'""", (dato['Nom'], dato['Ape'], )).fetchall()
                else:
                    rows = c.execute(
                        """SELECT * From Conyuge WHERE DNICON = ? AND ELICON='SI'""", (dato['DNI'], )).fetchall()

            # --------------------------------------------------#
            if quien == 'Titular_DNITIT':
                rows = c.execute(
                    """SELECT * From Conyuge WHERE Titular_DNITIT=? AND ELICON='SI'""", (dato['DNI'], )).fetchall()

            # --------------------------------------------------#
            if quien == 'Hijo/s':
                if len(dato['Nom']) > 0 and len(dato['Ape']) > 0:
                    rows = c.execute(
                        """SELECT * From Hijo WHERE NOMHIJ=? AND APEHIJ=? AND ELIHIJ='SI'""", (dato['Nom'], dato['Ape'], )).fetchall()
                else:
                    rows = c.execute(
                        """SELECT * From Hijo WHERE DNIHIJ=? AND ELIHIJ='SI'""", (dato['DNI'], )).fetchall()

            # --------------------------------------------------#
            if quien == 'DNITIT_HIJO':
                rows = c.execute(
                    """SELECT * From Hijo WHERE Titular_DNITIT=? AND ELIHIJ='SI'""", (dato['DNI'], )).fetchall()

            # --------------------------------------------------#

            if not rows:
                Messagebox.show_warning(
                    f'No existe ningun registro con ese DNI{dato["DNI"]}', 'Error')
                
                
            tree.delete(*tree.get_children())
            fecha_actual = datetime.now()
            if  quien == 'Conyuge' or quien == 'Titular_DNITIT' :
                for row in rows:
                    edad = definir_edad(row[4])
                    tree.insert('', END, row[0], values=(
                        row[0], row[1], row[2], row[3], row[4], edad, row[5], row[6], row[7], row[10]))
            if quien == 'Hijo/s' or quien == 'DNITIT_HIJO':
                for row in rows:
                    edad = definir_edad(row[4])
                    if edad >= 18:
                        mayor = 'Si'
                    else:
                        mayor = 'No'
                    
                    tree.insert('', END, row[0], values=(
                        row[0], row[1], row[2], row[3], row[4], edad, mayor, row[5], row[6], row[9]))
            if quien == 'Titular' or quien == 'TODOS':
                for row in rows:
                    edad = definir_edad(row[4])
                    tree.insert('', END, row[0], values=(
                        row[0], row[1], row[2], row[3], row[4], edad, row[5], row[6], row[7], row[9]))
            
    # ---------------------------------------------------------------------#

    # ---------------------------------------------------------------------#
    # Frame, Label, Entry y Button de DNI
    x = ttkb.LabelFrame(top, text=f'Buscar',
                        padding=5, borderwidth=3, relief="ridge")
    x.grid(row=1, column=0, padx=10, pady=10, columnspan=3)
    # ttkb.Label(x,text='Seleccione:',font=('Time New Roman',14),borderwidth=3,anchor=W,relief='groove').grid(row=1,column=0,sticky="nsew",pady=8)
    
    

   

    btn_Seleccionar = ttkb.Button(x, text='Seleccionar', command=lambda: seleccionado(
            control_hijo.get(), control_conyuge.get(), control_titular.get()))
    def toggle_titular():
        # Función llamada cuando se hace clic en el Checkbutton TITULAR
        if control_titular.get() == "Titular":
            conyuge.configure(state="disabled")
            hijo.configure(state="disabled")
            btn_Seleccionar.grid(row=0, column=0, sticky="nsew", pady=8)
        else:
            conyuge.configure(state="normal")
            hijo.configure(state="normal")
            btn_Seleccionar.grid_forget()

    def toggle_conyuge():
        # Función llamada cuando se hace clic en el Checkbutton CÓNYUGE
        if control_conyuge.get() == "Conyuge":
            titular.configure(state="disabled")
            hijo.configure(state="disabled")
            btn_Seleccionar.grid(row=0, column=0, sticky="nsew", pady=8)
        else:
            titular.configure(state="normal")
            hijo.configure(state="normal")
            btn_Seleccionar.grid_forget()
        

    def toggle_hijo():
        # Función llamada cuando se hace clic en el Checkbutton HIJO/S
        
        if control_hijo.get() == "Hijo/s":
            titular.configure(state="disabled")
            conyuge.configure(state="disabled")
            btn_Seleccionar.grid(row=0, column=0, sticky="nsew", pady=8)
        else:
            btn_Seleccionar.grid_forget()
            titular.configure(state="normal")
            conyuge.configure(state="normal")
            
            
            
            
        
        

    # defino StrinsVar para la obtencion de estados del checkbutton
    control_titular = StringVar()
    control_conyuge = StringVar()
    control_hijo = StringVar()

    # Checkbutton TITULAR
    titular = Checkbutton(x, text='Titular', bootstyle="success-round-toggle",
                          onvalue='Titular', offvalue='nada',
                          variable=control_titular, command=toggle_titular)
    titular.grid(row=3, column=1, pady=8, sticky="nsew")
    

    # Checkbutton CÓNYUGE
    conyuge = Checkbutton(x, text='Cónyuge', bootstyle="success-round-toggle", onvalue='Conyuge', offvalue='nada',
                          variable=control_conyuge, command=toggle_conyuge)
    conyuge.grid(row=4, column=1, pady=8, sticky="nsew")

    # Checkbutton HIJO/S
    hijo = Checkbutton(x, text='Hijo/s', bootstyle="success-round-toggle",
                       onvalue='Hijo/s', offvalue='nada',
                       variable=control_hijo, command=toggle_hijo)
    hijo.grid(row=5, column=1, pady=8, sticky="nsew")

    ttkb.Label(x, text='Solo puedes elegir una opción a la vez.',
               font=('Time New Roman', 10),
               anchor=W).grid(row=2, column=0,
                              sticky="nsew", pady=8, columnspan=2)
    
    
    

    # muestra los datos según la selección que se haya hecho
    def seleccionado(control_hijo, control_conyuge, control_titular):
    
        top2 = Toplevel()
        top2.title('Buscar')
        top2.geometry('1000x600')
        icono = ruta_archivo
        top2.iconbitmap(icono)

        estilo = ttkb.Style()
        estilo.configure("mystyle.Treeview", font=(
            'Time New Roman', 10), background='#DCE6F2', foreground='#000')
        
        
        

        def buscar(quien, tree):
            # gurada los datos en diccionarios para despues poder hacer el select correspondiente
            try:
                if len(Nom.get()) > 0 and len(Ape.get()) > 0:
                    ape = validar_apellido_sin_espacios(Ape.get()) # valida que no existan espacios en blanco adiconales a lo necesario en el apellido
                    nom = validar_nombre_sin_espacios(Nom.get())   # valida que no existan espacios en blanco adiconales a lo necesario en el nombre
                    Nombre = nom.upper() 
                    Apellido = ape.upper()
                else:
                    Nombre = ''
                    Apellido = ''

                if quien == 'Hijo/s' or quien == 'Conyuge' or quien == 'Titular_DNITIT' or quien == 'DNITIT_HIJO' or quien == 'Titular':
                    dato = {'DNI': dni.get(),
                            'Nom': Nombre.upper(),
                            'Ape': Apellido.upper()}
                    extraer_datos_dni(quien, dato, tree,tipo)
                if quien == 'TODOS':
                    dato = {'DNI': dni.get()}
                    extraer_datos_dni(quien, dato, tree,tipo)

            except ValueError:
                Messagebox.show_warning(
                    'Verifique los CAMPOS', 'Error en algun Campo')
                top2.lift()
        # Create Frame
        h = ttkb.Frame(top2,
                       padding=5, borderwidth=3, relief="ridge")
        h.pack(pady=10, padx=4)

        # Create scrollbar Y
        tree_scroollbar_y = ttk.Scrollbar(h,bootstyle="warning-round")
        tree_scroollbar_y.pack(side=RIGHT, fill=Y)

        # Create scrollbar X
        tree_scroollbar_x = ttk.Scrollbar(h, orient='horizontal',bootstyle="warning-round")
        tree_scroollbar_x.pack(side=BOTTOM, fill=X)

        # Create Treeview
        tree = ttk.Treeview(h, bootstyle='success', style="mystyle.Treeview",
                            yscrollcommand=tree_scroollbar_y.set, xscrollcommand=tree_scroollbar_x.set)
        tree.columnconfigure(0, weight=1)
        tree.rowconfigure(0, weight=1)

        # configurando scrollbar y
        tree_scroollbar_y.config(command=tree.yview)
        tree_scroollbar_x.config(command=tree.xview)

        if control_titular == 'Titular':
            quien = 'Titular'
            # Grilla de datos Titular.
            tree['columns'] = ('DNI', 'Nombre', 'Apellido', 'CUIL/CUIT',
                               'Fecha_de_Nacimiento', 'Edad', 'Telefono', 'Mail', 'Localidad', 'NOTTIT')
            tree.column('#0', width=0, stretch=NO)
            tree.column('DNI', anchor=CENTER)
            tree.column('Nombre', anchor=CENTER)
            tree.column('Apellido', anchor=CENTER)
            tree.column('CUIL/CUIT', anchor=CENTER)
            tree.column('Fecha_de_Nacimiento', anchor=CENTER)
            tree.column('Edad', anchor=CENTER, width=80)
            tree.column('Telefono', anchor=CENTER)
            tree.column('Mail', anchor=CENTER)
            tree.column('Localidad', anchor=CENTER)
            tree.column('NOTTIT', anchor=CENTER)

            tree.heading('DNI', text='DNI', anchor=CENTER)
            tree.heading('Nombre', text='Nombre/s', anchor=CENTER)
            tree.heading('Apellido', text='Apellido/s', anchor=CENTER)
            tree.heading('CUIL/CUIT', text='CUIL/CUIT', anchor=CENTER)
            tree.heading('Fecha_de_Nacimiento',
                         text='Fecha de Nacimiento', anchor=CENTER)
            tree.heading('Edad', text='Edad', anchor=CENTER)
            tree.heading('Telefono', text='Teléfono', anchor=CENTER)
            tree.heading('Mail', text='Mail', anchor=CENTER)
            tree.heading('Localidad', text='Localidad', anchor=CENTER)
            tree.heading('NOTTIT', text='Nota Cliente', anchor=CENTER)
            tree.pack()

        if control_hijo == 'Hijo/s':
            quien = 'Hijo/s'
            # Grilla de datos Hijo.
            tree['columns'] = ('DNI', 'Nombre', 'Apellido', 'CUIL/CUIT', 'Fecha_de_Nacimiento',
                               'Edad', 'Mayor_hijo', 'Localidad', 'Padre_Hijo', 'DNITIT_HIJO')
            tree.column('#0', width=0, stretch=NO)
            tree.column('DNI', anchor=CENTER)
            tree.column('Nombre', anchor=CENTER)
            tree.column('Apellido', anchor=CENTER)
            tree.column('CUIL/CUIT', anchor=CENTER)
            tree.column('Fecha_de_Nacimiento', anchor=CENTER)
            tree.column('Edad', anchor=CENTER, width=80)
            tree.column('Mayor_hijo', anchor=CENTER)
            tree.column('Localidad', anchor=CENTER)
            tree.column('Padre_Hijo', anchor=CENTER)
            tree.column('DNITIT_HIJO', anchor=CENTER)

            tree.heading('DNI', text='DNI', anchor=CENTER)
            tree.heading('Nombre', text='Nombre/s', anchor=CENTER)
            tree.heading('Apellido', text='Apellido/s', anchor=CENTER)
            tree.heading('CUIL/CUIT', text='CUIL/CUIT', anchor=CENTER)
            tree.heading('Fecha_de_Nacimiento',
                         text='Fecha de Nacimiento', anchor=CENTER)
            tree.heading('Edad', text='Edad', anchor=CENTER)
            tree.heading('Mayor_hijo', text='¿Es Mayor de 18?', anchor=CENTER)
            tree.heading('Localidad', text='Localidad', anchor=CENTER)
            tree.heading('Padre_Hijo', text='Es Hijo de:', anchor=CENTER)
            tree.heading('DNITIT_HIJO', text='DNI Titular', anchor=CENTER)
            tree.pack()

            # ---------------------------------------------------------------------#

        if control_conyuge == 'Conyuge':
            quien = 'Cónyuge'
            # Grilla de datos cónyuge.
            tree['columns'] = ('DNI', 'Nombre', 'Apellido', 'CUIL/CUIT', 'Fecha_de_Nacimiento',
                               'Edad', 'Telefono', 'Mail', 'Localidad', 'Titular_DNITIT')
            tree.column('#0', width=0, stretch=NO)
            tree.column('DNI', anchor=CENTER)
            tree.column('Nombre', anchor=CENTER)
            tree.column('Apellido', anchor=CENTER)
            tree.column('CUIL/CUIT', anchor=CENTER)
            tree.column('Fecha_de_Nacimiento', anchor=CENTER)
            tree.column('Edad', anchor=CENTER, width=50)
            tree.column('Telefono', anchor=CENTER)
            tree.column('Mail', anchor=CENTER)
            tree.column('Localidad', anchor=CENTER)
            tree.column('Titular_DNITIT', anchor=CENTER)

            tree.heading('DNI', text='DNI', anchor=CENTER)
            tree.heading('Nombre', text='Nombre/s', anchor=CENTER)
            tree.heading('Apellido', text='Apellido/s', anchor=CENTER)
            tree.heading('CUIL/CUIT', text='CUIL/CUIT', anchor=CENTER)
            tree.heading('Fecha_de_Nacimiento',
                         text='Fecha de Nacimiento', anchor=CENTER)
            tree.heading('Edad', text='Edad', anchor=CENTER)
            tree.heading('Telefono', text='Teléfono', anchor=CENTER)
            tree.heading('Mail', text='Mail', anchor=CENTER)
            tree.heading('Localidad', text='Localidad', anchor=CENTER)
            tree.heading('Titular_DNITIT',
                         text='DNI del Titular', anchor=CENTER)
            tree.pack()

            # ---------------------------------------------------------------------#

        # Frame, Label, Entry y Button de DNI
        g = ttkb.LabelFrame(
            top2, text=f'Buscar{quien}', padding=5, borderwidth=3, relief="ridge")
        g.pack(before=h, padx=4, pady=10)

        if control_titular == 'Titular':
            ttkb.Label(g, text='DNI:', font=('Time New Roman', 12),
                       borderwidth=3, relief="groove", anchor=W).grid(row=0, column=0, sticky="nsew", pady=8)
            dni = ttkb.Entry(g, width=25, font=(14))
            dni.grid(row=0, column=1, pady=8, padx=10)
            validar_Enreys_Solo_Numeros(dni)

            ttkb.Label(g, text='Nombre/Apellido:', font=('Time New Roman', 12),
                       borderwidth=3, relief="groove", anchor=W).grid(row=1, column=0, sticky="nsew", pady=8)
            Nom = ttkb.Entry(g, width=18, font=(14))
            Nom.grid(row=1, column=1, pady=8)
            validar_Enreys_Solo_Letras(Nom)
            Ape = ttkb.Entry(g, width=18, font=(14))
            Ape.grid(row=1, column=2, pady=8)
            validar_Enreys_Solo_Letras(Ape)

            btn_buscar_dni = ttkb.Button(
                g, text='Buscar', bootstyle='info-outline', command=lambda: buscar(control_titular, tree))
            btn_buscar_dni.grid(row=0, column=2, sticky='ew')

            T = 'TODOS'
            btn_buscar_todos = ttkb.Button(
                g, text='Buscar Todos', bootstyle='info-outline', command=lambda: buscar(T, tree),width=30)
            btn_buscar_todos.grid(
                row=0, column=3, padx=10, pady=8)
            
            # verifica si lo lamamos por el lado de papelera para agregar un button que devuelva a la lista "blanca" al registro/s
            if tipo == 'ver_papelera':
                btn_recuperar = ttkb.Button(g, text='Recuperar', bootstyle='info-outline',width=20,command= lambda:devolver_registro(tree,control_titular,top2))
                btn_recuperar.grid(
                    row=0, column=4, sticky='nsew', padx=4, pady=8)

        if control_hijo == 'Hijo/s':
            # verifica si es Hijo o Cónyuge para agregar el button de buscar por titular al Hijo.

            # cambio de referencia para hacer la busqueda, en vez de "quien" se pone "F"
            F = 'DNITIT_HIJO'
            btn_buscar_dni_t = ttkb.Button(
                g, text='Buscar por Titular', bootstyle='info-outline', command=lambda: buscar(F, tree))
            btn_buscar_dni_t.grid(row=0, column=3, sticky='ew', padx=8)

            ttkb.Label(g, text='DNI:', font=('Time New Roman', 12),
                       borderwidth=3, relief="groove", anchor=W).grid(row=0, column=0, sticky="nsew", pady=8)
            dni = ttkb.Entry(g, width=25, font=(14))
            dni.grid(row=0, column=1, pady=8, padx=10)
            validar_Enreys_Solo_Numeros(dni)

            ttkb.Label(g, text='Nombre/Apellido:', font=('Time New Roman', 12),
                       borderwidth=3, relief="groove", anchor=W).grid(row=1, column=0, sticky="nsew", pady=8)
            Nom = ttkb.Entry(g, width=18, font=(14))
            Nom.grid(row=1, column=1, pady=8)
            validar_Enreys_Solo_Letras(Nom)
            Ape = ttkb.Entry(g, width=18, font=(14))
            Ape.grid(row=1, column=2, pady=8)
            validar_Enreys_Solo_Letras(Ape)

            btn_buscar_dni = ttkb.Button(
                g, text='Buscar', bootstyle='info-outline', command=lambda: buscar(control_hijo, tree))
            btn_buscar_dni.grid(row=0, column=2, sticky='ew')
            # verifica si lo lamamos por el lado de papelera para agregar un button que devuelva a la lista "blanca" al registro/s
            if tipo == 'ver_papelera':
                btn_recuperar = ttkb.Button(g, text='Recuperar', bootstyle='info-outline',width=20,command= lambda:devolver_registro(tree,control_hijo,top2))
                btn_recuperar.grid(
                    row=0, column=4, sticky='nsew', padx=4, pady=8)


        if control_conyuge == 'Conyuge':
            # verifica si es Hijo o Cónyuge para agregar el button de buscar por titular al Cónyuge.

            # cambio de referencia para hacer la busqueda, en vez de "quien" se pone "F"
            F = 'Titular_DNITIT'
            btn_buscar_dni_t = ttkb.Button(
                g, text='Buscar por Titular', bootstyle='info-outline', command=lambda: buscar(F, tree))
            btn_buscar_dni_t.grid(row=0, column=3, padx=8)

            ttkb.Label(g, text='DNI:', font=('Time New Roman', 12),
                       borderwidth=3, relief="groove", anchor=W).grid(row=0, column=0, sticky="nsew", pady=8)
            dni = ttkb.Entry(g, width=25, font=(14))
            dni.grid(row=0, column=1, pady=8, padx=10)
            validar_Enreys_Solo_Numeros(dni)

            ttkb.Label(g, text='Nombre/Apellido:', font=('Time New Roman', 12),
                       borderwidth=3, relief="groove", anchor=W).grid(row=1, column=0, sticky="nsew", pady=8)
            Nom = ttkb.Entry(g, width=18, font=(14))
            Nom.grid(row=1, column=1, pady=8)
            validar_Enreys_Solo_Letras(Nom)
            Ape = ttkb.Entry(g, width=18, font=(14))
            Ape.grid(row=1, column=2, pady=8)
            validar_Enreys_Solo_Letras(Ape)

            btn_buscar_dni = ttkb.Button(
                g, text='Buscar', bootstyle='info-outline', command=lambda: buscar(control_conyuge, tree))
            btn_buscar_dni.grid(row=0, column=2, sticky='ew')
            # verifica si lo lamamos por el lado de papelera para agregar un button que devuelva a la lista "blanca" al registro/s
            if tipo == 'ver_papelera':
                btn_recuperar = ttkb.Button(g, text='Recuperar', bootstyle='info-outline',width=20,command= lambda:devolver_registro(tree,control_conyuge,top2))
                btn_recuperar.grid(
                    row=0, column=4, sticky='nsew', padx=4, pady=8)
        top2.lift()
        
        # ---------------------------------------------------------------------#


def Actualizar_registro(quien : str):
    """Actualizar_registro
        Lo que hace es tomar el DNI ingresado segun de (quien) lo solicita si es Hijo, cónyuge o  Titular.
            devuelve los datos en los entry, los cuales se pueden modificar y si se apreta el boton actualizar
            se le envia un mensaje preguntandole si quiere actualizar los datos, si la respuesta es afirmativa los 
            actualiza.
    """
    quien = quien 
    top = Toplevel()
    top.title('Actualizar')
    icono = ruta_archivo
    top.iconbitmap(icono)
    top.resizable(False,False)
    

    estilo = ttkb.Style()
    estilo.configure("mystyle.Treeview", font=(
        'Time New Roman', 10), background='#DCE6F2', foreground='#000')
    
    def extraer_registro(quien,dato):
        """Realiza la consulta SQL para la busqueda del regstro que se quiere actualizar."""

        bandera = True
        if quien == 'Titular':
                rows = c.execute(
                        """SELECT * From Titular WHERE DNITIT=? AND ELITIT='NO'""", (dato['DNI'], )).fetchall()

        if quien == 'Cónyuge':
                rows = c.execute(
                        """SELECT * From Conyuge WHERE DNICON = ? AND ELICON='NO'""", (dato['DNI'], )).fetchall()
        if quien == 'Hijo/a':
                rows = c.execute(
                        """SELECT * From Hijo WHERE DNIHIJ=? AND ELIHIJ='NO'""", (dato['DNI'], )).fetchall()
        
        if not rows:
                Messagebox.show_warning(
                    'No se enconto ningun registro', 'Error')
                top.lift()
                
        """"Setea los valores en los Entry para que se puedan visualizar los datos buscados a editar"""
        if quien == "Titular":
            for row in rows:
                edad = definir_edad(row[4])
                
                varDni.set(row[0])
                varNombre.set(row[1])
                varApellio.set(row[2])
                varCuil.set(row[3])
                varFnacimiento.set(row[4])
                varEdad.set(int(edad))
                varTelef.set(row[5])
                varMail.set(row[6])
                varLocalidad.set(row[7])
                varNota.set(row[9])
            mostrar_entradas(quien,bandera)
        
        if  quien == "Cónyuge":
            for row in rows:
                edad = definir_edad(row[4])
                    
                varDni.set(row[0])
                varNombre.set(row[1])
                varApellio.set(row[2])
                varCuil.set(row[3])
                varFnacimiento.set(row[4])
                varEdad.set(int(edad))
                varTelef.set(row[5])
                varMail.set(row[6])
                varLocalidad.set(row[7])
                VarTit_DNI.set(row[10])
            mostrar_entradas(quien,bandera)
                    

        if quien == 'Hijo/a':
            for row in rows:
                edad = definir_edad(row[4])
                if edad >= 18:
                        mayor:str = 'Si'
                else:
                        mayor :str = 'No'
                
                varDni.set(row[0])
                varNombre.set(row[1])
                varApellio.set(row[2])
                varCuil.set(row[3])
                varFnacimiento.set(row[4])
                varEdad.set(int(edad))
                varMayor.set(mayor)                    
                varLocalidad.set(row[5])
                varHijo_de.set(row[6])
                VarTit_DNI.set(row[9])
            mostrar_entradas(quien,bandera)

    def actualizar_registro(quien,resultados):

        if quien == "Titular":
            c.execute("UPDATE  Titular SET NOMTIT=?,APETIT=?,CUIL_CUIT_TIT=?,FNATIT=?,TELTIT=?,MAILTIT=?,LOCTIT=?,FCHTIT=?,NOTTIT=? WHERE DNITIT=?"
                      , (resultados['NOMTIT'],resultados['APETIT'],resultados['CUIL_CUIT_TIT'],
                         resultados['FNATIT'],resultados['TELTIT'],resultados['MAILTIT'],
                          resultados['LOCTIT'],resultados['FCHTIT'],resultados['NOTTIT'],resultados['DNITIT']))
            conn.commit()

        if quien == "Cónyuge":
            c.execute("UPDATE  Conyuge SET NOMCON=?,APECON=?,CUIL_CUIT_CON=?,FNACON=?,TELCON=?,MAILCON=?,LOCCON=?,FCHCON=?,Titular_DNITIT=? WHERE DNICON=?",
                      (resultados['NOMCON'], resultados['APECON'], resultados['CUIL_CUIT_CON'], resultados['FNACON'], resultados['TELCON'],
                        resultados['MAILCON'], resultados['LOCCON'], resultados['FCHCON'], resultados['Titular_DNITIT'],resultados['DNICON'] ))
            conn.commit()

        if quien == "Hijo/a":
            c.execute("""
                UPDATE Hijo  SET NOMHIJ=?,APEHIJ=?,CUIL_CUIT_HIJ=?,FNAHIJ=?,LOCHIJ=?,PDSHIJ=?,FCHHIJ=?,Titular_DNITIT=? WHERE DNIHIJ=?
            """, (resultados['NOMHIJ'], resultados['APEHIJ'], resultados['CUIL_CUIT_HIJ'], resultados['FNAHIJ'], resultados['LOCHIJ'],
                   resultados['PDSHIJ'], resultados['FCHHIJ'], resultados['DNITIT_HIJO'],resultados['DNIHIJ']))
            conn.commit()
        

    def mostrar_entradas(quien,bandera):
        """_summary_
        Pone en pantallas las labels y los entrys pra que el susuario vea y modifique los datos buscados.

        Args:
            quien (str): Es el string que define si el llamado va por parte del Titular o por el Cónyuge o hijo/a
        """
        
        top.geometry("768x780")


        def extraer_datos_actualizar():
            try:
                respuesta = Messagebox.okcancel(title="Actualizar Registro",message="¿Desea Actualizar la información?")
                if respuesta:
                    top.lift()
                    ahora = datetime.date(datetime.now())
                    if quien == "Titular":
                        nom = validar_nombre_sin_espacios(nombre.get()) # limpia el nombre
                        ape = validar_apellido_sin_espacios(apellido.get()) # limpia el apellido
                        
                        # Resultados de los entrys usados para actualizar los registros.
                        resultados = {
                            'DNITIT': int(dni.get()),
                            'NOMTIT': nom.upper(),
                            'APETIT': ape.upper(),
                            'CUIL_CUIT_TIT': int(cuil_cuit.get()),
                            'FNATIT': fNacimiento.get(),
                            'TELTIT': int(telef.get()),
                            'MAILTIT': mail.get(),
                            'LOCTIT': localidad_r.get().upper(),
                            'FCHTIT': ahora,
                            'NOTTIT': nota.get()
                        }
                        actualizar_registro(quien,resultados)
                    
                    if quien == "Cónyuge":
                            nom = validar_nombre_sin_espacios(nombre.get()) # limpia el nombre
                            ape = validar_apellido_sin_espacios(apellido.get()) # limpia el apellido
                            
                            # Resultados de los entrys usados para actualizar los registros
                            resultados = {
                                'DNICON': int(dni.get()),
                                'NOMCON': nom.upper(),
                                'APECON': ape.upper(),
                                'CUIL_CUIT_CON': int(cuil_cuit.get()),
                                'FNACON': fNacimiento.get(),
                                'TELCON': int(telef.get()),
                                'MAILCON': mail.get(),
                                'LOCCON': localidad_r.get().upper(),
                                'FCHCON': ahora,
                                'Titular_DNITIT': int(Tit_DNITIT.get())
                            }
                            actualizar_registro(quien,resultados)
                    
                    if quien == "Hijo/a":
                        nom = validar_nombre_sin_espacios(nombre.get()) # limpia el nombre
                        ape = validar_apellido_sin_espacios(apellido.get()) # limpia el apellido

                        # Resultados de los entrys usados para actualizar los registros
                        resultados = {
                            'DNIHIJ': int(dni.get()),
                            'NOMHIJ': nom.upper(),
                            'APEHIJ': ape.upper(),
                            'CUIL_CUIT_HIJ': int(cuil_cuit.get()),
                            'FNAHIJ': fNacimiento.get(),
                            'LOCHIJ': localidad_r.get().upper(),
                            'PDSHIJ': hijo_de.get(),
                            'FCHHIJ': ahora,
                            'DNITIT_HIJO': int(Tit_DNITIT.get())
                        }
                        actualizar_registro(quien,resultados)
                    top.destroy()

            except ValueError:
                Messagebox.show_info("Verifique que los campos esten llenados correctamente...","Información")
                top.lift()
        

        if bandera:
            btn_actualizar = ttkb.Button(top,text="Actualizar",width=10, command=extraer_datos_actualizar)
            btn_actualizar.grid(padx=8,pady=10,row=3,column=0,sticky="e")
            bandera = False    
        if quien == "Titular":
                x.after(500)
                x.update()
                ttkb.Label(x, text="Nombre: ", font=('Time New Roman', 14),
                            borderwidth=3, relief="groove", anchor=W).grid(padx=4,pady=8,row=1,column=0, sticky="nsew")
                nombre = ttkb.Entry(x,width=40,textvariable=varNombre, font=(16))
                nombre.grid(row=1,column=1,padx=2)
                validar_Enreys_Solo_Letras(nombre)

                ttkb.Label(x, text="Apellido: ", font=('Time New Roman', 14),
                            borderwidth=3, relief="groove", anchor=W).grid(padx=4,pady=8,row=2,column=0, sticky="nsew")
                apellido = ttkb.Entry(x,width=40,textvariable=varApellio, font=(16))
                apellido.grid(row=2,column=1,padx=2)
                validar_Enreys_Solo_Letras(apellido)
                

                l_cuil_cuit = ttkb.Label(x, text='CUIL / CUIT:', font=('Time New Roman', 14),
                                        borderwidth=3, relief="groove", anchor=W).grid(row=3, column=0, sticky="nsew", pady=8)
                cuil_cuit = ttkb.Entry(x, width=40, font=(16),textvariable=varCuil)
                cuil_cuit.grid(row=3, column=1, pady=8, padx=10)
                validar_Enreys_Solo_Numeros(cuil_cuit)

                l_fNacimiento = ttkb.Label(x, text='Fecha de Nacimiento:', font=(
                    'Time New Roman', 14), borderwidth=3, relief="groove", anchor=W).grid(row=4, column=0, sticky="nsew", pady=8)
                fNacimiento = ttkb.Entry(x, width=40, font=(16),textvariable=varFnacimiento)
                fNacimiento.grid(row=4, column=1, pady=8, padx=10)

                lEdad = ttkb.Label(x, text='Edad:', font=(
                    'Time New Roman', 14), borderwidth=3, relief="groove", anchor=W).grid(row=5, column=0, sticky="nsew", pady=8)
                Edad = ttkb.Entry(x,width=40,font=(16), textvariable=varEdad)
                Edad.grid(row=5, column=1, pady=8,padx=10)

                l_telef = ttkb.Label(x, text='Teléfono:', font=('Time New Roman', 14),
                                    borderwidth=3, relief="groove", anchor=W).grid(row=6, column=0, sticky="nsew", pady=8)
                telef = ttkb.Entry(x, width=40, font=(16), textvariable=varTelef)
                telef.grid(row=6, column=1, pady=8, padx=10)
                validar_Enreys_Solo_Numeros(telef)

                l_mail = ttkb.Label(x, text='Mail:',  font=('Time New Roman', 14),
                                    borderwidth=3, relief="groove", anchor=W).grid(row=7, column=0, sticky="nsew", pady=8)
                mail = ttkb.Entry(x, width=40, font=(16), textvariable=varMail)
                mail.grid(row=7, column=1, pady=8, padx=10)

                l_localidad_r = ttkb.Label(x, text='Localidad de residencia:', font=(
                    'Time New Roman', 14), borderwidth=3, relief="groove", anchor=W).grid(row=8, column=0, sticky="nsew", pady=8)
                localidad_r = ttkb.Entry(x, width=40, font=(16),textvariable=varLocalidad)
                localidad_r.grid(row=8, column=1, pady=8, padx=10)
                validar_Enreys_Solo_Letras(localidad_r)

                l_nota = ttkb.Label(x, text='Nota:', font=(
                    'Time New Roman', 14), borderwidth=3, relief="groove", anchor=W).grid(row=9, column=0, sticky="nsew", pady=8)
                nota = ttkb.Entry(x, width=40, font=(16),textvariable=varNota)
                nota.grid(row=9, column=1, pady=8, padx=10)

                


        if quien == "Cónyuge":
                x.after(500)
                x.update()

                ttkb.Label(x, text="Nombre: ", font=('Time New Roman', 14),
                            borderwidth=3, relief="groove", anchor=W).grid(padx=4,pady=8,row=1,column=0, sticky="nsew")
                nombre = ttkb.Entry(x,width=40,textvariable=varNombre, font=(16))
                nombre.grid(row=1,column=1,padx=2)
                validar_Enreys_Solo_Letras(nombre)

                ttkb.Label(x, text="Apellido: ", font=('Time New Roman', 14),
                            borderwidth=3, relief="groove", anchor=W).grid(padx=4,pady=8,row=2,column=0, sticky="nsew")
                apellido = ttkb.Entry(x,width=40,textvariable=varApellio, font=(16))
                apellido.grid(row=2,column=1,padx=2)
                validar_Enreys_Solo_Letras(apellido)

                l_cuil_cuit = ttkb.Label(x, text='CUIL / CUIT:', font=('Time New Roman', 14),
                                        borderwidth=3, relief="groove", anchor=W).grid(row=3, column=0, sticky="nsew", pady=8)
                cuil_cuit = ttkb.Entry(x, width=40, font=(16),textvariable=varCuil)
                cuil_cuit.grid(row=3, column=1, pady=8, padx=10)
                validar_Enreys_Solo_Numeros(cuil_cuit)

                l_fNacimiento = ttkb.Label(x, text='Fecha de Nacimiento:', font=(
                    'Time New Roman', 14), borderwidth=3, relief="groove", anchor=W).grid(row=4, column=0, sticky="nsew", pady=8)        
                fNacimiento = ttkb.Entry(x, width=40, font=(16),textvariable=varFnacimiento)
                fNacimiento.grid(row=4, column=1, pady=8, padx=10)
                
                lEdad = ttkb.Label(x, text='Edad:', font=(
                    'Time New Roman', 14), borderwidth=3, relief="groove", anchor=W).grid(row=5, column=0, sticky="nsew", pady=8)
                Edad = ttkb.Entry(x,width=40,font=(16),textvariable=varEdad)
                Edad.grid(row=5, column=1, pady=8,padx=10)

                l_telef = ttkb.Label(x, text='Teléfono:', font=('Time New Roman', 14),
                                    borderwidth=3, relief="groove", anchor=W).grid(row=6, column=0, sticky="nsew", pady=8)
                telef = ttkb.Entry(x, width=40, font=(16),textvariable=varTelef)
                telef.grid(row=6, column=1, pady=8, padx=10)
                validar_Enreys_Solo_Numeros(telef)

                l_mail = ttkb.Label(x, text='Mail:', font=('Time New Roman', 14),
                                    borderwidth=3, relief="groove", anchor=W).grid(row=7, column=0, sticky="nsew", pady=8)
                mail = ttkb.Entry(x, width=40, font=(16),textvariable=varMail)
                mail.grid(row=7, column=1, pady=8, padx=10)

                l_localidad_r = ttkb.Label(x, text='Localidad de residencia:', font=(
                    'Time New Roman', 14), borderwidth=3, relief="groove", anchor=W).grid(row=8, column=0, sticky="nsew", pady=8)
                localidad_r = ttkb.Entry(x, width=40, font=(16),textvariable=varLocalidad)
                localidad_r.grid(row=8, column=1, pady=8, padx=10)
                validar_Enreys_Solo_Letras(localidad_r)

                l_Tit_DNITIT = ttkb.Label(x, text='DNI Titular', font=(
                    'Time New Roman', 14), borderwidth=3, relief="groove", anchor=W).grid(row=9, column=0, sticky="nsew", pady=8)
                Tit_DNITIT = ttkb.Entry(x, width=40, font=(16),textvariable=VarTit_DNI)
                Tit_DNITIT.grid(row=9, column=1, pady=8, padx=10)
                validar_Enreys_Solo_Numeros(Tit_DNITIT)

                
                

        if quien == "Hijo/a":
                x.after(500)
                x.update()
                
                ttkb.Label(x, text="Nombre: ", font=('Time New Roman', 14),
                            borderwidth=3, relief="groove", anchor=W).grid(padx=4,pady=8,row=1,column=0, sticky="nsew")
                nombre = ttkb.Entry(x,width=40,textvariable=varNombre, font=(16))
                nombre.grid(row=1,column=1,padx=2)
                validar_Enreys_Solo_Letras(nombre)

                ttkb.Label(x, text="Apellido: ", font=('Time New Roman', 14),
                            borderwidth=3, relief="groove", anchor=W).grid(padx=4,pady=8,row=2,column=0, sticky="nsew")
                apellido = ttkb.Entry(x,width=40,textvariable=varApellio, font=(16))
                apellido.grid(row=2,column=1,padx=2)
                validar_Enreys_Solo_Letras(apellido)

                l_cuil_cuit = ttkb.Label(x, text='CUIL / CUIT:', font=('Time New Roman', 14),
                                        borderwidth=3, relief="groove", anchor=W).grid(row=3, column=0, sticky="nsew", pady=8)
                cuil_cuit = ttkb.Entry(x, width=40, font=(16),textvariable=varCuil)
                cuil_cuit.grid(row=3, column=1, pady=8, padx=10)
                validar_Enreys_Solo_Numeros(cuil_cuit)

                l_fNacimiento = ttkb.Label(x, text='Fecha de Nacimiento:', font=(
                    'Time New Roman', 14), borderwidth=3, relief="groove", anchor=W).grid(row=4, column=0, sticky="nsew", pady=8)
                fNacimiento =  ttkb.Entry(x, width=40, font=(16),textvariable=varFnacimiento)
                fNacimiento.grid(row=4, column=1, pady=8, padx=10)
                
                lEdad = ttkb.Label(x, text='Edad:', font=(
                    'Time New Roman', 14), borderwidth=3, relief="groove", anchor=W).grid(row=5, column=0, sticky="nsew", pady=8)
                Edad =  ttkb.Entry(x, width=40, font=(16),textvariable=varEdad)
                Edad.grid(row=5, column=1, pady=8, padx=10)
                validar_Enreys_Solo_Numeros(Edad)

                lMayor = ttkb.Label(x, text='¿Es Mayor de 18?', font=(
                    'Time New Roman', 14), borderwidth=3, relief="groove", anchor=W).grid(row=6, column=0, sticky="nsew", pady=8)
                Mayor =  ttkb.Entry(x, width=40, font=(16), textvariable=varMayor)
                Mayor.grid(row=6, column=1, pady=8, padx=10)
                validar_Enreys_Solo_Letras(Mayor)

                l_hijo_de = ttkb.Label(x, text='Hijo de:', font=(
                    'Time New Roman', 14), borderwidth=3, relief="groove", anchor=W).grid(row=7, column=0, sticky="nsew", pady=8)
                hijo_de = ttkb.Entry(x, width=40, font=(16),textvariable=varHijo_de)
                hijo_de.grid(row=7, column=1, pady=8, padx=10)
                validar_Enreys_Solo_Letras(hijo_de)

                l_localidad_r = ttkb.Label(x, text='Localidad de residencia:', font=(
                    'Time New Roman', 14), borderwidth=3, relief="groove", anchor=W).grid(row=8, column=0, sticky="nsew", pady=8)
                localidad_r = ttkb.Entry(x, width=40, font=(16),textvariable=varLocalidad)
                localidad_r.grid(row=8, column=1, pady=8, padx=10)
                validar_Enreys_Solo_Letras(localidad_r)

                l_Tit_DNITIT = ttkb.Label(x, text='DNI Titular', font=(
                    'Time New Roman', 14), borderwidth=3, relief="groove", anchor=W).grid(row=9, column=0, sticky="nsew", pady=8)
                Tit_DNITIT = ttkb.Entry(x, width=40, font=(16),textvariable=VarTit_DNI)
                Tit_DNITIT.grid(row=9, column=1, pady=8, padx=10)
                validar_Enreys_Solo_Numeros(Tit_DNITIT)

                
    
    def buscar(quien,dni):

        try:
            dato = {'DNI': dni.get()}

            extraer_registro(quien,dato)
        
        except ValueError:
            Messagebox.show_info("Verifique que los campos esten llenados correctamente...","Información")
            top.lift()

    # Frame principal
    x = ttkb.Frame(top,padding=10, borderwidth=3, relief="ridge")
    x.grid(padx=4,pady=10,row=0,column=0,sticky="nesew")
    
    #lanbel Frame 
    y = ttkb.LabelFrame(x,text="Buscar",padding=10, borderwidth=3, relief="ridge")
    y.grid(padx=4,pady=8,row=0,column=0,columnspan=2)

    varDni= StringVar()
    varNombre= StringVar()
    varApellio= StringVar()
    varCuil = StringVar()
    varFnacimiento= StringVar()
    varTelef = StringVar()
    varEdad= StringVar()
    varMail = StringVar()
    varMayor= StringVar()
    varHijo_de= StringVar()
    varLocalidad= StringVar()
    varNota = StringVar()
    VarTit_DNI= StringVar()

    ttkb.Label(y, text="DNI: ", font=('Time New Roman', 14),
                       borderwidth=3, relief="groove", anchor=W).grid(padx=4,pady=8,row=0,column=0,sticky="w")
    dni = ttkb.Entry(y, width=40,textvariable=varDni, font=(16))
    dni.grid(row=1,column=0,sticky="we",padx=2)
    validar_Enreys_Solo_Numeros(dni)




    btn_buscar = ttkb.Button(y,text="Buscar",width=10,command=lambda: buscar(quien,dni))
    btn_buscar.grid(row=2, column=0,pady=8,sticky="w")

    #-------------------------------------------------------------------------------#
    top.mainloop()
    


# eliminar registro x DNI titular
def eliminar_por_dni():

    """_summary_
        Lo que hace esta funcion es actualizar un registro del cliente seeccionado par dar la ilucion que comporta como una papelera de resiclaje

    """

    top = Toplevel()
    top.title('Eliminar Registro')
    top.resizable(False, False)
    icono = ruta_archivo
    top.iconbitmap(icono)
    
    

    def seleccion():
        try:
            elegido = {'titular': control_titular.get(),
                       'conyuge': control_conyuge.get(),
                       'hijo': control_hijo.get(),
                       'dni': (int(dni.get()))}
            respuesta = Messagebox.yesno(
                '¿Estás seguro de que querer eliminarlo? ¡El contenido esta ligado a otros datos!', '¿Seguro?')
            if respuesta:

                top.lift()
                eliminar(elegido)

            else:
                pass

        except ValueError:
            Messagebox.show_warning(
                '¡¡Parece que no Funcionó!! intentelo más tarde', 'Error')
            top.lift()

    def eliminar(elegido):

        if elegido['conyuge'] == 'Conyuge':
            cony = c.execute("SELECT * FROM Conyuge WHERE Titular_DNITIT=?", (elegido['dni'], )).fetchone()
            if cony:
                c.execute(
                    "UPDATE  Conyuge SET ELICON = 'SI' WHERE Titular_DNITIT=?", (elegido['dni'], ))
                conn.commit()
            else:
                Messagebox.show_warning(
                f'No existe ningun registro con ese DNI{elegido["dni"]}', 'Error')
                top.lift()

        if elegido['hijo'] == 'Hijo':
            hij = c.execute("SELECT * FROM Hijo WHERE Titular_DNITIT=?", (elegido['dni'], )).fetchone()
            if hij:
                c.execute(
                    "UPDATE  Hijo SET ELIHIJ = 'SI' WHERE Titular_DNITIT=?", (elegido['dni'], ))
                conn.commit()
            else:
                Messagebox.show_warning(
                f'No existe ningun registro con ese DNI{elegido["dni"]}', 'Error')
                top.lift()

        if elegido['titular'] == 'Titular':
            t = c.execute("SELECT * FROM Titular WHERE DNITIT=?", (elegido['dni'], )).fetchone()
            cony = c.execute("SELECT * FROM Conyuge WHERE Titular_DNITIT=?", (elegido['dni'], )).fetchone()
            hij = c.execute("SELECT * FROM Hijo WHERE Titular_DNITIT=?", (elegido['dni'], )).fetchone()
            cot = c.execute("SELECT * FROM Cotizacion WHERE Titular_DNITIT=?", (elegido['dni'], )).fetchone()
            llam = c.execute("SELECT * FROM Llamados_ventas WHERE Titular_DNITIT=?",(elegido['dni'], )).fetchone()
            
            if t:
                c.execute(
                    "UPDATE  Titular SET ELITIT = 'SI' WHERE DNITIT=?", (elegido['dni'], ))
                
                if cony:
                    c.execute(
                    "UPDATE  Conyuge SET ELICON = 'SI' WHERE Titular_DNITIT=?", (elegido['dni'], ))

                if hij:
                    c.execute(
                    "UPDATE  Hijo SET ELIHIJ = 'SI' WHERE Titular_DNITIT=?", (elegido['dni'], ))
                
                if cot:
                    c.execute(
                    "UPDATE  Cotizacion SET ELICOT = 'SI' WHERE Titular_DNITIT=?", (elegido['dni'], ))

                if llam:
                    c.execute(
                    "UPDATE  Llamados_Ventas SET ELILVEN = 'SI' WHERE Titular_DNITIT=?", (elegido['dni'], ))
            else:
                Messagebox.show_warning(
                f'No existe ningun registro con ese DNI{elegido["dni"]}', 'Error')
                top.lift()
            conn.commit()   

        if not seleccion:
            Messagebox.show_warning(
                f'No existe ningun registro con ese DNI{elegido["dni"]}', 'Error')
            top.lift()

    x = ttkb.LabelFrame(top, text='Eliminar', padding=5,
                        borderwidth=3, relief='ridge')
    x.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    l_quien_eliminar = ttkb.Label(x, text='Seleccione:', font=(
        'Time New Roman', 14), borderwidth=3, anchor=W, relief='groove').grid(row=1, column=0, sticky="nsew", pady=8)
    def toggle_titular():
        # Función llamada cuando se hace clic en el Checkbutton TITULAR
        if control_titular.get() == "Titular":
            conyuge.configure(state="disabled")
            hijo.configure(state="disabled")
        else:
            conyuge.configure(state="normal")
            hijo.configure(state="normal")

    def toggle_conyuge():
        # Función llamada cuando se hace clic en el Checkbutton CÓNYUGE
        if control_conyuge.get() == "Conyuge":
            titular.configure(state="disabled")
            hijo.configure(state="disabled")
        else:
            titular.configure(state="normal")
            hijo.configure(state="normal")

    def toggle_hijo():
        # Función llamada cuando se hace clic en el Checkbutton HIJO/S
        if control_hijo.get() == "Hijo/s":
            titular.configure(state="disabled")
            conyuge.configure(state="disabled")
        else:
            titular.configure(state="normal")
            conyuge.configure(state="normal")

    control_titular = StringVar()
    control_conyuge = StringVar()
    control_hijo = StringVar()

    # Checkbutton TITULAR
    titular = Checkbutton(x, text='Titular', bootstyle="success-round-toggle", onvalue='Titular',
                          offvalue='nada', variable=control_titular,command=toggle_titular)
    titular.grid(row=2, column=1, pady=8, sticky="nsew")

    # Checkbutton CÓNYUGE
    conyuge = Checkbutton(x, text='Cónyuge', bootstyle="success-round-toggle", onvalue='Conyuge',
                          offvalue='nada', variable=control_conyuge,command=toggle_conyuge)
    conyuge.grid(row=3, column=1, pady=8, sticky="nsew")

    # Checkbutton HIJO/S
    hijo = Checkbutton(x, text='Hijo/s', bootstyle="success-round-toggle", onvalue='Hijo',
                       offvalue='nada', variable=control_hijo,command=toggle_hijo)
    hijo.grid(row=4, column=1, pady=8, sticky="nsew")
    
    ttkb.Label(x, text='DNI del Titular:', font=('Time New Roman', 14), borderwidth=3,
               anchor=W, relief='groove').grid(row=5, column=0, sticky="nsew", pady=8, padx=4)

    # DNI REFERENTE A ELIMINAR
    dni = ttkb.Entry(x, width=30, font=(16))
    dni.grid(row=5, column=1, sticky="nsew", pady=8)
    validar_Enreys_Solo_Numeros(dni)

    btn_eliminar = ttkb.Button(top, text='Eliminar', command=seleccion, bootstyle='danger').grid(
        row=7, column=2, pady=8, padx=8, sticky="nsew")


# -------------------------------MAIN---------------------------------------------------#
titulo = ttkb.Label(root, text='Sistema de carga.', font=('Time New Roman', 28),
                    foreground='#fff').pack(padx=4,pady=8)#.grid(row=0, column=0, columnspan=4, pady=(10, 10), padx=(250))
# ----------------------------------------------------------------------------------#

content = ttkb.Frame(root,
                          padding=10, borderwidth=3, relief="ridge")
content.pack(padx=4,pady=10,expand=True)


btn_buscar = ttkb.Button(
    content, text='Buscar Registro', command=lambda:buscar('buscar'))
btn_buscar.grid(row=4, column=0, columnspan=3, pady=8, padx=10, sticky="ew")
# ----------------------------------------------------------------------------------#

# ----------------------------------TITULAR------------------------------------------------#
#   BTN Y LABEL CARGA TITULAR
cargaTitular = ttkb.Label(content, text='Titular', font=(
    'Time New Roman', 14), padding=5, borderwidth=3, relief="groove", anchor=W)
cargaTitular.grid(row=0, column=0, sticky="nsew", pady=10)

btn_carga_tit = ttkb.Button(
    content, text='Cargar Titular', command=carga_titular)
btn_carga_tit.grid(row=0, column=1, pady=8, padx=10, sticky="ew")
btn_actualizar_tit = ttkb.Button(
    content, text='Actualizar Titular', command=lambda: Actualizar_registro("Titular"))
btn_actualizar_tit.grid(row=0, column=2, pady=8, padx=10, sticky="ew")
#   BTN Buscar Titular
# btn_buscarTitular = ttk.Button(
#     content, text='Buscar Titular', command=buscar_dni)
# btn_buscarTitular.grid(row=0, column=2, pady=8, padx=10, sticky="ew")

# ----------------------------------------------------------------------------------#


# ----------------------------------Resultado de LLamada------------------------------------------------#
# BTN Carga de Resultado de LLamada
cargaLlamadaTit = ttkb.Label(content, text='Cargar Resultado de Llamada', font=(
    'Time New Roman', 14), padding=5, borderwidth=3, relief="groove", anchor=W)
cargaLlamadaTit.grid(row=0, column=4, sticky="nsew", pady=10)
btn_cargaLlamadaTit = ttkb.Button(
    content, text='Cargar Resultado de Llamada', command=cargar_llamada)
btn_cargaLlamadaTit.grid(row=0, column=5, pady=8, padx=10, sticky="ew")
# BTN Buscar Resultado de LLamada
btn_buscarLlamadaTit = ttkb.Button(
    content, text='Buscar Llamada', command=buscar_llamadas)
btn_buscarLlamadaTit.grid(row=0, column=6, padx=8, pady=10, sticky='ew')
# ----------------------------------------------------------------------------------#


# ----------------------------------Cónyuge------------------------------------------------#
#   BTN Y LABEL CARGA CONYUGE
cargaConyuge = ttkb.Label(content, text='Cónyuge', font=(
    'Time New Roman', 14), padding=5, borderwidth=3, relief="groove", anchor=W)
cargaConyuge.grid(row=2, column=0, sticky="nsew", pady=10)

btn_carga_cony = ttkb.Button(
    content, text='Cargar Cónyuge', command=carga_conyuge)
btn_carga_cony.grid(row=2, column=1, pady=8, padx=10, sticky="ew")
btn_actualizar_con = ttkb.Button(
    content, text='Actualizar Cónyuge', command=lambda: Actualizar_registro("Cónyuge"))
btn_actualizar_con.grid(row=2, column=2, pady=8, padx=10, sticky="ew")
#   BTN Buscar Cónyuge
# btn_buscarConyuge = ttk.Button(
#     content, text='Buscar Cónyuge', command=buscar_dni)
# btn_buscarConyuge.grid(row=2, column=2, pady=8, padx=10, sticky='ew')
# ----------------------------------------------------------------------------------#

# ----------------------------------Hijo/s------------------------------------------------#
#   BTN Y LABEL CARGA HIJO
cargaHijo = ttkb.Label(content, text='Hijo/a', font=(
    'Time New Roman', 14), padding=5, borderwidth=3, relief="groove", anchor=W)
cargaHijo.grid(row=3, column=0, sticky="nsew", pady=10)
btn_carga_hijo = ttkb.Button(
    content, text='Cargar Hijo/a', command=carga_hijo)
btn_carga_hijo.grid(row=3, column=1, pady=8, padx=10, sticky="ew")
btn_actualizar_hijo = ttkb.Button(
    content, text='Actualizar Hijo', command=lambda: Actualizar_registro("Hijo/a"))
btn_actualizar_hijo.grid(row=3, column=2, pady=8, padx=10, sticky="ew")
#   BTN Buscar Hijo
# btn_buscarHijo = ttk.Button(
#     content, text='Buscar Hijo/s', command=buscar_dni)
# btn_buscarHijo.grid(row=3, column=2, pady=8, padx=10, sticky='ew')
# ----------------------------------------------------------------------------------#

# -------------------------------Eliminar-----------------------------------------------#
eliminar_registro = ttkb.Label(content, text='Eliminar Registros', font=(
    'Time New Roman', 14), padding=5, borderwidth=3, relief="groove", anchor=W)
eliminar_registro.grid(row=10, column=9, sticky="nsew", pady=10)

btn_eliminar_registro = ttkb.Button(
    content, text='Eliminar', command=eliminar_por_dni, bootstyle='danger', width=8)
btn_eliminar_registro.grid(row=10, column=10, padx=4, pady=8)
# ----------------------------------------------------------------------------------#

# -------------------------------Recuperar Eliminado-----------------------------------------------#
recuperar_registro = ttkb.Label(content, text='Papelera de Reciclaje', font=(
    'Time New Roman', 14), padding=5, borderwidth=3, relief="groove", anchor=W)
recuperar_registro.grid(row=11,column=9,pady=10,sticky="nsew")


btn_buscar_ver_registros_papelera = ttkb.Button(content, text='Ver',command=lambda: buscar('ver_papelera'), width=8)
btn_buscar_ver_registros_papelera.grid(row=11, column=10, padx=4, pady=8)

# ----------------------------------------------------------------------------------#

# -------------------------------Menú de utilidades-----------------------------------------------#
#   Menú de utilidades
content_op_utilidad = ttkb.LabelFrame(
    content, text='Utilidades', padding=10, borderwidth=3, relief="ridge")
content_op_utilidad.grid(row=20, column=3,columnspan=3, sticky="nsew", padx=10, pady=10)
# content_op_utilidad.place(relx=0.03,rely=0.70,relheight=0.4,relwidth=0.6)
# ----------------------------------------------------------------------------------#


# -------------------------------Resumen ventas mes-----------------------------------------------#
# Resumen ventas mes
resumen_ventas_mes = ttkb.Label(content_op_utilidad, text='Resumen cantidad de planes vendidos en el mes',
                                font=('Time New Roman', 14), padding=5, borderwidth=3, relief="groove", anchor=W)
resumen_ventas_mes.grid(row=0, column=0, sticky="nsew", pady=10)
# resumen_ventas_mes.place(relx=0.03,rely=0.03,relheight=0.4,relwidth=0.6)
btn_resumen_ventas_mes = ttkb.Button(
    content_op_utilidad, text='Ver', command=buscar_ventas_mes, width=10)
btn_resumen_ventas_mes.grid(row=0, column=1, pady=8, padx=10)
# btn_resumen_ventas_mes.place(relx=0.23,rely=0.03,relheight=0.4,relwidth=0.6)
# ----------------------------------------------------------------------------------#

# ----------------------------------COTIZACION------------------------------------------------#
lCotizacion = ttkb.Label(content, text='Cotización', font=('Time New Roman', 14),
                         padding=5, borderwidth=3, relief="groove", anchor=W).grid(row=5, column=0, pady=8, sticky='nsew')
btn_carga_coti = ttkb.Button(
    content, text='Cargar Cotización', command=carga_cotizacion)
btn_carga_coti.grid(row=5, column=1, padx=10, pady=8)
btn_buscar_coti = ttkb.Button(
    content, text='Buscar Cotización', command=buscar_Cotizacion)
btn_buscar_coti.grid(row=5, column=2, padx=10, pady=8)

# ----------------------------------------------------------------------------------#

# BTN SALIR
btn_salir = ttkb.Button(root, text='Salir', command=lambda: root.quit())
# btn_salir.grid(column=3, row=5)
btn_salir.pack(side='right',pady=10,padx=4)


root.mainloop()

#preguntar si se redondea, tambien si se usa coma (linea: 1095)

# autonomo  -----> pendiente

# particular non lleva aporte -----> pendiente


