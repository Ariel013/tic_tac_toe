from pathlib import Path

import pygame

from constants import (
    WIDTH, HEIGHT, STATUS_HEIGHT,
    WHITE, BLACK, RED,
    CELL_SIZE, PIECE_SIZE, PIECE_MARGIN,
    LINE_WIDTH, WIN_LINE_WIDTH,
    GRAY, GRAY_HOVER, GREEN, ORANGE, RED_DARK,
)

PICTURES_DIR = Path(__file__).parent / "pictures"

TOTAL_HEIGHT = HEIGHT + STATUS_HEIGHT


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.pvp_button = pygame.Rect(0, 0, 0, 0)
        self.pva_button = pygame.Rect(0, 0, 0, 0)
        self.diff_buttons = {}
        self._load_assets()

    def _load_assets(self):
        cover = pygame.image.load(PICTURES_DIR / "modified_cover.png")
        self.cover = pygame.transform.scale(cover, (WIDTH, TOTAL_HEIGHT))

        x_raw = pygame.image.load(PICTURES_DIR / "X_modified.png")
        self.x_img = pygame.transform.scale(x_raw, (PIECE_SIZE, PIECE_SIZE))

        o_raw = pygame.image.load(PICTURES_DIR / "o_modified.png")
        self.o_img = pygame.transform.scale(o_raw, (PIECE_SIZE, PIECE_SIZE))

    def draw_cover(self):
        self.screen.blit(self.cover, (0, 0))
        pygame.display.update()

    def draw_menu(self):
        self.screen.fill(BLACK)
        font_title = pygame.font.Font(None, 56)
        font_btn = pygame.font.Font(None, 36)

        title = font_title.render("Tic Tac Toe", True, WHITE)
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 110)))

        self.pvp_button = pygame.Rect(WIDTH // 2 - 130, 210, 260, 60)
        pygame.draw.rect(self.screen, GRAY, self.pvp_button, border_radius=10)
        pvp_text = font_btn.render("Player vs Player", True, WHITE)
        self.screen.blit(pvp_text, pvp_text.get_rect(center=self.pvp_button.center))

        self.pva_button = pygame.Rect(WIDTH // 2 - 130, 310, 260, 60)
        pygame.draw.rect(self.screen, GRAY, self.pva_button, border_radius=10)
        pva_text = font_btn.render("Player vs AI", True, WHITE)
        self.screen.blit(pva_text, pva_text.get_rect(center=self.pva_button.center))

        pygame.display.update()

    def draw_difficulty(self):
        self.screen.fill(BLACK)
        font_title = pygame.font.Font(None, 46)
        font_btn = pygame.font.Font(None, 36)

        title = font_title.render("Choose difficulty", True, WHITE)
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 100)))

        difficulties = [
            ("Easy", "easy", 200, GREEN),
            ("Medium", "medium", 290, ORANGE),
            ("Hard", "hard", 380, RED_DARK),
        ]
        self.diff_buttons = {}
        for label, key, y, color in difficulties:
            rect = pygame.Rect(WIDTH // 2 - 110, y, 220, 58)
            pygame.draw.rect(self.screen, color, rect, border_radius=10)
            text = font_btn.render(label, True, WHITE)
            self.screen.blit(text, text.get_rect(center=rect.center))
            self.diff_buttons[key] = rect

        pygame.display.update()

    def draw_grid(self):
        self.screen.fill(WHITE)
        pygame.draw.line(self.screen, BLACK, (CELL_SIZE, 0), (CELL_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(self.screen, BLACK, (CELL_SIZE * 2, 0), (CELL_SIZE * 2, HEIGHT), LINE_WIDTH)
        pygame.draw.line(self.screen, BLACK, (0, CELL_SIZE), (WIDTH, CELL_SIZE), LINE_WIDTH)
        pygame.draw.line(self.screen, BLACK, (0, CELL_SIZE * 2), (WIDTH, CELL_SIZE * 2), LINE_WIDTH)

    def draw_pieces(self, board):
        for row in range(3):
            for col in range(3):
                if board[row][col] is not None:
                    x = col * CELL_SIZE + PIECE_MARGIN
                    y = row * CELL_SIZE + PIECE_MARGIN
                    img = self.x_img if board[row][col] == "X" else self.o_img
                    self.screen.blit(img, (x, y))

    def draw_winning_line(self, winning_line):
        if winning_line is None:
            return
        kind, idx = winning_line
        half = CELL_SIZE // 2
        if kind == "row":
            y = idx * CELL_SIZE + half
            pygame.draw.line(self.screen, RED, (0, y), (WIDTH, y), WIN_LINE_WIDTH)
        elif kind == "col":
            x = idx * CELL_SIZE + half
            pygame.draw.line(self.screen, RED, (x, 0), (x, HEIGHT), WIN_LINE_WIDTH)
        elif kind == "diag":
            if idx == 0:
                pygame.draw.line(self.screen, RED, (50, 50), (350, 350), WIN_LINE_WIDTH)
            else:
                pygame.draw.line(self.screen, RED, (350, 50), (50, 350), WIN_LINE_WIDTH)

    def draw_status(self, state, ai_player=None):
        if state.winner:
            if ai_player and state.winner == ai_player:
                message = "AI won!"
            else:
                message = f"{state.winner} won!"
        elif state.is_draw:
            message = "Draw!"
        elif ai_player and state.current_player == ai_player:
            message = "AI is thinking..."
        else:
            message = f"{state.current_player}'s Turn"

        font = pygame.font.Font(None, 30)
        text = font.render(message, True, WHITE)
        self.screen.fill(BLACK, (0, HEIGHT, WIDTH, STATUS_HEIGHT))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT + STATUS_HEIGHT // 2))
        self.screen.blit(text, text_rect)

    def render(self, state, ai_player=None):
        self.draw_grid()
        self.draw_pieces(state.board)
        if state.winner:
            self.draw_winning_line(state.get_winning_line())
        self.draw_status(state, ai_player=ai_player)
        pygame.display.update()
