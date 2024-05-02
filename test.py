import random
def other_check_cards(list1,list2):
    combined_list = list1 + list2
    checked_list = []
    duplicate_count = 0
    for i in combined_list:
        if i not in checked_list:
            checked_list.append(i)
        else: duplicate_count += 1

    if duplicate_count > 0:
        replacement_cards = card_list(duplicate_count)
        checked_list = checked_list + replacement_cards
    print(checked_list)
    print(duplicate_count)

def card_list(number_of_cards):
    # generates list of cards. doesnt currently prevent getting same card twice
    id_list = []
    while True:
        if len(id_list) == number_of_cards*2:
            break
        else:
            id = random.randint(1, 151)
            if id in id_list:
                continue
            else:
                id_list.append(id)
    print(id_list)
    player_list = id_list[:number_of_cards]
    pc_list = id_list[number_of_cards:]
    return player_list,pc_list


player_list,pc_list = card_list(5)
print(player_list)
print(pc_list)