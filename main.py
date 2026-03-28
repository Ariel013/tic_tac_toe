"""
Tic Tac Toe — entry point.

Run locally:
    python main.py

Deploy to web (requires pygbag):
    pygbag main.py
    # then open http://localhost:8000

Build executable (requires pyinstaller):
    pyinstaller --onefile --add-data "pictures:pictures" main.py
"""

import asyncio
import sys
import time

import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN

from constants import WIDTH, HEIGHT, STATUS_HEIGHT, FPS, COVER_DURATION, RESULT_DURATION
from game_state import GameState
from renderer import Renderer


class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT + STATUS_HEIGHT), 0, 32)
        pygame.display.set_caption("Tic Tac Toe")
        self.clock = pygame.time.Clock()
        self.state = GameState()
        self.renderer = Renderer(self.screen)
        self._start_cover()

    def _start_cover(self):
        self.showing_cover = True
        self.cover_start = time.time()
        self.result_start = None
        self.renderer.draw_cover()

    def handle_click(self, pos):
        x, y = pos
        if self.showing_cover:
            self.showing_cover = False
            return
        if self.result_start is not None or self.state.winner or self.state.is_draw:
            return
        if x >= WIDTH or y >= HEIGHT:
            return
        col = x * 3 // WIDTH
        row = y * 3 // HEIGHT
        if self.state.make_move(row, col):
            self.renderer.render(self.state)
            if self.state.winner or self.state.is_draw:
                self.result_start = time.time()

    def update(self):
        now = time.time()
        if self.showing_cover and now - self.cover_start >= COVER_DURATION:
            self.showing_cover = False

        if not self.showing_cover and self.result_start is None:
            self.renderer.render(self.state)

        if self.result_start is not None and now - self.result_start >= RESULT_DURATION:
            self.state.reset()
            self._start_cover()

    async def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            self.update()
            self.clock.tick(FPS)
            await asyncio.sleep(0)


async def main():
    app = App()
    await app.run()


asyncio.run(main())
