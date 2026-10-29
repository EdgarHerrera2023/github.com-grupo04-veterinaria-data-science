"""
Sistema de Gestión - Clínica Veterinaria
Entrega 2 - Aplicación en Python con MySQL y POO
Grupo 04: Arroyo, Bertetti, Bertetti, Herrera
"""

import mysql.connector
from mysql.connector import Error


# ============================================================
# CLASE DE CONEXIÓN A LA BASE DE DATOS
# ============================================================
class ConexionDB:
    """Se encarga de gestionar la conexión con MySQL."""

    def __init__(self):
        self.host = "localhost"
        self.user = "root"              # Cambiar si es necesario
        self.password = ""              # Colocar tu contraseña
        self.database = "clinica_veterinaria"
        self.conexion = None

    def conectar(self):
        try:
            self.conexion = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return self.conexion.is_connected()
        except Error as e:
            print(f"Error al conectar con la base de datos: {e}")
            return False

    def desconectar(self):
        if self.conexion and self.conexion.is_connected():
            self.conexion.close()

    def ejecutar(self, query, params=None, fetch=False):
        """Ejecuta una consulta. Si fetch=True devuelve los resultados."""
        try:
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute(query, params or ())
            if fetch:
                resultado = cursor.fetchall()
                cursor.close()
                return resultado
            self.conexion.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error en la consulta: {e}")
            return None


# ============================================================
# CLASE CLIENTE
# ============================================================
class Cliente:
    def __init__(self, db: ConexionDB):
        self.db = db

    def alta(self, nombre, apellido, telefono, email, direccion):
        query = """
            INSERT INTO clientes (nombre, apellido, telefono, email, direccion)
            VALUES (%s, %s, %s, %s, %s)
        """
        return self.db.ejecutar(query, (nombre, apellido, telefono, email, direccion))

    def baja(self, id_cliente):
        query = "DELETE FROM clientes WHERE id_cliente = %s"
        return self.db.ejecutar(query, (id_cliente,))

    def modificar(self, id_cliente, nombre, apellido, telefono, email, direccion):
        query = """
            UPDATE clientes
            SET nombre = %s, apellido = %s, telefono = %s, email = %s, direccion = %s
            WHERE id_cliente = %s
        """
        return self.db.ejecutar(query, (nombre, apellido, telefono, email, direccion, id_cliente))

    def listar(self):
        return self.db.ejecutar("SELECT * FROM clientes ORDER BY id_cliente", fetch=True)

    def buscar_por_apellido(self, apellido):
        query = "SELECT * FROM clientes WHERE apellido LIKE %s"
        return self.db.ejecutar(query, (f"%{apellido}%",), fetch=True)


# ============================================================
# CLASE MASCOTA
# ============================================================
class Mascota:
    def __init__(self, db: ConexionDB):
        self.db = db

    def alta(self, nombre, especie, raza, edad, peso, id_cliente):
        query = """
            INSERT INTO mascotas (nombre, especie, raza, edad, peso, id_cliente)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        return self.db.ejecutar(query, (nombre, especie, raza, edad, peso, id_cliente))

    def listar(self):
        return self.db.ejecutar("SELECT * FROM mascotas ORDER BY id_mascota", fetch=True)

    def buscar_por_especie(self, especie):
        query = "SELECT * FROM mascotas WHERE especie LIKE %s"
        return self.db.ejecutar(query, (f"%{especie}%",), fetch=True)


# ============================================================
# CLASE VETERINARIO
# ============================================================
class Veterinario:
    def __init__(self, db: ConexionDB):
        self.db = db

    def listar(self):
        return self.db.ejecutar("SELECT * FROM veterinarios ORDER BY id_veterinario", fetch=True)


# ============================================================
# CLASE CONSULTA
# ============================================================
class Consulta:
    def __init__(self, db: ConexionDB):
        self.db = db

    def alta(self, fecha, motivo, diagnostico, costo, id_mascota, id_veterinario):
        query = """
            INSERT INTO consultas (fecha, motivo, diagnostico, costo, id_mascota, id_veterinario)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        return self.db.ejecutar(query, (fecha, motivo, diagnostico, costo, id_mascota, id_veterinario))

    def baja(self, id_consulta):
        query = "DELETE FROM consultas WHERE id_consulta = %s"
        return self.db.ejecutar(query, (id_consulta,))

    def modificar(self, id_consulta, fecha, motivo, diagnostico, costo, id_mascota, id_veterinario):
        query = """
            UPDATE consultas
            SET fecha = %s, motivo = %s, diagnostico = %s, costo = %s,
                id_mascota = %s, id_veterinario = %s
            WHERE id_consulta = %s
        """
        return self.db.ejecutar(
            query,
            (fecha, motivo, diagnostico, costo, id_mascota, id_veterinario, id_consulta)
        )

    def listar(self):
        return self.db.ejecutar("SELECT * FROM consultas ORDER BY fecha DESC", fetch=True)

    def buscar_por_fecha(self, fecha):
        query = "SELECT * FROM consultas WHERE fecha = %s"
        return self.db.ejecutar(query, (fecha,), fetch=True)

    def buscar_por_motivo(self, motivo):
        query = "SELECT * FROM consultas WHERE motivo LIKE %s"
        return self.db.ejecutar(query, (f"%{motivo}%",), fetch=True)

    def consultar_vista(self):
        """Consulta la vista creada en MySQL."""
        query = "SELECT * FROM vista_consultas_completas LIMIT 20"
        return self.db.ejecutar(query, fetch=True)


# ============================================================
# MENÚ Y FUNCIÓN PRINCIPAL
# ============================================================
def mostrar_menu():
    print("\n" + "=" * 55)
    print("   SISTEMA DE GESTIÓN - CLÍNICA VETERINARIA")
    print("=" * 55)
    print("1.  Alta de Cliente")
    print("2.  Baja de Cliente")
    print("3.  Modificar Cliente")
    print("4.  Listar Clientes")
    print("5.  Buscar Cliente por Apellido")
    print("6.  Alta de Mascota")
    print("7.  Listar Mascotas")
    print("8.  Buscar Mascota por Especie")
    print("9.  Alta de Consulta")
    print("10. Baja de Consulta")
    print("11. Modificar Consulta")
    print("12. Listar Consultas")
    print("13. Buscar Consulta por Fecha")
    print("14. Buscar Consulta por Motivo")
    print("15. Ver Vista Completa de Consultas")
    print("16. Listar Veterinarios")
    print("0.  Salir")
    print("=" * 55)


def main():
    db = ConexionDB()
    if not db.conectar():
        print("No se pudo establecer la conexión. Verifique usuario y contraseña.")
        return

    print("✓ Conexión exitosa a la base de datos 'clinica_veterinaria'")

    cliente = Cliente(db)
    mascota = Mascota(db)
    veterinario = Veterinario(db)
    consulta = Consulta(db)

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            print("\n--- ALTA DE CLIENTE ---")
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            telefono = input("Teléfono: ")
            email = input("Email: ")
            direccion = input("Dirección: ")
            if cliente.alta(nombre, apellido, telefono, email, direccion):
                print("✓ Cliente agregado correctamente.")

        elif opcion == "2":
            print("\n--- BAJA DE CLIENTE ---")
            id_cli = input("ID del cliente a eliminar: ")
            if cliente.baja(id_cli):
                print("✓ Cliente eliminado.")

        elif opcion == "3":
            print("\n--- MODIFICAR CLIENTE ---")
            id_cli = input("ID del cliente: ")
            nombre = input("Nuevo nombre: ")
            apellido = input("Nuevo apellido: ")
            telefono = input("Nuevo teléfono: ")
            email = input("Nuevo email: ")
            direccion = input("Nueva dirección: ")
            if cliente.modificar(id_cli, nombre, apellido, telefono, email, direccion):
                print("✓ Cliente modificado.")

        elif opcion == "4":
            print("\n--- LISTADO DE CLIENTES ---")
            datos = cliente.listar()
            if datos:
                for c in datos:
                    print(f"ID: {c['id_cliente']} | {c['nombre']} {c['apellido']} | Tel: {c['telefono']}")

        elif opcion == "5":
            print("\n--- BUSCAR CLIENTE POR APELLIDO ---")
            ape = input("Apellido (o parte): ")
            datos = cliente.buscar_por_apellido(ape)
            if datos:
                for c in datos:
                    print(f"ID: {c['id_cliente']} | {c['nombre']} {c['apellido']} | {c['email']}")
            else:
                print("No se encontraron resultados.")

        elif opcion == "6":
            print("\n--- ALTA DE MASCOTA ---")
            nombre = input("Nombre: ")
            especie = input("Especie (Perro/Gato): ")
            raza = input("Raza: ")
            edad = input("Edad: ")
            peso = input("Peso: ")
            id_cli = input("ID del dueño: ")
            if mascota.alta(nombre, especie, raza, edad, peso, id_cli):
                print("✓ Mascota agregada.")

        elif opcion == "7":
            print("\n--- LISTADO DE MASCOTAS ---")
            datos = mascota.listar()
            if datos:
                for m in datos:
                    print(f"ID: {m['id_mascota']} | {m['nombre']} | {m['especie']} | Dueño ID: {m['id_cliente']}")

        elif opcion == "8":
            print("\n--- BUSCAR MASCOTA POR ESPECIE ---")
            esp = input("Especie: ")
            datos = mascota.buscar_por_especie(esp)
            if datos:
                for m in datos:
                    print(f"ID: {m['id_mascota']} | {m['nombre']} | {m['raza']} | Edad: {m['edad']}")
            else:
                print("No se encontraron resultados.")

        elif opcion == "9":
            print("\n--- ALTA DE CONSULTA ---")
            fecha = input("Fecha (YYYY-MM-DD): ")
            motivo = input("Motivo: ")
            diagnostico = input("Diagnóstico: ")
            costo = input("Costo: ")
            id_masc = input("ID Mascota: ")
            id_vet = input("ID Veterinario: ")
            if consulta.alta(fecha, motivo, diagnostico, costo, id_masc, id_vet):
                print("✓ Consulta registrada.")

        elif opcion == "10":
            print("\n--- BAJA DE CONSULTA ---")
            id_con = input("ID de la consulta: ")
            if consulta.baja(id_con):
                print("✓ Consulta eliminada.")

        elif opcion == "11":
            print("\n--- MODIFICAR CONSULTA ---")
            id_con = input("ID de la consulta: ")
            fecha = input("Nueva fecha (YYYY-MM-DD): ")
            motivo = input("Nuevo motivo: ")
            diagnostico = input("Nuevo diagnóstico: ")
            costo = input("Nuevo costo: ")
            id_masc = input("Nuevo ID Mascota: ")
            id_vet = input("Nuevo ID Veterinario: ")
            if consulta.modificar(id_con, fecha, motivo, diagnostico, costo, id_masc, id_vet):
                print("✓ Consulta modificada.")

        elif opcion == "12":
            print("\n--- LISTADO DE CONSULTAS ---")
            datos = consulta.listar()
            if datos:
                for c in datos:
                    print(f"ID: {c['id_consulta']} | {c['fecha']} | {c['motivo']} | ${c['costo']}")

        elif opcion == "13":
            print("\n--- BUSCAR CONSULTA POR FECHA ---")
            fecha = input("Fecha (YYYY-MM-DD): ")
            datos = consulta.buscar_por_fecha(fecha)
            if datos:
                for c in datos:
                    print(f"ID: {c['id_consulta']} | {c['motivo']} | ${c['costo']}")
            else:
                print("No se encontraron resultados.")

        elif opcion == "14":
            print("\n--- BUSCAR CONSULTA POR MOTIVO ---")
            motivo = input("Motivo (o parte): ")
            datos = consulta.buscar_por_motivo(motivo)
            if datos:
                for c in datos:
                    print(f"ID: {c['id_consulta']} | {c['fecha']} | {c['motivo']} | ${c['costo']}")
            else:
                print("No se encontraron resultados.")

        elif opcion == "15":
            print("\n--- VISTA COMPLETA DE CONSULTAS ---")
            datos = consulta.consultar_vista()
            if datos:
                for c in datos:
                    print(f"{c['fecha']} | {c['nombre_mascota']} ({c['especie']}) | "
                          f"Dueño: {c['dueño']} | Vet: {c['veterinario']} | ${c['costo']}")
            else:
                print("No se pudo obtener la vista. Verifique que exista en MySQL.")

        elif opcion == "16":
            print("\n--- LISTADO DE VETERINARIOS ---")
            datos = veterinario.listar()
            if datos:
                for v in datos:
                    print(f"ID: {v['id_veterinario']} | {v['nombre']} {v['apellido']} | {v['especialidad']}")

        elif opcion == "0":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción no válida.")

        input("\nPresione Enter para continuar...")

    db.desconectar()
    print("Conexión cerrada. ¡Hasta luego!")


if __name__ == "__main__":
    main()