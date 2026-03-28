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

from constants import WIDTH, HEIGHT, STATUS_HEIGHT, FPS, COVER_DURATION, RESULT_DURATION, AI_DELAY
from game_state import GameState
from renderer import Renderer
from ai import get_ai_move

AI_PLAYER = "O"


class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT + STATUS_HEIGHT), 0, 32)
        pygame.display.set_caption("Tic Tac Toe")
        self.clock = pygame.time.Clock()
        self.state = GameState()
        self.renderer = Renderer(self.screen)
        self.mode = None        # "pvp" or "pva"
        self.difficulty = None  # "easy", "medium", "hard"
        self.ai_move_time = None
        self.result_start = None
        self._start_cover()

    def _start_cover(self):
        self.showing_cover = True
        self.cover_start = time.time()
        self.renderer.draw_cover()

    def _go_to_menu(self):
        self.showing_cover = False
        self.mode = None
        self.difficulty = None
        self.result_start = None
        self.ai_move_time = None
        self.renderer.draw_menu()

    def _start_game(self):
        self.state.reset()
        self.result_start = None
        self.ai_move_time = None
        self.renderer.render(self.state, ai_player=AI_PLAYER if self.mode == "pva" else None)

    def handle_click(self, pos):
        if self.showing_cover:
            self.showing_cover = False
            self._go_to_menu()
            return

        if self.mode is None:
            if self.renderer.pvp_button.collidepoint(pos):
                self.mode = "pvp"
                self._start_game()
            elif self.renderer.pva_button.collidepoint(pos):
                self.mode = "pva"
                self.renderer.draw_difficulty()
            return

        if self.mode == "pva" and self.difficulty is None:
            for diff, rect in self.renderer.diff_buttons.items():
                if rect.collidepoint(pos):
                    self.difficulty = diff
                    self._start_game()
            return

        # In-game click
        if self.result_start is not None or self.state.winner or self.state.is_draw:
            return
        if self.mode == "pva" and self.state.current_player == AI_PLAYER:
            return  # Block input during AI turn
        x, y = pos
        if x >= WIDTH or y >= HEIGHT:
            return

        col = x * 3 // WIDTH
        row = y * 3 // HEIGHT
        if self.state.make_move(row, col):
            ai_player = AI_PLAYER if self.mode == "pva" else None
            self.renderer.render(self.state, ai_player=ai_player)
            if self.state.winner or self.state.is_draw:
                self.result_start = time.time()
            elif self.mode == "pva" and self.state.current_player == AI_PLAYER:
                self.ai_move_time = time.time() + AI_DELAY

    def update(self):
        now = time.time()

        if self.showing_cover:
            if now - self.cover_start >= COVER_DURATION:
                self._go_to_menu()
            return

        if self.mode is None or (self.mode == "pva" and self.difficulty is None):
            return

        ai_player = AI_PLAYER if self.mode == "pva" else None

        # Trigger AI move after delay
        if (self.ai_move_time is not None
                and now >= self.ai_move_time
                and not self.state.winner
                and not self.state.is_draw):
            self.ai_move_time = None
            move = get_ai_move(self.state.board, AI_PLAYER, self.difficulty)
            if move:
                self.state.make_move(*move)
                self.renderer.render(self.state, ai_player=ai_player)
                if self.state.winner or self.state.is_draw:
                    self.result_start = time.time()

        # Reset after result display
        if self.result_start is not None and now - self.result_start >= RESULT_DURATION:
            self.state.reset()
            self._go_to_menu()
            return

        if self.result_start is None:
            self.renderer.render(self.state, ai_player=ai_player)

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
