from abc import ABC, abstractmethod
from typing import Callable, Tuple
from constants import MouseButton
from pygame import Surface

class Scene(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def start(self, change_scene: Callable[['Scene'], None], resize_screen: Callable[[Tuple[int, int]], None]) -> None:
        pass

    @abstractmethod
    def handle_click(self, btn: MouseButton, pos: Tuple[int, int]) -> None:
        pass

    @abstractmethod
    def draw(self, screen: Surface) -> None:
        pass
