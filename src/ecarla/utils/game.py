import pygame
import numpy as np
from datetime import timedelta

from typing import Any, Dict, List, Tuple, Callable


class Game():
    """PyGame window handler.
    """
    def __init__(self, resolution: Tuple[int, int]) -> None:
        self.resolution = resolution
        self._init_game()

    def _init_game(self) -> None:
        """Initializes PyGame window.
        """
        self.surface = None
        self.font = None
        self.clock = None

        pygame.init()
        self.surface = pygame.display.set_mode(
            size=(self.resolution[1], self.resolution[0]),
            flags=pygame.HWSURFACE | pygame.DOUBLEBUF
        )
        self.font = self.get_font()
        self.clock = pygame.time.Clock()

    # === General Functions === #
    @staticmethod
    def get_font() -> pygame.font.Font:
        """Returns PyGame default font based on operating system.
        """
        fonts = [f for f in pygame.font.get_fonts()]
        default_font = "ubuntumono"
        font = default_font if default_font in fonts else fonts[0]
        font = pygame.font.match_font(font)
        font = pygame.font.Font(font, 14)
        return font

    @staticmethod
    def flip() -> None:
        """Flips PyGame display.
        """
        pygame.display.flip()

    @staticmethod
    def quit() -> None:
        """Quits PyGame.
        """
        pygame.quit()
        print("PyGame window killed.")

    # === User Functions === #
    # TODO: Add code here
