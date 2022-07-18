import pygame
import sys
from logic import Board, Particle, WIDTH, HEIGHT, header, padding


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
WHITE = (255, 255, 255)

# Text fonts
title_font = pygame.font.Font("fonts/Pixeltype.ttf", 100)
win_font = pygame.font.Font("fonts/Pixeltype.ttf", 500)
button_font = pygame.font.Font("fonts/Pixeltype.ttf", 40)

# Turn AI mode on/off
ai_mode = True

# Text timers
text_gravity = 0
ai_safe_text_counter = 0
ai_random_text_counter = 0
particle_timer = 0
ai_particle_timer = 0
solve_mode = False
solve_counter = 0

board = Board(screen, 16, 16)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if board.game_over:
                if event.button == 1:
                    if outline.collidepoint(event.pos):
                        board.reset()
            else:
                if pygame.MOUSEBUTTONDOWN:
                    # Click particle
                    particle_timer = 70
                    particle = Particle(event.pos)

                    if ai_mode:
                        # Player has clicked on AI Move
                        if ai_outline.collidepoint(event.pos):
                            ai_move = board.ai_move()
                            if ai_move is None:
                                board.inference()
                                ai_move = board.ai_move()
                                if ai_move is None:
                                    # AI has made random move
                                    ai_random_text_counter = 255
                                    text_gravity = 0
                                    ai_particle_timer = 70
                                    random_move = board.ai_random_move()
                                    ai_particle = Particle(board.center(random_move))
                                else:
                                    # AI has made a safe move
                                    ai_particle_timer = 70
                                    ai_particle = Particle(board.center(ai_move[0]))
                                    ai_safe_text_counter = 255
                                    text_gravity = 0
                                    if ai_move[1]:
                                        board.mark_mine(ai_move[0])
                                    else:
                                        board.explore(ai_move[0])
                            else:
                                # AI has made a safe move
                                ai_particle_timer = 70
                                ai_particle = Particle(board.center(ai_move[0]))
                                ai_safe_text_counter = 255
                                text_gravity = 0
                                if ai_move[1]:
                                    board.mark_mine(ai_move[0])
                                else:
                                    board.explore(ai_move[0])

                        # Player has clicked on AI Solve
                        if solve_outline.collidepoint(event.pos):
                            solve_mode = True

                    # Click on board
                    board.click()

    screen.fill(BLACK)

    # Title
    title_text = title_font.render(f"MINESWEEPER", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, header // 2))
    screen.blit(title_text, title_rect)

    # Board
    board.draw_skeleton()
    board.draw()

    # Ai buttons
    if ai_mode:
        ai_text = button_font.render("AI Move", True, WHITE)
        ai_rect = ai_text.get_rect(midleft=(padding + 20, header // 2 + 90))
        ai_outline = ai_rect.copy()
        ai_outline.width += 40
        ai_outline.height += 20
        ai_outline.x -= 20
        ai_outline.y -= 15
        pygame.draw.rect(screen, WHITE, ai_outline, 3)
        screen.blit(ai_text, ai_rect)

        solve_text = button_font.render("AI Solve", True, WHITE)
        solve_rect = solve_text.get_rect(midleft=(padding + 20, header // 2 + 30))
        solve_outline = solve_rect.copy()
        solve_outline.width += 40
        solve_outline.height += 20
        solve_outline.x -= 20
        solve_outline.y -= 15
        pygame.draw.rect(screen, WHITE, solve_outline, 3)
        screen.blit(solve_text, solve_rect)

    # AI solved has been clicked
    if solve_mode:
        solve_counter += 1
        if solve_counter >= 70:
            ai_move = board.ai_move()
            if ai_move is None:
                board.inference()
                ai_move = board.ai_move()
                if ai_move is None:
                    # AI has made random move
                    ai_random_text_counter = 255
                    text_gravity = 0
                    ai_particle_timer = 70
                    random_move = board.ai_random_move()
                    ai_particle = Particle(board.center(random_move))
                else:
                    # AI has made a safe move
                    ai_particle_timer = 70
                    ai_particle = Particle(board.center(ai_move[0]))
                    ai_safe_text_counter = 255
                    text_gravity = 0
                    if ai_move[1]:
                        board.mark_mine(ai_move[0])
                    else:
                        board.explore(ai_move[0])
            else:
                # AI has made a safe move
                ai_particle_timer = 70
                ai_particle = Particle(board.center(ai_move[0]))
                ai_safe_text_counter = 255
                text_gravity = 0
                if ai_move[1]:
                    board.mark_mine(ai_move[0])
                else:
                    board.explore(ai_move[0])
            solve_counter = 0

    # AI safe moved text
    if ai_safe_text_counter > 0:
        ai_safe_text = button_font.render("AI has made a safe move.", True, (ai_safe_text_counter,
                                                                             ai_safe_text_counter,
                                                                             ai_safe_text_counter))
        ai_safe_rect = ai_safe_text.get_rect(center=(WIDTH // 2, header // 2 + 90 - int(text_gravity)))
        screen.blit(ai_safe_text, ai_safe_rect)
        ai_safe_text_counter -= 3
        text_gravity += 0.1

    # AI random moved text
    if ai_random_text_counter > 0:
        ai_random_text = button_font.render("AI has made a random move.", True, (ai_random_text_counter,
                                                                                 ai_random_text_counter,
                                                                                 ai_random_text_counter))
        ai_random_rect = ai_random_text.get_rect(center=(WIDTH // 2, header // 2 + 90 - int(text_gravity)))
        screen.blit(ai_random_text, ai_random_rect)
        ai_random_text_counter -= 2
        text_gravity += 0.1

    # Click particle
    if particle_timer > 0:
        particle.render(screen)
        particle_timer -= 1

    if ai_particle_timer > 0:
        ai_particle.render(screen)
        ai_particle_timer -= 1

    if board.game_over:
        solve_mode = False
        game_text = button_font.render("Reset", True, WHITE)
        game_rect = game_text.get_rect(midright=(WIDTH - padding - 25, header // 2 + 90))
        outline = game_rect.copy()
        outline.width += 40
        outline.height += 20
        outline.x -= 20
        outline.y -= 15
        pygame.draw.rect(screen, WHITE, outline, 3)
        screen.blit(game_text, game_rect)

    if board.won:
        win_text = title_font.render("YOU WIN", True, BLACK)
        win_rect = win_text.get_rect(center=(WIDTH//2, (HEIGHT-header)//2 + header))
        screen.blit(win_text, win_rect)

    if board.lost:
        win_text = title_font.render("YOU LOSE", True, BLACK)
        win_rect = win_text.get_rect(center=(WIDTH//2, (HEIGHT-header)//2 + header))
        screen.blit(win_text, win_rect)

    pygame.display.update()
