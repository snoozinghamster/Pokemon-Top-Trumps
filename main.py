# import required modules
import pygame
import random
import requests
from io import BytesIO
from pygame.locals import (
    # K_UP,
    # K_DOWN,
    # K_LEFT,
    # K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    RLEACCEL,
)

# Define constants for the screen width and height, button positions, fonts etc
SCREEN_WIDTH = 1020
SCREEN_HEIGHT = 720
pygame.init()
pygame.font.init()
title_font = pygame.font.SysFont('Comic Sans MS', 40)
stats_font = pygame.font.SysFont('Comic Sans MS', 20)
screen = pygame.display.set_mode((720, 720))
clock = pygame.time.Clock()
running = True
buttons = {"height": (SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 + 100, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 149),
           "weight": (SCREEN_WIDTH / 2 + 40, SCREEN_HEIGHT / 2 + 100, SCREEN_WIDTH / 2 + 150, SCREEN_HEIGHT / 2 + 149),
           "defence": (SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 + 150, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 199),
           "attack": (SCREEN_WIDTH / 2 + 40, SCREEN_HEIGHT / 2 + 150, SCREEN_WIDTH / 2 + 150, SCREEN_HEIGHT / 2 + 199),
           "hp": (SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 + 200, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 249)}


class NewGame:
    def __init__(self):
        print ("Starting a new game with 5 cards each")
        self.player_card_count = 5
        self.opponent_card_count = 5
        self.player_list,self.opponent_list = card_list(self.player_card_count)
        self.player_turn = True #determine whether it is the players turn or the pc - start with player by default

    def compareStats(self,player,pc):
        #take the player value and compare with the pc value. grant the winner the losers card, add to the end of their list. in a draw put but players card to the end
        if int(player) > int(pc):
            print("Player Won")
            # take card 0 from opponent, put on end of list, put player card 0 on end of list
            self.player_card_count = self.player_card_count + 1
            self.player_list.append(self.opponent_list[0])
            self.player_list.append(self.player_list[0])
            self.player_list = self.player_list[1:]
            self.opponent_card_count = self.opponent_card_count - 1
            self.opponent_list = self.opponent_list[1:]
            self.player_turn = True
        elif int(player) == int(pc):
            print("Draw")
            # take first card put to back (not correct handling of a draw, should be go to middle and next winner gains both
            self.player_list.append(self.player_list[0])
            self.player_list = self.player_list[1:]
            self.opponent_list.append(self.opponent_list[0])
            self.opponent_list = self.opponent_list[1:]
        else:
            print("Player Lost")
            self.opponent_card_count = self.opponent_card_count + 1
            self.opponent_list.append(self.player_list[0])
            self.opponent_list.append(self.opponent_list[0])
            self.opponent_list = self.opponent_list[1:]
            self.player_card_count = self.player_card_count - 1
            self.player_list = self.player_list[1:]
            self.player_turn = False #passes the turn to the pc
            #self.player_turn = True #this line needs to be deleted to let the pc play once that is coded

class Pokemon:
    def __init__(self, card_id):
        #initialise a pokemon based on the id. would be nice to add shiny mechanics
        print(card_id)
        self.id = card_id
        url = 'https://pokeapi.co/api/v2/pokemon/{}/'.format(self.id)
        response = requests.get(url)
        pokemon = response.json()
        self.name = pokemon['name']
        self.height = pokemon['height']
        self.weight = pokemon['weight']
        self.base_image_url = pokemon['sprites']['front_default']
        self.base_hp = pokemon['stats'][0]['base_stat']
        self.base_attack = pokemon['stats'][1]['base_stat']
        self.base_defence = pokemon['stats'][2]['base_stat']
        self.stat_summary = {"height":pokemon['height'],"weight":pokemon['weight'],"hp":pokemon['stats'][0]['base_stat'],"attack":pokemon['stats'][1]['base_stat'],"defence":pokemon['stats'][2]['base_stat']}
        #create the card image
        img_response = requests.get(self.base_image_url)
        self.surf = pygame.image.load(BytesIO(img_response.content)).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.surf = pygame.transform.scale(self.surf, (400, 400))

def card_list(number_of_cards):
    #generates list of cards. prevents dulicate cards, and splits into player and pc cards
    id_list = []
    while True:
        if len(id_list) == number_of_cards * 2:
            break
        else:
            id = random.randint(1, 151)
            if id in id_list:
                continue
            else:
                id_list.append(id)
    player_list = id_list[:number_of_cards]
    pc_list = id_list[number_of_cards:]
    print("Player and Opponent Card Lists Generated: \n Player List: {} \n PC List: {}".format(player_list,pc_list))

    return player_list, pc_list

game = NewGame()
game_over = False
player_pokemon = Pokemon(game.player_list[0])
opponent_pokemon = Pokemon(game.opponent_list[0])
result_text_1 = ""
result_text_2 = ""
turn_taken = ""
while running: #game
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        stat_selected = "None"
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False
        #check for mouse clicks on the various buttons

        elif event.type == pygame.MOUSEBUTTONDOWN and game.player_turn is True:  # if mouse clicked
            if mouse[0] >= buttons["height"][0] and mouse[0] <= buttons["height"][2]:
                if mouse[1] >= buttons["height"][1] and mouse[1] <= buttons["height"][3]:
                    stat_selected = "height"
                elif mouse[1] >= buttons["defence"][1] and mouse[1] <= buttons["defence"][3]:
                    stat_selected = "defence"
                elif mouse[1] >= buttons["hp"][1] and mouse[1] <= buttons["hp"][3]:
                    stat_selected = "hp"
            elif mouse[0] >= buttons["weight"][0] and mouse[0] <= buttons["weight"][2]:
                if mouse[1] >= buttons["weight"][1] and mouse[1] <= buttons["weight"][3]:
                    stat_selected = "weight"
                elif mouse[1] >= buttons["attack"][1] and mouse[1] <= buttons["attack"][3]:
                    stat_selected = "attack"
            turn_taken = "Player"
        elif event.type == pygame.MOUSEBUTTONDOWN and game.player_turn is False:
            stat_options = ["height", "weight", "hp", "attack", "defence"]
            stat_selected = random.choice(stat_options)
            turn_taken = "Opponent"
        #need dict to assign stats
        if stat_selected != "None":
            #get stats from dict
            player_result = player_pokemon.stat_summary[stat_selected]
            opponent_result = opponent_pokemon.stat_summary[stat_selected]
            print ("player result: ",str(player_result), "opponent result: ", str(opponent_result))
            game.compareStats(player_result,opponent_result)
            print(game.player_list)
            print(game.opponent_list)
            if len(game.player_list) == 0:
                game_over = True
                result = "Loser..."
            elif len(game.opponent_list) == 0:
                game_over = True
                result = "WINNER!"
            else:
                player_pokemon = Pokemon(game.player_list[0])
                opponent_pokemon = Pokemon(game.opponent_list[0])
                print (player_pokemon.name)

    screen.fill("pink")

    # track mouse
    mouse = pygame.mouse.get_pos()

    if game_over is False:
        if game.player_turn is True:
            if mouse[0] >= buttons["height"][0] and mouse[0] <= buttons["height"][2]:
                if mouse[1] >= buttons["height"][1] and mouse[1] <= buttons["height"][3]:
                    pygame.draw.rect(screen, "blue", (buttons["height"][0], buttons["height"][1],
                                                      buttons["height"][2] - buttons["height"][0],
                                                      buttons["height"][3] - buttons["height"][1]))
                elif mouse[1] >= buttons["defence"][1] and mouse[1] <= buttons["defence"][3]:
                    pygame.draw.rect(screen, "blue", (
                    buttons["defence"][0], buttons["defence"][1], buttons["defence"][2] - buttons["defence"][0],
                    buttons["defence"][3] - buttons["defence"][1]))
                elif mouse[1] >= buttons["hp"][1] and mouse[1] <= buttons["hp"][3]:
                    pygame.draw.rect(screen, "blue", (
                    buttons["hp"][0], buttons["hp"][1], buttons["hp"][2] - buttons["hp"][0],
                    buttons["hp"][3] - buttons["hp"][1]))
            elif mouse[0] >= buttons["weight"][0] and mouse[0] <= buttons["weight"][2]:
                if mouse[1] >= buttons["weight"][1] and mouse[1] <= buttons["weight"][3]:
                    pygame.draw.rect(screen, "blue", (
                    buttons["weight"][0], buttons["weight"][1], buttons["weight"][2] - buttons["weight"][0],
                    buttons["weight"][3] - buttons["weight"][1]))
                elif mouse[1] >= buttons["attack"][1] and mouse[1] <= buttons["attack"][3]:
                    pygame.draw.rect(screen, "blue", (
                    buttons["attack"][0], buttons["attack"][1], buttons["attack"][2] - buttons["attack"][0],
                    buttons["attack"][3] - buttons["attack"][1]))

        #show card count
        player_cards_remaining = game.player_card_count
        opponent_cards_remaining = game.opponent_card_count
        player_card_text = stats_font.render("Cards: {}".format(player_cards_remaining),False,(0,0,0))
        player_card_text_rect = player_card_text.get_rect(center=((SCREEN_WIDTH / 4 - 100),75))
        screen.blit(player_card_text,player_card_text_rect)
        opponent_card_text = stats_font.render("Opponent Cards: {}".format(opponent_cards_remaining), False, (0, 0, 0))
        opponent_card_text_rect = opponent_card_text.get_rect(center=((SCREEN_WIDTH / 4 - 100), 125))
        screen.blit(opponent_card_text,opponent_card_text_rect)

        # produce card
        # pygame.draw.rect(screen, 'blue', (SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 5 + 0, 400 , 400 ) )
        pygame.draw.rect(screen, 'grey', (SCREEN_WIDTH / 2 - 200, 30, 400, 600), width=20, border_radius=20)
        screen.blit(player_pokemon.surf, ((SCREEN_WIDTH / 2 - 200), (SCREEN_HEIGHT / 2 - 200 - 100)))

        name_text = title_font.render(player_pokemon.name.title(), False, (0, 0, 0))
        name_rect = name_text.get_rect(center=(SCREEN_WIDTH / 2, 75))
        screen.blit(name_text, name_rect)

        # height
        height_text = stats_font.render("Height: " + str(player_pokemon.height), False, (0, 0, 0))
        screen.blit(height_text, (SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 + 100))

        # weight
        weight_text = stats_font.render("Weight: " + str(player_pokemon.weight), False, (0, 0, 0))
        screen.blit(weight_text, (SCREEN_WIDTH / 2 + 40, SCREEN_HEIGHT / 2 + 100))

        # defence
        defence_text = stats_font.render("Defence: " + str(player_pokemon.base_defence), False, (0, 0, 0))
        screen.blit(defence_text, (SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 + 150))

        # attack
        attack_text = stats_font.render("Attack: " + str(player_pokemon.base_attack), False, (0, 0, 0))
        screen.blit(attack_text, (SCREEN_WIDTH / 2 + 40, SCREEN_HEIGHT / 2 + 150))

        # hp
        hp_text = stats_font.render("HP: " + str(player_pokemon.base_hp), False, (0, 0, 0))
        screen.blit(hp_text, (SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 + 200))

        #opponent card
        #add display of opponent card. need button to progress onto next card.

        if turn_taken == "Player" and stat_selected != "None":
            print("round complete")
            result_text_1 = "You Chose: " + str(stat_selected) +" : " + str(player_result)
            result_text_2 =  "Enemy Score: " + str(opponent_result)
        elif turn_taken == "Opponent" and stat_selected != "None":
            print("round complete")
            result_text_1 = "Your Score: " + str(player_result)
            result_text_2 = "Enemy Chose: " + str(stat_selected) + " : " + str(opponent_result)
        if game.player_turn is True:
            result_text_3 = "Click to select a stat"
        elif game.player_turn is False:
            result_text_3 = "Lost! Opponents turn to select, click anywhere"
        result_text_1_display = stats_font.render(result_text_1, False, (0, 0, 0))
        screen.blit(result_text_1_display, (SCREEN_WIDTH / 2 - 450, SCREEN_HEIGHT / 2 + 150))
        result_text_2_display = stats_font.render(result_text_2, False, (0, 0, 0))
        screen.blit(result_text_2_display, (SCREEN_WIDTH / 2 - 450, SCREEN_HEIGHT / 2 + 200))
        result_text_3_display = stats_font.render(result_text_3, False, (0, 0, 0))
        screen.blit(result_text_3_display, (SCREEN_WIDTH / 2 - 450, SCREEN_HEIGHT / 2 + 250))

        """
        winner/loser
        
        if playter choice
        you chose: stat score
        Enemy score: score
        
        if enemy choice
        your score: score
        enemy chose: stat : scpre
        
        your turn / enemy turn (click to play)
        """

    else:
        result_text = title_font.render(result, False, (0, 0, 0))
        result_rect = result_text.get_rect(center=(SCREEN_WIDTH / 2, 75))
        screen.blit(result_text, result_rect)
    # refresh display
    pygame.display.flip()
    clock.tick(30)  # limits FPS to 30
pygame.quit()
