import pygame, sys, random

class base:

    def __init__(self):
        self.base_src = pygame.transform.scale2x(pygame.image.load('items/base.png').convert())
        self.base_src_x_pos = 0

    def draw(self):
        self.base_src_x_pos -= 1
        screen.blit(self.base_src, (self.base_src_x_pos, 900))
        screen.blit(self.base_src, (self.base_src_x_pos + 576, 900))
        if self.base_src_x_pos <= -576:
            self.base_src_x_pos = 0

class pipe:

    def __init__(self):
        self.pipe_src = pygame.transform.scale2x(pygame.image.load('items/pipe.png').convert_alpha())
        self.pipe_list = []
        self.pipe_start = pygame.USEREVENT
        pygame.time.set_timer(self.pipe_start, 1000)
        self.pipe_high = [400, 600, 800]

    def create_pipe(self):
        random_pipe_pos = random.choice(self.pipe_high)
        pipe_bottom = self.pipe_src.get_rect(midtop=(700, random_pipe_pos))
        pipe_top = self.pipe_src.get_rect(midbottom=(700, random_pipe_pos - 300))
        return pipe_bottom, pipe_top

    def move_pipe(self,x):
        for pipe in x:
            pipe.centerx -= 5
        return x

    def add_pipe(self,x):
        for pipe in x:
            if pipe.bottom >= 1024:
                screen.blit(self.pipe_src, pipe)
            else:
                rotate_pipe = pygame.transform.flip(self.pipe_src, False, True)
                screen.blit(rotate_pipe, pipe)

class pikachu:

    def __init__(self):
        self.gravity = 0.25
        self.pikachu_move = 0
        self.main_game = True
        self.pikachu_src = pygame.transform.scale2x(pygame.image.load('items/pikachu.png').convert_alpha())
        self.pikachu_rect = self.pikachu_src.get_rect(center=(100, 512))

    def pikachu_r(self,pikachu):
        new_pikachu = pygame.transform.rotozoom(pikachu, -self.pikachu_move * 3, 1)
        return new_pikachu
class collision:

    def check_collision(self,x):
        for pipe in x:
            if pikachu1.pikachu_rect.colliderect(pipe):
                death_sound.play()
                return False
        if pikachu1.pikachu_rect.top <= -100 or pikachu1.pikachu_rect.bottom >= 900:
            death_sound.play()
            return False
        return True

class score:

    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.x = True

    def score_display(self,game_state):
        if game_state == 'main_game':
            score_surface = font.render(str(int(self.score)), True, (255, 211, 31))
            score_rect = score_surface.get_rect(center=(288, 100))
            screen.blit(score_surface, score_rect)

        if game_state == 'game_over':
            score_surface = font.render(f'Score: {int(self.score)}', True, (255, 211, 31))
            score_rect = score_surface.get_rect(center=(288, 100))
            screen.blit(score_surface, score_rect)

            high_score_surface = font.render(f'High Score: {int(self.high_score)}', True, (255, 211, 31))
            high_score_rect = high_score_surface.get_rect(center=(288, 850))
            screen.blit(high_score_surface, high_score_rect)

    def pipe_score(self):
        if pipe1.pipe_list:
            for pipe in pipe1.pipe_list:
                if 95 < pipe.centerx < 105 and self.x:
                    self.score += 1
                    score_sound.play()
                    self.x = False
                if pipe.centerx < 0:
                    self.x = True

    def update_score (self,score, high_score):
        if score > high_score:
            high_score = score
        return high_score

pygame.init()
screen = pygame.display.set_mode((576,1024))
clock = pygame.time.Clock()
font = pygame.font.Font('items/Aleo-Bold.otf',50)

bg_src = pygame.transform.scale2x(pygame.image.load('items/bg.png').convert())
game_over_src = pygame.transform.scale2x(pygame.image.load('items/text.png').convert_alpha())
game_over_rect = game_over_src.get_rect(center = (288,512))

flap_sound = pygame.mixer.Sound('items/wing.wav')
death_sound = pygame.mixer.Sound('items/hit.wav')
score_sound = pygame.mixer.Sound('items/point.wav')

base1 = base()
pipe1 = pipe()
collision1 = collision()
score1 = score()
pikachu1 = pikachu()

while True:
    screen.blit(bg_src, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and pikachu1.main_game:
                pikachu1.pikachu_move = 0
                pikachu1.pikachu_move -= 12
                flap_sound.play()
            if event.key == pygame.K_UP and pikachu1.main_game == False:
                pikachu1.main_game = True
                pipe1.pipe_list.clear()
                pikachu1.pikachu_rect.center =(100,512)
                pikachu1.pikachu_move=0
                score1.score = 0
        if event.type == pipe1.pipe_start:
            pipe1.pipe_list.extend(pipe1.create_pipe())

    if pikachu1.main_game:
        pikachu1.pikachu_move += pikachu1.gravity
        pikachu_rotate = pikachu1.pikachu_r(pikachu1.pikachu_src)
        pikachu1.pikachu_rect.centery += pikachu1.pikachu_move
        screen.blit(pikachu_rotate,pikachu1.pikachu_rect)
        pikachu1.main_game = collision1.check_collision(pipe1.pipe_list)

        pipe1.pipe_list = pipe1.move_pipe(pipe1.pipe_list)
        pipe1.add_pipe(pipe1.pipe_list)
        score1.pipe_score()
        score1.score_display('main_game')

    else:
        screen.blit(game_over_src,game_over_rect)
        score1.high_score=score1.update_score(score1.score,score1.high_score)
        score1.score_display('game_over')

    base1.draw()
    pygame.display.update()
    clock.tick(120)