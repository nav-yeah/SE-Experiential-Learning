import random
import math
import pygame
from game.color_button import ColorButton


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        pad_size = 130
        gap = 24
        start_x = width // 2 - pad_size - (gap // 2)
        start_y = 150

        self.buttons = [
            ColorButton(
                0,
                pygame.Rect(start_x, start_y, pad_size, pad_size),
                (110, 20, 20),
                (255, 50, 50)
            ),  # Red
            ColorButton(
                1,
                pygame.Rect(
                    start_x + pad_size + gap,
                    start_y,
                    pad_size,
                    pad_size
                ),
                (15, 60, 150),
                (40, 170, 255)
            ),  # Blue
            ColorButton(
                2,
                pygame.Rect(
                    start_x,
                    start_y + pad_size + gap,
                    pad_size,
                    pad_size
                ),
                (15, 100, 30),
                (50, 255, 90)
            ),  # Green
            ColorButton(
                3,
                pygame.Rect(
                    start_x + pad_size + gap,
                    start_y + pad_size + gap,
                    pad_size,
                    pad_size
                ),
                (140, 110, 10),
                (255, 235, 40)
            ),  # Yellow
        ]

        self.sequence = []
        self.player_input = []
        self.score = 0

        self.state = "WATCH"
        self.showing_step = 0
        self.step_start_time = 0

        # Dynamic playback speed
        self.flash_duration = 450
        self.pause_duration = 200
        self.is_flashing = False

        self.player_lit_button = None
        self.player_lit_start = 0
        self.player_flash_duration = 150

        # Player countdown
        self.player_turn_duration = 5000
        self.player_turn_start = 0

        # Sound effects
        self.sound_frequencies = {
            0: 261,   # Red
            1: 329,   # Blue
            2: 392,   # Green
            3: 523    # Yellow
        }

        self.sounds = {}
        self._create_sounds()

        self.font_title = pygame.font.SysFont(None, 40)
        self.font_medium = pygame.font.SysFont(None, 28)

        self.start_next_round()

    def _create_sounds(self):
        """
        Create simple tones for each color.

        pygame.mixer must already be initialized by the main program.
        """
        try:
            sample_rate = 44100

            for color_id, frequency in self.sound_frequencies.items():
                duration = 0.15
                samples = int(sample_rate * duration)

                sound_buffer = bytearray()

                for i in range(samples):
                    value = int(
                        32767
                        * 0.25
                        * math.sin(
                            2 * math.pi * frequency * i / sample_rate
                        )
                    )

                    sound_buffer += int(value).to_bytes(
                        2,
                        byteorder="little",
                        signed=True
                    )

                sound = pygame.mixer.Sound(buffer=bytes(sound_buffer))
                self.sounds[color_id] = sound

        except (pygame.error, ValueError):
            self.sounds = {}

    def play_color_sound(self, color_id):
        sound = self.sounds.get(color_id)

        if sound is not None:
            sound.play()

    def update_speed(self):
        """
        Make playback faster as the score increases.

        Minimum limits:
        flash >= 180 ms
        pause >= 80 ms
        """
        self.flash_duration = max(
            180,
            450 - self.score * 20
        )

        self.pause_duration = max(
            80,
            200 - self.score * 10
        )

    def start_next_round(self):
        new_color = random.randint(0, 3)

        # Add exactly one new color to the sequence.
        self.sequence.append(new_color)

        self.update_speed()

        self.player_input.clear()
        self.state = "WATCH"
        self.showing_step = 0
        self.step_start_time = pygame.time.get_ticks()
        self.is_flashing = True

        first_button = self.buttons[self.sequence[0]]
        first_button.is_lit = True
        self.play_color_sound(self.sequence[0])

    def start_player_turn(self):
        self.state = "PLAYER_TURN"
        self.player_turn_start = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()

        # Turn off player button after its flash duration.
        if self.player_lit_button is not None:
            if now - self.player_lit_start >= self.player_flash_duration:
                self.player_lit_button.is_lit = False
                self.player_lit_button = None

        if self.state == "WATCH":
            current_btn_id = self.sequence[self.showing_step]

            if self.is_flashing:
                if now - self.step_start_time >= self.flash_duration:
                    self.buttons[current_btn_id].is_lit = False
                    self.is_flashing = False
                    self.step_start_time = now

            else:
                if now - self.step_start_time >= self.pause_duration:
                    self.showing_step += 1

                    if self.showing_step < len(self.sequence):
                        next_id = self.sequence[self.showing_step]

                        self.buttons[next_id].is_lit = True
                        self.play_color_sound(next_id)

                        self.is_flashing = True
                        self.step_start_time = now

                    else:
                        self.start_player_turn()

        elif self.state == "PLAYER_TURN":
            elapsed = now - self.player_turn_start

            if elapsed >= self.player_turn_duration:
                self.state = "GAME_OVER"

    def handle_event(self, event):
        if self.state == "GAME_OVER":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()
            return

        if (
            self.state == "PLAYER_TURN"
            and event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):
            for btn in self.buttons:
                if btn.contains(event.pos):
                    btn.is_lit = True
                    self.player_lit_button = btn
                    self.player_lit_start = pygame.time.get_ticks()

                    self.play_color_sound(btn.color_id)
                    self.register_player_click(btn.color_id)
                    break

    def register_player_click(self, color_id):
        self.player_input.append(color_id)

        current_idx = len(self.player_input) - 1

        if self.player_input[current_idx] != self.sequence[current_idx]:
            self.state = "GAME_OVER"
            return

        if len(self.player_input) == len(self.sequence):
            self.score += 1
            self.start_next_round()

    def reset(self):
        self.sequence.clear()
        self.player_input.clear()
        self.score = 0

        for btn in self.buttons:
            btn.is_lit = False

        self.player_lit_button = None

        self.start_next_round()

    def render(self, screen):
        screen.fill((22, 24, 30))

        title_surf = self.font_title.render(
            "Memory Pattern Arena",
            True,
            (245, 245, 245)
        )
        screen.blit(
            title_surf,
            (
                self.width // 2 - title_surf.get_width() // 2,
                20
            )
        )

        score_surf = self.font_medium.render(
            f"Score: {self.score}",
            True,
            (255, 220, 80)
        )
        screen.blit(
            score_surf,
            (
                self.width // 2 - score_surf.get_width() // 2,
                60
            )
        )

        status_text = (
            "Watch the pattern..."
            if self.state == "WATCH"
            else "Your turn: Click the pattern!"
        )

        status_color = (
            (190, 195, 205)
            if self.state == "WATCH"
            else (80, 240, 130)
        )

        if self.state == "GAME_OVER":
            status_text = "Game Over - Press R to restart"
            status_color = (240, 70, 70)

        status_surf = self.font_medium.render(
            status_text,
            True,
            status_color
        )

        screen.blit(
            status_surf,
            (
                self.width // 2 - status_surf.get_width() // 2,
                95
            )
        )

        for btn in self.buttons:
            btn.render(screen)

        # Countdown bar during player's turn.
        if self.state == "PLAYER_TURN":
            elapsed = pygame.time.get_ticks() - self.player_turn_start
            remaining = max(
                0,
                self.player_turn_duration - elapsed
            )

            progress = remaining / self.player_turn_duration

            bar_width = 300
            bar_height = 18
            bar_x = self.width // 2 - bar_width // 2
            bar_y = 430

            pygame.draw.rect(
                screen,
                (60, 65, 75),
                (bar_x, bar_y, bar_width, bar_height),
                border_radius=8
            )

            pygame.draw.rect(
                screen,
                (80, 200, 120),
                (
                    bar_x,
                    bar_y,
                    int(bar_width * progress),
                    bar_height
                ),
                border_radius=8
            )

            timer_text = self.font_medium.render(
                f"Time: {remaining / 1000:.1f}s",
                True,
                (230, 230, 230)
            )

            screen.blit(
                timer_text,
                (
                    self.width // 2 - timer_text.get_width() // 2,
                    455
                )
            )

        if self.state == "GAME_OVER":
            overlay = pygame.Surface(
                (self.width, self.height),
                pygame.SRCALPHA
            )
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))

            over_surf = self.font_title.render(
                "WRONG PATTERN! GAME OVER",
                True,
                (240, 70, 70)
            )

            screen.blit(
                over_surf,
                (
                    self.width // 2 - over_surf.get_width() // 2,
                    self.height // 2 - 40
                )
            )

            final_score_surf = self.font_medium.render(
                f"Final Score: {self.score}",
                True,
                (255, 255, 255)
            )

            screen.blit(
                final_score_surf,
                (
                    self.width // 2 - final_score_surf.get_width() // 2,
                    self.height // 2 + 10
                )
            )

            restart_surf = self.font_medium.render(
                "Press [R] to Play Again",
                True,
                (200, 200, 200)
            )

            screen.blit(
                restart_surf,
                (
                    self.width // 2 - restart_surf.get_width() // 2,
                    self.height // 2 + 50
                )
            )