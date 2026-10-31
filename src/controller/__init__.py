"""Controladores que fazem a interface entre modelos e PostgreSQL."""

from src.controller.controller_adocao import ControllerAdocao
from src.controller.controller_adotante import ControllerAdotante
from src.controller.controller_animal import ControllerAnimal

__all__ = ["ControllerAdocao", "ControllerAdotante", "ControllerAnimal"]

