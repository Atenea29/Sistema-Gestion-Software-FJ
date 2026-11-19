"""Clase abstracta general de la que heredan Cliente y Servicio."""

from abc import ABC, abstractmethod  # ABC y abstractmethod permiten definir clases abstractas

from excepciones import DatosInvalidosError  # Error para identificadores inválidos


class Entidad(ABC):
    """Clase abstracta general: toda entidad del sistema tiene un id y se puede describir."""

    def __init__(self, identificador):
        # bool es subclase de int en Python, por eso se excluye explícitamente
        if isinstance(identificador, bool) or not isinstance(identificador, int) or identificador <= 0:
            raise DatosInvalidosError(f"El identificador debe ser un entero positivo: {identificador!r}")
        self._id = identificador  # Atributo protegido (encapsulación)

    @property
    def id(self):
        """Solo lectura: el identificador no se puede modificar después de creado."""
        return self._id

    @abstractmethod
    def describir(self):
        """Método abstracto: cada subclase devuelve su propia descripción."""

    def __str__(self):
        # Polimorfismo: str(objeto) usa la descripción de la subclase concreta
        return self.describir()
    def __eq__(self, otro):
        # Dos entidades son iguales si son del mismo tipo y tienen el mismo id
        return type(self) is type(otro) and self._id == otro._id

    def __hash__(self):
        # Necesario al definir __eq__: permite usar entidades en sets y diccionarios
        return hash((type(self).__name__, self._id))

    def __repr__(self):
        # Representación técnica, útil al depurar: Cliente(id=1)
        return f"{type(self).__name__}(id={self._id})"
