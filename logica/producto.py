from logica.conexion import conectar
from modelo.producto import ProductoModel

class ProductoLogica:

    def listar(self):
        sql = "SELECT codigo, nombre, precio FROM producto ORDER BY codigo asc"
        mysql = conectar()
        cursor = mysql.cursor()
        cursor.execute(sql)
        resultados = cursor.fetchall() # [(1,'camisa',10.0),(2,'pantalon',15.0)]
        mysql.close()

        # productos = list(map(lambda dato: ProductoModel(dato[0],dato[1],dato[2]), resultados));

        productos = []
        for dato in resultados:
            # producto = ProductoModel()
            # producto.set_codigo(dato[0])
            # producto.set_nombre(dato[1])
            # producto.set_precio(dato[2])
            # productos.append(producto)

            productos.append(ProductoModel(dato[0], dato[1], dato[2]))

        return productos

    def insertar(self, producto: ProductoModel):
        sql = "INSERT INTO producto (nombre, precio) VALUES ('%s', %f)" % (producto.get_nombre(), producto.get_precio())

        mysql = conectar()
        cursor = mysql.cursor()
        print(sql)
        cursor.execute(sql)
        mysql.commit()
        mysql.close()

    def actualizar(self, producto: ProductoModel):
        sql = f"UPDATE producto SET nombre = '{producto.get_nombre()}', precio = {producto.get_precio()} WHERE codigo = {producto.get_codigo()}"

        mysql = conectar()
        cursor = mysql.cursor()
        cursor.execute(sql)
        mysql.commit()
        mysql.close()

    def eliminar(self, codigo: int):
        sql = "DELETE FROM producto WHERE codigo = %s" % (codigo)
        # %s -> str
        # %f -> float
        # %d -> int

        mysql = conectar()
        cursor = mysql.cursor()
        cursor.execute(sql)
        mysql.commit()
        mysql.close()