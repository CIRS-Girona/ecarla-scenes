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

    # === Clock Functions === #
    def get_clock(self) -> Any:
        """Returns PyGame clock.
        """
        return self.clock

    def tick_clock(self) -> None:
        """Ticks PyGame clock.
        """
        self.clock.tick()

    def tick_clock_busy_loop(self, fps: int = 60) -> None:
        """Ticks PyGame clock busy loop.
        """
        self.clock.tick_busy_loop(fps)

    # === Rendering Functions === #
    def render_image(self, image: np.ndarray, blend: bool = False) -> None:
        """Renders image.
        """
        surf_data = pygame.surfarray.make_surface(
            image.swapaxes(0, 1)
        )
        if blend:
            surf_data.set_alpha(100)
        self.surface.blit(surf_data, (0, 0))

    def render_sim_time(self, time: float) -> None:
        """Renders simulation time.
        """
        self.surface.blit(self.font.render(
            "Simulation time: %s" % str(timedelta(seconds=time)),
            True, (255, 255, 255)
        ), (8, 10))

    def render_text(self, text: str) -> None:
        """Renders text.
        """
        self.surface.blit(
            self.font.render(text, True, (255, 255, 255)), (8, 26)
        )

    # === Quit Function === #
    def should_quit(self) -> bool:
        """Quits PyGame on key stroke.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    return True
        return False
