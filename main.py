import random

WIDTH = 800
HEIGHT = 600

floor_height_scenario1= 130 #Altura do chão do cenário 1 - garante o personagem no solo

#Menu inicial
game_state= "menu"


#Imagens dos cenários
scenario1_background_parts= ["image1_background_scenario_introduction", "image2_background_scenario_introduction", "image3_background_scenario_introduction", "image4_background_scenario_introduction", "image5_background_scenario_introduction", "image6_background_scenario_introduction", "image7_background_scenario_introduction", "background_scenario1_part1", "background_scenario1_part2", "background_scenario1_part3", "background_scenario1_final_items"]
current_scenario1_index= 0
dialogues_scenario1_interactive= ["dialog_next_phase"]
dialogue_on_screen= None

#Definindo imagem padrão dos personagens
#Personagem Principal
hero= Actor("hero_stopped_right")
hero.x= 100
hero.y= HEIGHT - floor_height_scenario1
hero_velocit_y= 0
hero_jump_force= -11
hero_gravity= 0.5
hero_direction= "right" #Lado da posição inicial do personagem
hero_health= 100 #Vida do personagem principal
hero_invulnerable= False
hero_alive= True
hero_attack_cooldown= False
hero_attack_damage= 20
hero_attacking= False
hero_attack_range= 50
#Inimigos
#Zumbis
zombies_by_scenario= {z: [] for z in range(len(scenario1_background_parts))}
zombie1= Actor("zombie_stopped_left") #Zumbi do 1° cenário
zombie1.health= 80
zombie1.x= 500
zombie1.y= HEIGHT - floor_height_scenario1
zombie1.direction= "left"
zombie1.speed= 1.4
zombies_by_scenario[7].append(zombie1)

for zum_scenario2 in range(2): #2 zumbids do 2° cenário
    zombie= Actor("zombie_stopped_left")
    zombie.health= 80
    zombie.speed= 1 
    zombie.x= 300 + zum_scenario2 * 150
    zombie.y= HEIGHT - floor_height_scenario1
    zombie.direction= "left"
    zombies_by_scenario[8].append(zombie)

for zum_scenario3 in range(3):
    zombie= Actor("zombie_stopped_left")
    zombie.health= 80
    zombie.speed= 1
    zombie.x= 200 + zum_scenario3 * 150
    zombie.y= HEIGHT - floor_height_scenario1
    zombie.direction= "left"
    zombies_by_scenario[9].append(zombie)

#Definindo imagens padrão de elementos do cenário
#Nuvens
clouds_images= ["cloud_model1", "cloud_model2", "cloud_model3", "cloud_model4", "cloud_model5"]
clouds= []
for images in clouds_images:
    cloud_select= Actor(images)
    cloud_select.x= random.randint(0, WIDTH)
    cloud_select.y= random.randint(50, 200)
    cloud_select.speed= random.uniform(0.5, 2.5)
    clouds.append(cloud_select)
#Itens
potion_item= Actor("image_potion_hp")
potion_item.x= 400
potion_item.y= HEIGHT - floor_height_scenario1 - 30
potion_acquired= Actor("msg10_obtained_potion")
letter_item= Actor("old_paper_letter")
letter_item.x= 600
letter_item.y= HEIGHT - floor_height_scenario1 - 30
letter_item_acquired= Actor("msg10_letter_item_acquired")

#Imagens dos personagens parados
hero_stopped_left= "hero_stopped_left"
hero_stopped_right= "hero_stopped_right"

#Conjuntos de imagens das movimentações dos personagens
#Pulo
hero_jump_images_left= ["hero_preparing_jump_left", "hero_jump_left"]
hero_jump_images_right= ["hero_preparing_jump_right", "hero_jump_right"]

#Esquerda/Direita
hero_walking_left_images= ["hero_walk_left1", "hero_walk_left2"]
hero_walking_right_images= ["hero_walk_right1", "hero_walk_right2"]

#Sinalizadores de movimentos dos personagens
frame_index= 0
hero_walking= False
hero_jumping= False
event_active= False
event_sleep= False
event_images= []

def update():
    global hero_walking, hero_jumping, hero_direction, current_scenario1_index, hero_velocit_y, hero_attacking, hero_attack_cooldown, event_step, event_active, game_state

    if game_state == "menu":
        if keyboard.K_1:
            game_state = "playing"
        elif keyboard.K_2:
            exit()
        return

    if not hero_alive or current_scenario1_index < 6:
        return #Interrompe todos movimentos do personagem principal

    if event_active: #Enquanto ativo, ignora as tentativas movimentação apenas do personagem
        if event_step >= 3 and keyboard.RETURN:
            event_step= event_step + 1
            if event_step == 4:
                clock.schedule_unique(show_shrug, 2.0)
            elif event_step > 4:
                end_event()
        
        for cloud in clouds:
            cloud.x= cloud.x - cloud.speed
            if cloud.right < 0:
                cloud.left= WIDTH
                cloud.y= random.randint(50, 200)
                cloud.speed= random.uniform(0.5, 2.5)
        return
    
    hero_walking= False

    #Movimentação - esquerda/direita
    move_x= 0
    if keyboard.left:
        move_x= move_x - 5
        hero_walking= True
        hero_direction= "left"
    if keyboard.right:
        move_x= move_x + 5
        hero_walking= True
        hero_direction= "right"
    
    future_x= hero.x + move_x
    if hero_jumping:
        hero.x= future_x
    else:
        collision= False
        current_zombies= zombies_by_scenario[current_scenario1_index]
        for zombie in current_zombies: #Simula o movimento lateral do herói
            original_x= hero.x
            hero.x= future_x
            if strong_collision(hero, zombie):
                collision= True
            hero.x= original_x #Volta ao valor original (não se move de fato ainda)
            if collision:
                break
        if not collision:
            hero.x= future_x

    if hero.x >= WIDTH:
        if current_scenario1_index < len(scenario1_background_parts) - 1:
            if current_scenario1_index + 1 == 10:
                all_zombies_dead= all(len(zombies) == 0 for idx, zombies in zombies_by_scenario.items() if idx < 10)
                if not all_zombies_dead:
                    hero.x= WIDTH
                    return
            current_scenario1_index= current_scenario1_index + 1
            hero.x= 0
        else:
            hero.x= WIDTH
    if hero.x < 0:
        if current_scenario1_index > 7:
            current_scenario1_index= current_scenario1_index - 1
            hero.x= WIDTH - 1
        else:
            hero.x= 0
    hero.x= max(0, min(WIDTH, hero.x))

    #Movimentação - pular
    if keyboard.up and not hero_jumping:
        hero_jumping= True
        hero_velocit_y= hero_jump_force
    
    if hero_jumping:
        if hero_direction == "left":
            hero.image= hero_jump_images_left[frame_index]
        elif hero_direction == "right":
            hero.image= hero_jump_images_right[frame_index]
    elif hero_attacking:
        if hero_direction == "left":
            hero.image= "hero_attack_punch_left2"
        elif hero_direction == "right":
            hero.image= "hero_attack_punch_right2"
    elif hero_walking:
        if keyboard.left:
            hero.image= hero_walking_left_images[frame_index]
        if keyboard.right:
            hero.image= hero_walking_right_images[frame_index]
    else:
        if hero_direction == "left":
            hero.image= hero_stopped_left
        elif hero_direction == "right":
            hero.image= hero_stopped_right
    
    update_zombies()
    damage_from_zombies()
    
    if hero_jumping:
        hero_velocit_y= hero_velocit_y + hero_gravity
        hero.y= hero.y + hero_velocit_y

        if hero.y >= HEIGHT - floor_height_scenario1:
            hero.y= HEIGHT - floor_height_scenario1
            hero_velocit_y= 0
            hero_jumping= False
    
    #Ataque
    if keyboard.a and not hero_attack_cooldown and not hero_attacking:
        hero_attacking= True
        hero_attack_cooldown= True
        perform_attack()
        clock.schedule_unique(end_attack, 0.2) #Duração da animação de ataque
        clock.schedule_unique(reset_attack_cooldown , 0.5) #Tempo entre ataques

    for cloud in clouds:
        cloud.x= cloud.x - cloud.speed
        if cloud.right < 0:
            cloud.left= WIDTH
            cloud.y= random.randint(50, 200)
            cloud.speed= random.uniform(0.5, 2.5)
    
    if event_active and keybard.RETURN:
        event_step= event_step + 1
        if event_step > 4:
            event_active= False
            hero.image= hero_stopped_right

    if not event_active and current_scenario1_index == 10 and 585 <= hero.x <= 595:
        start_event()

def perform_attack():
    current_zombies= zombies_by_scenario[current_scenario1_index]
    for zombie in current_zombies:
        if abs(zombie.y - hero.y) < 50:
            if hero_direction == "right" and zombie.x > hero.x and zombie.x - hero.x <= hero_attack_range:
                stun_zombie(zombie)
            elif hero_direction == "left" and zombie.x < hero.x and hero.x - zombie.x <= hero_attack_range:
                stun_zombie(zombie)

def update_zombies(): #Atualiza os zumbis do cenário atual - em que o personagem está
    for idx in range(current_scenario1_index + 1):
        current_zombies= zombies_by_scenario[idx]
        for zombie in current_zombies:
            if hero_alive:
                if zombie.x < hero.x:
                    zombie.x= zombie.x + zombie.speed
                    zombie.direction= "right"
                elif zombie.x > hero.x:
                    zombie.x= zombie.x - zombie.speed   
                    zombie.direction= "left"
                
                if zombie.colliderect(hero):
                    if zombie.direction == "right":
                        zombie.x= zombie.x + 1
                    else:
                        zombie.x= zombie.x - 1

def damage_from_zombies():
    global hero_health, hero_invulnerable, hero_alive

    if hero_invulnerable or not hero_alive or hero_jumping :
        return #Permanece invulnerável

    current_zombies= zombies_by_scenario[current_scenario1_index]
    for zombie in current_zombies:
        if hero.colliderect(zombie):
            hero_health= hero_health - 1
            hero_invulnerable= True
            knockback_distance= 25
            if zombie.x < hero.x:
                hero.x= hero.x + knockback_distance
            else:
                hero.x= hero.x - knockback_distance
            original_zombie_speed= zombie.speed
            zombie.speed= 0.7
            clock.schedule_unique(lambda: restore_zombie_speed(zombie, original_zombie_speed), 1.0)
            clock.schedule_unique(remove_invulnerability, 0.5) #Fica invulnerável por 0,5 segundos
            if hero_health <= 0:
                print(f"Você morreu!")
                hero_alive= False
                hero.image= "hero_dead" #Personagem principal morto
                hero.y= HEIGHT - floor_height_scenario1 + 30

def restore_zombie_speed(zombie, speed):
    zombie.speed= speed

def stun_zombie(zombie):
    original_speed= zombie.speed
    zombie.speed= 0
    zombie.health= zombie.health - hero_attack_damage #Dano aplicado no zumbi
    if zombie.health <= 0:
        current_zombies= zombies_by_scenario[current_scenario1_index]
        if zombie in current_zombies:
            current_zombies.remove(zombie)
            return
    clock.schedule_unique(lambda: restore_zombie_speed(zombie, original_speed), 0.5)

def strong_collision(hero, zombie):
    if hero_jumping and hero.y + 50 < zombie.y:
        return False
    return hero.colliderect(zombie)

def end_attack():
    global hero_attacking
    hero_attacking= False

def reset_attack_cooldown():
    global hero_attack_cooldown
    hero_attack_cooldown= False

def remove_invulnerability():
    global hero_invulnerable

    hero_invulnerable= False

def start_event():
    global event_active, event_step
    event_active= True
    event_step= 2
    hero.image= "hero_back"
    clock.schedule_unique(show_letter, 2.0)
    
def show_potion():
    global event_step
    event_step= 2
    clock.schedule_unique(show_letter, 2.0)

def show_letter():
    global event_step
    event_step= 3

def show_dialog():
    global event_step
    event_step= 4
    clock.schedule_unique(show_shrug, 3.0)

def show_shrug():
    global event_step
    event_step= 5
    clock.schedule_unique(end_event, 2.0)

def end_event():
    global event_active, event_step
    event_active= False
    event_step= 0
    hero.image= hero_stopped_right


#Desenha o cenário e quem aparece nele
def draw():
    screen.clear()
    if game_state == "menu":
        screen.blit("menu_main", (0, 0))
        return
    screen.blit(scenario1_background_parts[current_scenario1_index], (0, 0))

    # Se estiver em tela de introdução (0 a 5), só mostra o fundo
    if current_scenario1_index < 6:
        return

    if current_scenario1_index == 6:
        hero.pos= (hero.x, hero.y)
        hero.draw()
        return

    # Elementos do jogo são desenhados a partir da imagem 6 (índice 6 ou 7)
    hero.pos = (hero.x, hero.y)
    hero.draw()

    # Corações (HUD)
    heart_spacing = 50
    max_hearts = 10
    for heart in range(max_hearts):
        heart_image = Actor("heart_full" if hero_health > heart * 10 else "heart_clear")
        heart_image.pos = (10 + heart * heart_spacing, 27)
        heart_image.draw()

    # Nuvens
    for cloud in clouds:
        cloud_screen_x = cloud.x 
        cloud.pos = (cloud_screen_x, cloud.y)
        cloud.draw()

    # Zumbis + vida
    for zombie in zombies_by_scenario[current_scenario1_index]:
        zombie.draw()
        draw_zombie_health_bar(zombie)

    # Itens e caixa de diálogo no cenário 4
    if current_scenario1_index == 4:
        potion_item.draw()
        letter_item.draw()
        screen.draw.textbox("Você encontrou uma poção misteriosa e uma carta rasgada...\n\n\"...o Boss final se esconde na escuridão do abismo...\"\n\nAlgo está prestes a acontecer.", Rect(50, 50, 700, 200), color="white", fontsize=26)

    if current_scenario1_index == 10 and event_active:
        for cloud in clouds:
            cloud.draw()
        hero.pos= (hero.x, hero.y)
        hero.image= "hero_back"
        hero.draw()

        if event_step == 2:
            potion_acquired.pos= (WIDTH // 2, HEIGHT // 2)
            potion_acquired.draw()
        elif event_step == 3:
            letter_item_acquired.pos= (WIDTH // 2, HEIGHT // 2)
            potion_acquired.draw()
        elif event_step == 4:
            screen.draw.textbox("Você encontrou uma poção misteriosa e uma carta rasgada...\n\n\"...o Boss final se esconde na escuridão do abismo...\"\n\nAlgo está prestes a acontecer.", Rect(50, 50, 700, 200), color="white", fontsize=26)
        
    
    if event_active:
        if event_active == 1:
            potion_acquired.draw()
        elif event_active == 2:
            letter_item_acquired.draw()
        elif event_active == 3:
            screen.blit(dialogues_scenario1_interactive[0], (150, 150))

def next_frame():
    global frame_index

    if not hero_alive:
        return #Não troca frame se estiver morto

    if hero_jumping:
        if hero_direction == "left":
            frame_index= (frame_index + 1) % len(hero_jump_images_left)
        elif hero_direction == "right":
            frame_index= (frame_index + 1) % len(hero_jump_images_right)
    elif hero_walking:
        if keyboard.left:
            frame_index= (frame_index + 1) % len(hero_walking_left_images)
        if keyboard.right:
            frame_index= (frame_index + 1) % len(hero_walking_right_images)
    else:
        frame_index= 0 #Parado, não ocorre mudança no frame

def draw_zombie_health_bar(zombie): #Barra de vida dos zumbis
    max_health= 80
    bar_width= 40
    bar_height= 6
    health_percent= max(0, zombie.health / max_health) #Total de vida dos zumbis
    health_bar_width= int(bar_width * health_percent)

    bar_x= zombie.x - bar_width // 2
    bar_y= zombie.y - bar_height // 2 - 20 #Acima da cabeça dos zumbis

    screen.draw.filled_rect(Rect((bar_x, bar_y), (bar_width, bar_height)), (100, 100, 100)) #Fundo cinza da barra de vida
    screen.draw.filled_rect(Rect((bar_x, bar_y), (health_bar_width, bar_height)), (200, 0, 0)) #Barra vermelha de vida
    screen.draw.rect(Rect((bar_x, bar_y), (bar_width, bar_height)), (0, 0, 0)) #Borda da barra de vida

def on_key_down(key):
    global current_scenario1_index
    if key == keys.RETURN and current_scenario1_index < 6:
        current_scenario1_index= current_scenario1_index + 1

clock.schedule_interval(next_frame, 0.3)
