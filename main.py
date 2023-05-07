import pygame, sys, random
from pygame import mixer

pygame.init()

#Cửa sổ game
screen = pygame.display.set_mode((346, 614))

#Tiêu đề game
pygame.display.set_caption('Flappy Bird')

#FPS game
clock = pygame.time.Clock()

#Các âm thanh game
mixer.init()
wing = pygame.mixer.Sound("flappy-bird-assets-master/audio/wing.wav" )
point = pygame.mixer.Sound("flappy-bird-assets-master/audio/point.wav")
die = pygame.mixer.Sound("flappy-bird-assets-master/audio/die.wav")
hit = pygame.mixer.Sound("flappy-bird-assets-master/audio/hit.wav")
move_pointer = pygame.mixer.Sound("flappy-bird-assets-master/audio/coin.wav")

#Các biến của game
game_play = True
choose_skin = False
show_start_screen = True
show_choose_skin_screen = False
is_day = True
time_counter = 0
start_time = pygame.time.get_ticks() 
#trọng lực
p = 0.15
#Điểm của game
score = 0   #Khởi tạo điểm của game
high_score = 0  #Khởi tạo điểm cao nhất
game_font = pygame.font.Font(r'flappy-bird-assets-master\04B_19__.TTF', 40)

#Icon game
icon = pygame.image.load(r"flappy-bird-assets-master\favicon.ico").convert()
pygame.display.set_icon(icon)

#Background game
background = pygame.image.load(r"flappy-bird-assets-master\sprites\background-day.png").convert()
#Chỉnh background size lớn hơn
background = pygame.transform.scale(background, (346, 614))
 
#Floor game
floor = pygame.image.load(r"flappy-bird-assets-master\sprites\base.png").convert()
#Chỉnh floor size lớn hơn
floor = pygame.transform.scale(floor, (346, 134))
floor_x = 0 #Biến x của floor
#Hàm vẽ floor
def draw_floor():
    global floor_x
    floor_x -= 1    #Biến x của floor giảm dần -> chạy sang trái
    screen.blit(floor, (floor_x, 614 - 134))
    screen.blit(floor, (floor_x + 346, 614 - 134))  #Thêm 1 floor nối tiếp cái ban đầu
    if floor_x == -346:     #Nếu floor đầu chạy hết (x của floor đầu ban đầu bằng 0) thì reset floor_x
        floor_x = 0

#Chim của game
bird_mid = pygame.image.load(r"flappy-bird-assets-master\sprites\bluebird-midflap.png").convert_alpha()
bird_up = pygame.image.load(r"flappy-bird-assets-master\sprites\bluebird-upflap.png").convert_alpha()
bird_down = pygame.image.load(r"flappy-bird-assets-master\sprites\bluebird-downflap.png").convert_alpha()

bird_mid = pygame.transform.scale_by(bird_mid, 1.2)
bird_up = pygame.transform.scale_by(bird_up, 1.2)
bird_down = pygame.transform.scale_by(bird_down, 1.2)
bird_list = [bird_down, bird_mid, bird_down]
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center = (50, (614 - 134)/2))
bird_y = 0  #Biến y của chim
#Xoay chim
def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, bird_y * 3, 1)
    return new_bird
#Taọ timer cho chim
bird_flap = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap, 200)
#Hàm tạo animation đập cánh
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (50, bird_rect.centery))
    return new_bird, new_bird_rect
#Khởi tạo các đối tượng màn hình chọn skin:
red_bird = pygame.image.load(r"flappy-bird-assets-master\sprites\redbird-midflap.png").convert_alpha()
red_bird = pygame.transform.scale_by(red_bird, 1.2)
redbird_rect = red_bird.get_rect(center = (screen.get_rect().centerx, screen.get_rect().centery))

blue_bird = pygame.image.load(r"flappy-bird-assets-master\sprites\bluebird-midflap.png").convert_alpha()
blue_bird = pygame.transform.scale_by(blue_bird, 1.2)
bluebird_rect = blue_bird.get_rect(center = (redbird_rect.centerx - 100, screen.get_rect().centery))

yellow_bird = pygame.image.load(r"flappy-bird-assets-master\sprites\yellowbird-midflap.png").convert_alpha()
yellow_bird = pygame.transform.scale_by(yellow_bird, 1.2)
yellowbird_rect = yellow_bird.get_rect(center = (redbird_rect.centerx + 100, screen.get_rect().centery))

pointer = pygame.image.load(r"flappy-bird-assets-master\sprites\pointer.png").convert_alpha()
pointer = pygame.transform.scale(pointer, (40,40))
pointer_rect = pointer.get_rect(center = (screen.get_rect().centerx + 5, screen.get_rect().centery + 40))

def draw_choose_skin_screen():
    screen.blit(red_bird, redbird_rect)
    screen.blit(blue_bird, bluebird_rect)
    screen.blit(yellow_bird, yellowbird_rect)
    screen.blit(pointer, pointer_rect)
    text_surface = game_font.render('Choose skin', True, (255, 255, 255))
    text_rect = text_surface.get_rect(center = ((screen.get_rect().centerx), 200))
    screen.blit(text_surface, text_rect)

#Tạo ống
pipe_surface = pygame.image.load(r"flappy-bird-assets-master\sprites\pipe-green.png")
pipe_surface = pygame.transform.scale_by(pipe_surface, 1.2)
pipe_list = []
pipe_height = [200, 250, 300, 350, 400]
#Hàm tạo ống
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos - 550))
    return bottom_pipe, top_pipe
#Hàm di chuyển ống
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    return pipes
#Hàm vẽ ống
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 614 - 134:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


#Tạo timer
spawn_pipe = pygame.USEREVENT
pygame.time.set_timer(spawn_pipe, 1000)

#Màn hình kết thúc game
screen_over = pygame.image.load(r'flappy-bird-assets-master\sprites\gameover.png')
screen_over = pygame.transform.scale_by(screen_over, 1.2)
screen_over_rect = screen_over.get_rect(center = (screen.get_rect().center))

#Màn hình bắt đầu game
screen_start = pygame.image.load(r'flappy-bird-assets-master\sprites\message.png')
screen_start = pygame.transform.scale_by(screen_start, 1.2)
screen_start_rect = screen_start.get_rect(center = (screen.get_rect().center))




#Hàm hiện điểm
def score_view(game_state):
    if game_state:
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = ((screen.get_rect().centerx), 100))
        screen.blit(score_surface, score_rect)
    else:
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = ((screen.get_rect().centerx), 100))
        screen.blit(score_surface, score_rect)
        #Điểm cao nhất
        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center = ((screen.get_rect().centerx), 200 ))
        screen.blit(high_score_surface, high_score_rect)
#Đọc điểm cao nhất từ file text
def read_high_score(file_name):
    f = open(file_name, 'r')
    global high_score
    high_score = float(f.read())
    f.close()
#Ghi điểm từ file text 
def write_high_score(file_name):
    f = open(file_name, 'w')
    global high_score
    f.write(str(high_score))
    f.close()
#Hàm xử lý va chạm
def check_collision(pipes):
    if (bird_rect.bottom >= 614 - 134) or (bird_rect.top <= 0):
        pygame.mixer.Sound.play(hit)
        return False
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            pygame.mixer.Sound.play(hit)
            return False
    return True
        
#Vòng lặp xử lí game
while True:
    read_high_score('high_score.txt')
    
    for event in pygame.event.get():    #Event thoát game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and show_start_screen:
                screen_start_rect.centerx = 1000
                screen_start_rect.centery = 1000
                show_start_screen = False
            
            if event.key == pygame.K_SPACE and game_play and choose_skin:
                bird_y = -5
                pygame.mixer.Sound.play(wing)
            if event.key == pygame.K_SPACE and game_play == False:  #Cho phép chơi lại
                game_play = True
                pipe_list.clear()
                bird_y = 0
                bird_rect.center = (50, (614 - 134)/2)
                score = 0 
            
            if event.key == pygame.K_RIGHT and choose_skin == False and show_start_screen == False and show_choose_skin_screen:
                pygame.mixer.Sound.play(move_pointer)
                if pointer_rect.centerx != yellowbird_rect.centerx + 5:
                    if pointer_rect.centerx == redbird_rect.centerx + 5:
                        pointer_rect.centerx = yellowbird_rect.centerx + 5
                    else: pointer_rect.centerx = redbird_rect.centerx + 5
                    
            if event.key == pygame.K_LEFT and choose_skin == False and show_start_screen == False and show_choose_skin_screen:   
                pygame.mixer.Sound.play(move_pointer)
                if pointer_rect.centerx != bluebird_rect.centerx + 5:
                    if pointer_rect.centerx == redbird_rect.centerx + 5:
                        pointer_rect.centerx = bluebird_rect.centerx + 5
                    else: pointer_rect.centerx = redbird_rect.centerx + 5
            
            if event.key == pygame.K_SPACE and show_choose_skin_screen:
                if pointer_rect.centerx == bluebird_rect.centerx + 5:
                    bird_mid = pygame.image.load(r"flappy-bird-assets-master\sprites\bluebird-midflap.png").convert_alpha()
                    bird_up = pygame.image.load(r"flappy-bird-assets-master\sprites\bluebird-upflap.png").convert_alpha()
                    bird_down = pygame.image.load(r"flappy-bird-assets-master\sprites\bluebird-downflap.png").convert_alpha()
                   
                    choose_skin = True
                    show_choose_skin_screen = False
                if pointer_rect.centerx == redbird_rect.centerx + 5:
                    bird_mid = pygame.image.load(r"flappy-bird-assets-master\sprites\redbird-midflap.png").convert_alpha()
                    bird_up = pygame.image.load(r"flappy-bird-assets-master\sprites\redbird-upflap.png").convert_alpha()
                    bird_down = pygame.image.load(r"flappy-bird-assets-master\sprites\redbird-downflap.png").convert_alpha()
                   
                    choose_skin = True
                    show_choose_skin_screen = False
                if pointer_rect.centerx == yellowbird_rect.centerx + 5:
                    bird_mid = pygame.image.load(r"flappy-bird-assets-master\sprites\yellowbird-midflap.png").convert_alpha()
                    bird_up = pygame.image.load(r"flappy-bird-assets-master\sprites\yellowbird-upflap.png").convert_alpha()
                    bird_down = pygame.image.load(r"flappy-bird-assets-master\sprites\yellowbird-downflap.png").convert_alpha()
                    
                    choose_skin = True
                    show_choose_skin_screen = False
                
                
        if event.type == spawn_pipe and choose_skin and game_play:    #Cho ống xuất hiện
            pipe_list.extend(create_pipe())
            
        if event.type == bird_flap and game_play:   #Chim đập cánh
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()
     # Cập nhật thời gian
    time_counter += pygame.time.get_ticks() - start_time
    start_time = pygame.time.get_ticks()

    # Thay đổi background nếu đã đủ thời gian
    if time_counter >= 20000:
        if is_day:
            background = pygame.image.load(r"flappy-bird-assets-master\sprites\background-night.png").convert()
        else:
            background = pygame.image.load(r"flappy-bird-assets-master\sprites\background-day.png").convert()
        background = pygame.transform.scale(background, (346, 614))
        is_day = False
        time_counter = 0

    #Thêm background vào game
    screen.blit(background, (0, 0))

    #Thêm sàn    
    draw_floor()

    screen.blit(screen_start, screen_start_rect)
    
    if choose_skin == False and show_start_screen == False:
        draw_choose_skin_screen()
        show_choose_skin_screen = True

    if game_play and show_start_screen == False and choose_skin:
        
        #Thêm chim vào game:
        rotated_bird = rotate_bird(bird)
        screen.blit(rotated_bird, bird_rect)
        bird_y += p #y của chim tăng theo p -> bị rớt xuống
        bird_rect.centery += bird_y
        
        #Ống
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)\
        #sàn
        draw_floor()
        #Xử lý ghi điểm
        bird_mid_pos = bird_rect.x + bird_rect.width / 2
        for pipe in pipe_list:
            pipe_mid_pos = pipe.x + pipe.width / 2
            if pipe_mid_pos <=  bird_mid_pos <=  pipe_mid_pos:
                score += 0.5
                pygame.mixer.Sound.play(point)
        #Cập nhật điểm cao nhất
        if score > high_score:
            high_score = score
            write_high_score('high_score.txt')
        #Thêm score vào màn hình
        score_view(game_play)
        
        #Va chạm
        game_play = check_collision(pipe_list)

    elif game_play == False and show_start_screen == False and choose_skin: 
        screen.blit(screen_over, screen_over_rect)
        score_view(game_play)
        screen_start_rect.centerx = 1000
        screen_start_rect.centery = 1000
    
    pygame.display.update()
    
    #clock 120
    clock.tick(120)
            
