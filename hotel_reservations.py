"""
Este es un programa que contiene las clases hotel, cliente y reservación,
en el se pueden crear hoteles, clientes y reservaciones
que persisten en archivos creados y modificados por el mismo programa.

Cumple con el estandard PEP-8 y no muestra errores en pylint ni en flake8
"""


import json
import os
from datetime import datetime


def leer_archivo(nombre_archivo):
    """
    Lee un archivo JSON
    """
    if not os.path.exists(nombre_archivo):
        return []

    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        if not isinstance(datos, list):
            print(
                f"[ERROR] {nombre_archivo} no es JSON váloido"
            )
            return []

        return datos

    except json.JSONDecodeError:
        print(f"[ERROR] {nombre_archivo} no contiene JSON válido.")
        return []

    except OSError as error:
        print(f"[ERROR] No se pudo acceder al archivo: {error}")
        return []


def escribir_archivo(nombre_archivo, datos):
    """
    Escribir los datos a un archivo JSON.
    """
    try:
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4)
    except OSError as error:
        print(f"[ERROR] No se pudoo crear el archivo: {error}")


class Hotel:
    """Representa el objeto Hotel."""

    ARCHIVO = "hoteles.json"

    @classmethod
    def crear_hotel(cls, nombre, total_habitaciones):
        """Funcion para crear un hotel nuevo."""
        hoteles = leer_archivo(cls.ARCHIVO)
        id_hotel = len(hoteles) + 1

        nuevo_hotel = {
            "id_hotel": id_hotel,
            "nombre": nombre,
            "total_habitaciones": total_habitaciones,
            "habitaciones_disponibles": total_habitaciones,
        }

        hoteles.append(nuevo_hotel)
        escribir_archivo(cls.ARCHIVO, hoteles)

    @classmethod
    def mostrar_hoteles(cls):
        """Muestra la lista de hoteles."""
        hoteles = leer_archivo(cls.ARCHIVO)
        hoteles_validos = []

        for hotel in hoteles:
            try:
                if (
                    "id_hotel" in hotel
                    and "nombre" in hotel
                    and "habitaciones_disponibles" in hotel
                ):
                    hoteles_validos.append(hotel)
                else:
                    print("[ERROR] Registro de hotel invalido.")
            except (TypeError, KeyError):
                print("[ERROR] Registro de hotel invalido.")

        return hoteles_validos

    @classmethod
    def reservar_habitacion(cls, id_hotel):
        """Funcion para hacer una registrar una reservación."""
        hoteles = leer_archivo(cls.ARCHIVO)

        for hotel in hoteles:
            try:
                if hotel["id_hotel"] == id_hotel:
                    if hotel["habitaciones_disponibles"] > 0:
                        hotel["habitaciones_disponibles"] -= 1
                        escribir_archivo(cls.ARCHIVO, hoteles)
                        return True
                    return False
            except KeyError:
                print("[ERROR] Registro de hotel invalido.")

        return False

    @classmethod
    def cancelar_reserva(cls, id_hotel):
        """Función para cancelar reservación."""
        hoteles = leer_archivo(cls.ARCHIVO)

        for hotel in hoteles:
            try:
                if hotel["id_hotel"] == id_hotel:
                    hotel["habitaciones_disponibles"] += 1
                    break
            except KeyError:
                print("[ERROR] Registro de hotel invalido")

        escribir_archivo(cls.ARCHIVO, hoteles)


class Cliente:
    """Clase de cliente."""

    ARCHIVO = "clientes.json"

    @classmethod
    def crear_cliente(cls, nombre, correo):
        """Función para crear un cliente."""
        clientes = leer_archivo(cls.ARCHIVO)
        id_cliente = len(clientes) + 1

        nuevo_cliente = {
            "id_cliente": id_cliente,
            "nombre": nombre,
            "correo": correo,
        }

        clientes.append(nuevo_cliente)
        escribir_archivo(cls.ARCHIVO, clientes)

    @classmethod
    def mostrar_clientes(cls):
        """Muestra los clientes"""
        clientes = leer_archivo(cls.ARCHIVO)
        clientes_validos = []

        for cliente in clientes:
            try:
                if "id_cliente" in cliente and "nombre" in cliente:
                    clientes_validos.append(cliente)
                else:
                    print("[ERROR] Registro de cliente invalido")
            except (TypeError, KeyError):
                print("[ERROR]Registro de cliente invalido.")

        return clientes_validos


class Reservacion:
    """Clase de reservación"""

    ARCHIVO = "reservaciones.json"

    @classmethod
    def crear_reservacion(cls, id_cliente, id_hotel):
        """Crear una reservación"""
        if not Hotel.reservar_habitacion(id_hotel):
            return False

        reservaciones = leer_archivo(cls.ARCHIVO)
        id_reservacion = len(reservaciones) + 1

        nueva_reservacion = {
            "id_reservacion": id_reservacion,
            "id_cliente": id_cliente,
            "id_hotel": id_hotel,
            "fecha": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        }

        reservaciones.append(nueva_reservacion)
        escribir_archivo(cls.ARCHIVO, reservaciones)

        return True

    @classmethod
    def cancelar_reservacion(cls, id_reservacion):
        """Funcion para cancelar reservaciones."""
        reservaciones = leer_archivo(cls.ARCHIVO)

        for reservacion in reservaciones:
            try:
                if reservacion["id_reservacion"] == id_reservacion:
                    Hotel.cancelar_reserva(
                        reservacion["id_hotel"]
                    )
                    reservaciones.remove(reservacion)
                    escribir_archivo(cls.ARCHIVO, reservaciones)
                    return True
            except KeyError:
                print("[ERROR] Registro de reservaciones erróneo.")

        return False


def main():
    """Ejecuta la función principal del programa"""
    # Crear hotel
    Hotel.crear_hotel("Hotel Rojo", 6)

    # Crear cliente
    Cliente.crear_cliente("Rodrigo", "rodrigo@email.com")

    # Mostrar hoteles
    print("Hoteles:")
    print(Hotel.mostrar_hoteles())

    # Mostrar clientes
    print("\nClientes:")
    print(Cliente.mostrar_clientes())

    # Crear reservación
    print("\nCreando reservación...")
    exito = Reservacion.crear_reservacion(1, 1)
    print("Reservación exitosa:", exito)

    # Cancelar reservación
    print("\nCancelando reservación...")
    exito = Reservacion.cancelar_reservacion(1)
    print("Cancelación exitosa:", exito)


if __name__ == "__main__":
    main()
