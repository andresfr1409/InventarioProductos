class ProductoModel:
    def __init__(self,codigo=None,nombre=None,precio=None):
        self.__codigo = codigo
        self.__nombre = nombre
        self.__precio = precio

    def get_codigo(self):
        return self.__codigo

    def set_codigo(self, codigo):
        self.__codigo = codigo

    def get_nombre(self):
        return self.__nombre

    def set_nombre(self, nombre):
        self.__nombre = nombre

    def get_precio(self):
        return self.__precio

    def set_precio(self, precio):
        self.__precio = precio
