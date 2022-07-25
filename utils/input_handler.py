import pygame


def handle_events(game, event):
    if event.type == pygame.QUIT:
        game.playing = False
        game.running = False
    if event.type == pygame.VIDEORESIZE:
        game.SCREEN_W, game.SCREEN_H = event.w, event.h
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            game.playing = False
            game.running = False
        if event.key == pygame.K_a:
            game.actions['left'] = True
        if event.key == pygame.K_d:
            game.actions['right'] = True
        if event.key == pygame.K_w:
            game.actions['up'] = True
        if event.key == pygame.K_s:
            game.actions['down'] = True
        if event.key == pygame.K_SPACE:
            game.actions['action1'] = True
        if event.key == pygame.K_f:
            game.actions['action2'] = True
        if event.key == pygame.K_RETURN:
            game.actions['start'] = True

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_a:
            game.actions['left'] = False
        if event.key == pygame.K_d:
            game.actions['right'] = False
        if event.key == pygame.K_w:
            game.actions['up'] = False
        if event.key == pygame.K_s:
            game.actions['down'] = False
        if event.key == pygame.K_SPACE:
            game.actions['action1'] = False
        if event.key == pygame.K_f:
            game.actions['action2'] = False
        if event.key == pygame.K_RETURN:
            game.actions['start'] = False

    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            game.actions['left_click'] = True

    if event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            game.actions['left_click'] = False
