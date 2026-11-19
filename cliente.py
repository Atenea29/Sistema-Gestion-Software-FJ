"""Clase Cliente con encapsulación y validaciones."""

import re  # Expresiones regulares para validar correo y teléfono

from entidad import Entidad  # Clase abstracta general
from excepciones import ClienteInvalidoError  # Error específico de datos de cliente


class Cliente(Entidad):
    """Cliente de Software FJ. Sus atributos son privados y se validan al asignarlos."""

    def __init__(self, identificador, nombre, documento, correo, telefono):
        super().__init__(identificador)  # Valida y guarda el id
        # Al asignar se ejecutan los setters, que validan cada dato
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    # ---- nombre -------------------------------------------------------
    @property
    def nombre(self):
        return self.__nombre  # Atributo privado (name mangling: _Cliente__nombre)

    @nombre.setter
    def nombre(self, valor):
        # Mínimo 3 caracteres, solo letras y espacios (incluye tildes y ñ)
        if not isinstance(valor, str) or not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]{3,60}", valor.strip()):
            raise ClienteInvalidoError(f"Nombre inválido: {valor!r} (3 a 60 letras)")
        if "  " in valor.strip():  # Dos o más espacios seguidos dentro del nombre
            raise ClienteInvalidoError(f"Nombre inválido: {valor!r} (no se permiten espacios dobles)")
        self.__nombre = valor.strip().title()  # Se normaliza a formato Título

    # ---- documento ----------------------------------------------------
    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        # Solo dígitos, entre 5 y 12
        if not isinstance(valor, str) or not re.fullmatch(r"\d{5,12}", valor):
            raise ClienteInvalidoError(f"Documento inválido: {valor!r} (5 a 12 dígitos)")
        self.__documento = valor

    # ---- correo -------------------------------------------------------
    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        # Formato básico usuario@dominio.ext
        if not isinstance(valor, str) or not re.fullmatch(r"[\w.+-]+@[\w-]+(\.[\w-]+)+", valor):
            raise ClienteInvalidoError(f"Correo inválido: {valor!r}")
        usuario = valor.split("@")[0]  # Parte anterior a la arroba
        if ".." in valor or usuario.startswith(".") or usuario.endswith("."):
            raise ClienteInvalidoError(f"Correo inválido: {valor!r} (puntos mal ubicados)")
        if len(valor) > 60:  # Límite razonable de longitud
            raise ClienteInvalidoError(f"Correo inválido: supera los 60 caracteres ({len(valor)})")
        self.__correo = valor.lower()

    # ---- teléfono -----------------------------------------------------
    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        # Celular colombiano: 10 dígitos que empiezan por 3
        if not isinstance(valor, str) or not re.fullmatch(r"3\d{9}", valor):
            raise ClienteInvalidoError(f"Teléfono inválido: {valor!r} (10 dígitos, inicia en 3)")
        self.__telefono = valor

    def correo_enmascarado(self):
        """Devuelve el correo ocultando el usuario (protege datos personales): a**@correo.com."""
        usuario, dominio = self.correo.split("@")  # Separa usuario y dominio
        return f"{usuario[0]}{'*' * (len(usuario) - 1)}@{dominio}"

    def describir(self):
        """Implementación del método abstracto de Entidad."""
        return f"Cliente #{self.id}: {self.nombre} (doc. {self.documento})"
