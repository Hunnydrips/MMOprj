import sys
import time
import random
import pygame

from Classes import player, mob, item, dropped_item

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
P_rect = pygame.Rect((0, 0), (66, 92))
M_rect = pygame.Rect((0, 0), (88, 120))
items_on_surface = []
font = pygame.font.Font("freesansbold.ttf", 20)
font_gold = pygame.font.Font("freesansbold.ttf", 100)

gold_coin = pygame.image.load('../Assets/coins/gold.png')
silver_coin = pygame.image.load('../Assets/coins/silver.png')
bronze_coin = pygame.image.load('../Assets/coins/bronze.png')

gold_coin = pygame.transform.scale(gold_coin, (70, 70))
silver_coin = pygame.transform.scale(silver_coin, (70, 70))
bronze_coin = pygame.transform.scale(bronze_coin, (70, 70))

chat_box = pygame.image.load('../Assets/basics/chatBox.png')

chat_box = pygame.transform.scale(chat_box, (540, 30))

icon_bow = pygame.image.load('../Assets/icons/icon-bow.png')
icon_dagger = pygame.image.load('../Assets/icons/icon-dagger.png')
icon_snowball = pygame.image.load('../Assets/icons/icon-cumball.png')

icon_bow = pygame.transform.scale(icon_bow, (70, 70))
icon_dagger = pygame.transform.scale(icon_dagger, (70, 70))
icon_snowball = pygame.transform.scale(icon_snowball, (70, 70))

mob_image = pygame.image.load('../Assets/basics/mob.png')
zombie_image = pygame.image.load('../Assets/basics/zombie.png')


def time_to_string(t):
    return f'{int(t // 3600)}:{int(t // 60)}:{int(t // 1)}'


def identify_par_dmg(Ps: list, Ms: list):
    """
    :param Ps: A list of all the players that exist in the game
    :param Ms: A list of the mobs
    :return: new health for each entity
    """
    for M in Ms:
        for S in M.spears:
            for P in Ps:
                P_rect.center = P.x, P.y
                if P_rect.colliderect(S.hit_box) and not S.hit:
                    M.spears.remove(S)
                    S.hit = True
                    P.health -= int(10 * P.income_dmg_multiplier)
                    if P.health <= 0:
                        Ps.remove(P)
    for P1 in Ps:
        for par in P1.projectiles:
            for M in Ms:
                if M.is_alive:
                    M_rect.center = M.x, M.y
                    if M_rect.colliderect(par.hit_box) and not par.hit:
                        par.hit = True
                        if par.speed != 1:
                            P1.projectiles.remove(par)
                        M.health -= par.dmg
                        if M.health <= 0:
                            P1.gold += M.worth
                            M.death_time = time.time()
                            M.is_alive = False
                            items_on_surface.append(generate_drop(M.x, M.y, M.lvl))
            for P2 in Ps:
                if P2.nickname != P1.nickname:
                    P2_rect = pygame.Rect((0, 0), (66, 92))
                    P2_rect.center = P2.x, P2.y
                    if P2_rect.colliderect(par.hit_box) and not par.hit:
                        par.hit = True
                        if par.speed != 1:
                            P1.projectiles.remove(par)
                        P2.health -= int(par.dmg * P2.income_dmg_multiplier)
                        if P2.health <= 0:
                            Ps.remove(P2)


def show_mob_health(M: mob.Mob):
    pygame.draw.rect(screen, (0, 255, 0), ((M.x - 50, M.y - 75), (M.health // M.lvl, 10)))
    pygame.draw.rect(screen, (255, 0, 0), ((M.x - 50 + M.health // M.lvl, M.y - 75), (100 - M.health // M.lvl, 10)))


def show_player_health(P: player.Player):
    pygame.draw.rect(screen, (0, 255, 0), ((P.x - 50, P.y - 70), (P.health, 10)))
    pygame.draw.rect(screen, (255, 0, 0), ((P.x - 50 + P.health, P.y - 70), (100 - P.health, 10)))


def show_inventory(P: player.Player):
    slot_rect = pygame.Rect((screen.get_size()[0] - 490, screen.get_size()[1] - 90), (90, 90))
    in_hand_x, in_hand_y = 0, 0
    for i, I in enumerate(P.inventory):
        pygame.draw.rect(screen, (100, 100, 100), slot_rect, 10)
        if i == P.picked:
            in_hand_x = slot_rect.x
            in_hand_y = slot_rect.y
        if I:
            slot_rect.x += 10
            slot_rect.y += 10
            if I.name == 'bow':
                screen.blit(icon_bow, slot_rect)
            elif I.name == 'dagger':
                screen.blit(icon_dagger, slot_rect)
            else:
                screen.blit(icon_snowball, slot_rect)
            screen.blit(font.render(str(I.lvl), True, (255, 255, 255)), slot_rect)
            slot_rect.x -= 10
            slot_rect.y -= 10
        slot_rect.x += 80
    pygame.draw.rect(screen, (255, 255, 255), ((in_hand_x, in_hand_y), (90, 90)), 10)


def show_time(start_time):
    text_rect = font.render(time_to_string(time.time() - start_time), True, (255, 255, 255)).get_rect()
    text_rect.topright = screen.get_size()[0], 0
    screen.blit(font.render(time_to_string(time.time() - start_time), True, (255, 255, 255)), text_rect)


def show_gold(gold: int):
    screen.blit(gold_coin, (35, screen.get_height() - 130))
    screen.blit(silver_coin, (0, screen.get_height() - 70))
    screen.blit(bronze_coin, (70, screen.get_height() - 70))
    to_add = ''
    if gold >= 1000000000:
        gold = int(gold / 100000000)
        gold /= 10.0
        to_add = 'T'
    elif gold >= 1000000:
        gold = int(gold / 100000)
        gold /= 10.0
        to_add = 'M'
    elif gold >= 1000:
        gold = int(gold / 100)
        gold /= 10
        to_add = 'K'
    toShow = font_gold.render(str(gold) + to_add, True, (255, 215, 0))
    screen.blit(toShow, (150, screen.get_height() - 110))


def show_mob_lvl(M: mob.Mob):
    name = font.render(str(M.lvl), True, (0, 0, 0))
    name_rect = name.get_rect()
    name_rect.center = M.x, M.y
    name_rect.y -= 70
    name_rect.x -= 70
    screen.blit(name, name_rect)


def show_name(P: player.Player):
    name = font.render(P.nickname, True, (0, 0, 0))
    name_rect = name.get_rect()
    name_rect.center = P.x, P.y
    name_rect.y -= 90
    screen.blit(name, name_rect)


def generate_drop(x, y, average):
    lvl = abs(random.randint(average - 11, average + 9)) + 1
    name = random.randint(0, 2)
    if name == 0:
        return dropped_item.Dropped_item(x, y, lvl, 'bow', time.time())
    elif name == 1:
        return dropped_item.Dropped_item(x, y, lvl, 'dagger', time.time())
    return dropped_item.Dropped_item(x, y, lvl, "cumball", time.time())


def move(P2: player.Player, P: player.Player):
    keys = pygame.key.get_pressed()
    P.dir_x = keys[pygame.K_d] - keys[pygame.K_a]
    P.dir_y = keys[pygame.K_s] - keys[pygame.K_w]
    P2.dir_x = keys[pygame.K_l] - keys[pygame.K_j]
    P2.dir_y = keys[pygame.K_k] - keys[pygame.K_i]


def move_all_players_and_their_particles(players: list):
    for Pl in players:
        Pl.move()
        Pl.ability()
        P_rect.center = Pl.x, Pl.y
        screen.blit(pygame.transform.flip(P_sprite, Pl.last_dir == -1, False), P_rect)
        show_player_health(Pl)
        show_name(Pl)
        for par in Pl.projectiles:
            if par.range <= 0:
                Pl.projectiles.remove(par)
            par.move(Pl.x, Pl.y)
            screen.blit(par.image, par.hit_box)


def move_all_mobs_and_their_spear(mobs: list, players: list):
    for Mo in mobs:
        if Mo.is_alive:
            Mo.move(players)
            M_rect.center = Mo.x, Mo.y
            if Mo.is_melee:
                screen.blit(pygame.transform.flip(zombie_image, Mo.last_dir, False), M_rect)
            else:
                screen.blit(pygame.transform.flip(mob_image, not Mo.last_dir, False), M_rect)
            show_mob_lvl(Mo)
            show_mob_health(Mo)
        elif time.time() - Mo.death_time >= 7:
            Mo.is_alive = True
            Mo.x, Mo.y = Mo.home_x, Mo.home_y
            Mo.health = 100 * Mo.lvl
        for spear in Mo.spears:
            if spear.range <= 0:
                Mo.spears.remove(spear)
            spear.move(0, 0)
            screen.blit(spear.image, spear.hit_box)


def main():
    start_time = time.time()
    chat_log = []
    frame_counter = 0
    in_chat = False
    chat_enabled = True
    chat_message = ''
    CL = pygame.time.Clock()
    P = player.Player("Hunnydrips", 0, 0)
    P2 = player.Player("Glidaria", 0, 0)
    global P_sprite
    P_sprite = pygame.image.load(f'../Assets/basics/{P.Class}.png')
    M = mob.Mob(50, 50, 5)
    M2 = mob.Mob(500, 50, 3)
    players = [P, P2]
    mobs = [M, M2]
    running = True
    while running:
        screen.fill((0, 0, 255))
        m_x, m_y = pygame.mouse.get_pos()
        frame_counter += 1
        frame_counter %= 60
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and chat_enabled:
                    in_chat = not in_chat
                    if not in_chat:
                        if chat_message:
                            while len(chat_log) >= 5:
                                chat_log = chat_log[1:]
                            chat_log.append(
                                f'({P.nickname}): {chat_message} [{time_to_string(time.time() - start_time)}]')
                            chat_message = ''
                    else:
                        P.dir_x = 0
                        P.dir_y = 0
                elif in_chat:
                    if len(chat_message) < 45 and '~' >= event.unicode >= ' ':
                        chat_message += event.unicode
                elif event.key == pygame.K_TAB:
                    chat_enabled = not chat_enabled
                elif event.key == pygame.K_e:
                    P.use_ability()
                elif event.key == pygame.K_x and P.picked and P.inventory[P.picked]:
                    P.gold += P.inventory[P.picked].upgrade_cost * 0.75
                    P.inventory[P.picked] = False
                    P.picked = 0
                elif event.key == pygame.K_q:
                    for I in items_on_surface:
                        if I.check_pick_up(P):
                            if P.inventory[P.picked]:
                                P.gold += P.inventory[P.picked].upgrade_cost * 0.6
                            P.inventory[P.picked] = item.Item(I.name, I.lvl)
                            items_on_surface.remove(I)
                            break
                elif event.key == pygame.K_u and P.inventory[P.picked].lvl < 999 and P.inventory[P.picked].upgrade_cost <= P.gold:
                    P.gold -= P.inventory[P.picked].upgrade_cost
                    P.inventory[P.picked].upgrade()
                elif pygame.K_1 <= event.key <= pygame.K_6:
                    P.picked = int(event.unicode) - 1
            elif event.type == pygame.MOUSEBUTTONDOWN and not in_chat and event.button == 1 and P.inventory[P.picked]:
                P.attack(m_x, m_y)
        if not in_chat:
            move(P2, P)  # client
        move_all_players_and_their_particles(players)  # server
        move_all_mobs_and_their_spear(mobs, players)  # server
        identify_par_dmg(players, mobs)  # server
        if chat_enabled:
            height_of_msg = 10
            for msg in chat_log:
                screen.blit(font.render(msg, True, (255, 255, 255)), (20, height_of_msg))
                height_of_msg += 30

        if in_chat:
            if keys[pygame.K_BACKSPACE] and keys[pygame.K_LCTRL]:
                chat_message = ''
            if keys[pygame.K_BACKSPACE] and chat_message and not frame_counter % 4:
                chat_message = chat_message[:-1]
            screen.blit(chat_box, (10, 200))
            blinking_shit = ''
            if frame_counter < 30:
                blinking_shit = '|'
            screen.blit(font.render(chat_message + blinking_shit, True, (255, 255, 255)), (13, 205))
        for I in items_on_surface:
            if time.time() - I.time_dropped > 7:
                items_on_surface.remove(I)
            I.show_item_on_surface(screen)
        show_inventory(P)  # client
        show_time(start_time)  # client
        show_gold(P.gold)  # client
        CL.tick(60)
        pygame.display.update()


if __name__ == '__main__':
    main()
