from math import prod
import tkinter as tk
from tkinter import ttk, messagebox
from turtle import width
from logica.producto import ProductoLogica
from modelo.producto import ProductoModel
import locale
class ProductoVista(tk.Tk):

    def __init__(self):
        super().__init__() # Llamar el constructor del padre

        self.__logica = ProductoLogica()
    
        # Tamaño de la ventana
        window_width = 640
        window_height = 480

        # Tamaño de pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Centrar la ventana
        # find the center point
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        print(center_x, ",", center_y)

        # Cambio de tamaño y posición
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')


        self.title("Productos en inventario")
        self.iconbitmap("controlar.ico")

        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        izquierda = tk.Frame(self)
        self.__construir_frame_izquierdo(izquierda)
        izquierda.grid(column=0, row=0, sticky=tk.NSEW, padx=5, pady=10 )

        derecha = tk.Frame(self)
        self.__construir_frame_derecho(derecha)
        derecha.grid(column=1, row=0, sticky=tk.NSEW, padx=5, pady=10)

        self.__cargar_tabla()

    def __construir_frame_izquierdo(self, frame: tk.Frame):
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        self.__tabla = ttk.Treeview(frame, selectmode=tk.BROWSE)
        self.__tabla.grid(column=0, row=0, columnspan=2, sticky=tk.NSEW)
        self.__tabla['columns'] = ('Código', 'Nombre', 'Precio')

        self.__tabla.heading('#0',text="", anchor=tk.CENTER)
        self.__tabla.heading('Código', text="Código", anchor=tk.CENTER)
        self.__tabla.heading('Nombre', text="Nombre", anchor=tk.CENTER)
        self.__tabla.heading('Precio', text="Precio", anchor=tk.CENTER)

        self.__tabla.column('#0', width=0, stretch=tk.NO)
        self.__tabla.column('Código', anchor=tk.E, width=80)
        self.__tabla.column('Nombre', anchor=tk.W)
        self.__tabla.column('Precio', anchor=tk.E, width=80)

        def seleccionar_elemento(event):
            if len(self.__tabla.selection()) > 0:
                self.__btnEliminar['state']=tk.NORMAL
                self.__btnActualizar['state']=tk.NORMAL
                self.__btnIngresar['state']=tk.DISABLED
            else:
                self.__btnEliminar['state']=tk.DISABLED
                self.__btnActualizar['state']=tk.DISABLED
                self.__btnIngresar['state']=tk.NORMAL


            for item_selected in self.__tabla.selection():
                item = self.__tabla.item(item_selected)
                self.__codigo.set(item['values'][0])
                self.__nombre.set(item['values'][1])
                self.__precio.set(item['values'][2])

        self.__tabla.bind('<<TreeviewSelect>>', seleccionar_elemento)

        def nuevo():
            # Limpiar la seleccion de la tabla
            if len(self.__tabla.selection()) > 0:
                self.__tabla.selection_remove(self.__tabla.selection()[0])

            self.__codigo.set("")
            self.__nombre.set("")
            self.__precio.set("")

        def eliminar():
            opcion = messagebox.askquestion('Eliminar producto', '¿Esta seguro en eliminar este producto?')
            if opcion == 'yes':
                # Seleccionar el codigo del elemento seleccionado en la tabla
                codigo = int(self.__codigo.get())

                # Enviar a eliminar el producto con ese id
                self.__logica.eliminar(codigo)
                messagebox.showinfo("Eliminar producto", "Se eliminó de forma existosa")

                self.__cargar_tabla()   

        botones = tk.Frame(frame, relief=tk.RIDGE)
        botones.columnconfigure(0, weight=1)
        botones.columnconfigure(1, weight=1)
        botones.grid(column=0, row=1, columnspan=2, 
                sticky=tk.EW, padx=5, pady=15)

        self.__btnNuevo = ttk.Button(botones, text="Nuevo", command=nuevo)
        self.__btnNuevo.grid(column=0, row=0, sticky=tk.EW, padx=5)

        self.__btnEliminar = ttk.Button(botones, text="Eliminar", state=tk.DISABLED, 
                command=eliminar)
        self.__btnEliminar.grid(column=1, row=0, sticky=tk.EW, padx=5)

    def __construir_frame_derecho(self, frame: tk.Frame):

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=2)
        
        ttk.Label(frame, text="Datos del producto", font=("Calibri",12,"bold"), 
                anchor=tk.CENTER).grid(column=0, row=0, columnspan=2, 
                sticky=tk.EW, pady=5)

        ttk.Label(frame, text="Código").grid(column=0, row=1, 
                sticky=tk.EW, padx=5, pady=2)
        self.__codigo = tk.IntVar(); 
        ttk.Entry(frame, textvariable=self.__codigo, state=tk.DISABLED,
                justify=tk.RIGHT).grid(column=1, row=1, 
                 sticky=tk.EW, padx=5, pady=2)

        ttk.Label(frame, text="Nombre").grid(column=0, row=2, 
                sticky=tk.EW, padx=5, pady=2)
        self.__nombre = tk.StringVar(); 
        ttk.Entry(frame, textvariable=self.__nombre).grid(column=1, row=2, 
                sticky=tk.EW, padx=5, pady=2)

        ttk.Label(frame, text="Precio").grid(column=0, row=3, 
                sticky=tk.EW, padx=5, pady=2)
        self.__precio = tk.DoubleVar(); 
        ttk.Entry(frame, textvariable=self.__precio, 
                justify=tk.RIGHT).grid(column=1, row=3, 
                sticky=tk.EW, padx=5, pady=2)

        botones = tk.Frame(frame, relief=tk.RIDGE)
        botones.columnconfigure(0, weight=1)
        botones.columnconfigure(1, weight=1)
        botones.grid(column=0, row=4, columnspan=2, 
                sticky=tk.EW, padx=5, pady=15)

        def insertar():
            # TODO Validar los campos llenos
            producto = ProductoModel()
            producto.set_nombre(self.__nombre.get())
            producto.set_precio(self.__precio.get())

            try:
                # Envio a guardar a la base de datos
                self.__logica.insertar(producto)
                self.__cargar_tabla()

                messagebox.showinfo("Guardado de producto", "Se guardó de forma existosa")
            except Exception as ex:
                messagebox.showerror("Error guardando el producto", str(ex))

        self.__btnIngresar = ttk.Button(botones, text="Ingresar", 
                command=insertar)
        self.__btnIngresar.grid(column=0, row=0, sticky=tk.EW, padx=5)

        def actualizar():
            # TODO Validar los campos llenos
            producto = ProductoModel()
            producto.set_codigo(self.__codigo.get())
            producto.set_nombre(self.__nombre.get())
            producto.set_precio(self.__precio.get())

            try:
                # Envio a guardar a la base de datos
                self.__logica.actualizar(producto)
                self.__cargar_tabla()

                messagebox.showinfo("Actualizar de producto", "Se actualizó de forma existosa")
            except:
                messagebox.showerror("Actualizar de producto", "Error al actualizar el producto")

        self.__btnActualizar = ttk.Button(botones, text="Actualizar", 
                state=tk.DISABLED, command=actualizar)
        self.__btnActualizar.grid(column=1,row=0, sticky=tk.EW, padx=5)

    def __cargar_tabla(self):
        productos = self.__logica.listar()

        # Eliminar los valores anteriores
        for item in self.__tabla.get_children(""):
            self.__tabla.delete(item)

        # Establecer el formato de precio
        locale.setlocale(locale.LC_ALL, '')  # Utilizar la configuración regional actual del sistema

        for producto in productos:
            identificador = producto.get_codigo()
            precio_formateado = locale.currency(producto.get_precio(), grouping=True)
            self.__tabla.insert(parent='', index=identificador, iid=identificador, text="",
            values=(identificador, producto.get_nombre(), precio_formateado))

    def iniciar_ejecucion(self):
        self.mainloop()