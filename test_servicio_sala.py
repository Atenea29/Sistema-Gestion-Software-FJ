"""Pruebas unitarias de Servicio y ReservaSala. Ejecutar: python -m unittest -v"""

import math
import unittest

from excepciones import (
    CalculoInconsistenteError,
    DatosInvalidosError,
    ParametroInvalidoError,
    ServicioNoDisponibleError,
)
from servicio import Servicio
from servicio_sala import ReservaSala


class ServicioSalaTests(unittest.TestCase):
    def setUp(self):
        self.sala = ReservaSala(101, "Sala Norte", 100_000, 12)

    def test_servicio_es_abstracta(self):
        with self.assertRaises(TypeError):
            Servicio(1, "Servicio", 100)

    def test_calculo_basico(self):
        self.assertEqual(self.sala.calcular_costo(2), 200_000.00)

    def test_calculo_con_descuento(self):
        self.assertEqual(self.sala.calcular_costo(2, 0.10), 180_000.00)

    def test_calculo_con_descuento_e_iva(self):
        self.assertEqual(self.sala.calcular_costo(2, 0.10, 0.19), 214_200.00)

    def test_rechaza_capacidad_decimal(self):
        with self.assertRaises(ParametroInvalidoError):
            ReservaSala(102, "Sala", 100_000, 5.5)

    def test_rechaza_capacidad_cero(self):
        with self.assertRaises(ParametroInvalidoError):
            ReservaSala(103, "Sala", 100_000, 0)

    def test_rechaza_capacidad_boolean(self):
        with self.assertRaises(ParametroInvalidoError):
            ReservaSala(104, "Sala", 100_000, True)

    def test_rechaza_nan_en_tarifa(self):
        with self.assertRaises(ParametroInvalidoError):
            ReservaSala(105, "Sala", math.nan, 5)

    def test_rechaza_porcentaje_infinito(self):
        with self.assertRaises(ParametroInvalidoError):
            self.sala.calcular_costo(2, math.inf)

    def test_rechaza_disponibilidad_no_booleana(self):
        with self.assertRaises(DatosInvalidosError):
            ReservaSala(106, "Sala", 100_000, 5, disponible="False")

    def test_no_calcula_si_no_esta_disponible(self):
        sala = ReservaSala(107, "Sala cerrada", 100_000, 5, disponible=False)
        with self.assertRaises(ServicioNoDisponibleError):
            sala.calcular_costo(1)

    def test_rechaza_mas_de_12_horas(self):
        with self.assertRaises(ParametroInvalidoError):
            self.sala.calcular_costo(13)


if __name__ == "__main__":
    unittest.main()
