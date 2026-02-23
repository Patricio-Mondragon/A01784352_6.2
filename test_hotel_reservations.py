import os
import unittest

from hotel_reservations import Hotel, Cliente, Reservacion


class TestSistemaHotel(unittest.TestCase):

    def setUp(self):
        """Se ejecuta antes de cada prueba."""
        # Limpiar archivos antes de cada test
        for archivo in [
            "hoteles.json",
            "clientes.json",
            "reservaciones.json",
        ]:
            if os.path.exists(archivo):
                os.remove(archivo)

    def test_1_crear_hotel(self):
        """Debe crear un hotel correctamente."""
        Hotel.crear_hotel("Hotel Test", 10)
        hoteles = Hotel.mostrar_hoteles()

        self.assertEqual(len(hoteles), 1)
        self.assertEqual(hoteles[0]["nombre"], "Hotel Test")
        self.assertEqual(hoteles[0]["habitaciones_disponibles"], 10)

    def test_2_crear_cliente(self):
        """Debe crear un cliente correctamente."""
        Cliente.crear_cliente("Juan", "juan@email.com")
        clientes = Cliente.mostrar_clientes()

        self.assertEqual(len(clientes), 1)
        self.assertEqual(clientes[0]["nombre"], "Juan")

    def test_3_crear_reservacion(self):
        """Debe crear una reservación si hay habitaciones."""
        Hotel.crear_hotel("Hotel Azul", 5)
        Cliente.crear_cliente("Ana", "ana@email.com")

        resultado = Reservacion.crear_reservacion(1, 1)

        self.assertTrue(resultado)

        hoteles = Hotel.mostrar_hoteles()
        self.assertEqual(hoteles[0]["habitaciones_disponibles"], 4)

    def test_4_cancelar_reservacion(self):
        """Debe cancelar reservación y liberar habitación."""
        Hotel.crear_hotel("Hotel Azul", 5)
        Cliente.crear_cliente("Ana", "ana@email.com")

        Reservacion.crear_reservacion(1, 1)
        resultado = Reservacion.cancelar_reservacion(1)

        self.assertTrue(resultado)

        hoteles = Hotel.mostrar_hoteles()
        self.assertEqual(hoteles[0]["habitaciones_disponibles"], 5)

    def test_5_no_reserva_sin_habitaciones(self):
        """No debe permitir reservar si no hay habitaciones."""
        Hotel.crear_hotel("Hotel Lleno", 1)
        Cliente.crear_cliente("Luis", "luis@email.com")

        Reservacion.crear_reservacion(1, 1)
        resultado = Reservacion.crear_reservacion(1, 1)

        self.assertFalse(resultado)


if __name__ == "__main__":
    unittest.main()