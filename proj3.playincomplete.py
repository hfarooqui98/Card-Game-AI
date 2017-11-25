import copy

# Initialising golobal variable for 'A'/Wild card
WILD = 'A'


def phasedout_score(hand):
    ''' Takes as input the remaining cards in a players hand after the end of a
    game and adds up the score and returning that'''

    # Returning score
    score = 0

    # Initializing a dictionary for value and score
    score_dict = {'A': 25, 'K': 13, 'Q': 12, 'J': 11, '0': 10}
    for i in range(2, 10):
        score_dict[str(i)] = i

    # Tallying score
    for mem in hand:
        score += score_dict[mem[0]]

    return score


def check_value_play(hand, value_len):
    '''Helper function designed to check if, given a set of cards in hand and a
    desried length of cards, whether a value phase can be completed and if so
    what the paly hand should be returning a tuple of the phase (empty if not
    complete) and possible phase'''

    # Returning value:
    phase = []

    # creating a dictionary of values to sort hand by
    score_dict = {'A': 25, 'K': 13, 'Q': 12, 'J': 11, '0': 10}
    for i in range(2, 10):
        score_dict[str(i)] = i

    # sorting hand in order of increasing value and creating a copy for itter
    hand = sorted(hand, key=lambda x: score_dict[x[0]])
    hand_copy = copy.copy(hand)

    # setting context in which decisions will be made:
    # checking amount of aces in hand
    wild_count = 0
    wild_cards = []
    for card in hand:
        if card[0] == WILD:
            wild_count += 1
            wild_cards.append(card)

    # checking for possible complete phases in hand
    possible_phase = []
    for card in hand_copy:
        if card[0] != WILD:
            test_value = card[0]
            l = [card]
            for mem in hand_copy[(hand_copy.index(card) + 1):]:
                if mem[0] == test_value:
                    l.append(mem)
                    hand_copy.remove(mem)
                else:
                    break
            if len(l) >= abs(value_len - wild_count):
                possible_phase.append(l)

    # if any possible phases are in hand then putting them down
    if len(possible_phase) >= 2:
        l = []
        count_1 = 0
        count_2 = -1
        for i in range(len(possible_phase) + 1):
            diff = value_len - len(possible_phase[count_2])
            # scenario 1: exactly 3 cards of the same value, no wild needed
            if len(possible_phase[count_2]) == value_len:
                l = possible_phase[count_2]
                possible_phase.pop()
                phase.append(l)
                count_1 += 1
            # scenario 2: more than 3 cards of the same value
            elif len(possible_phase[count_2]) > value_len:
                l = possible_phase[count_2][:value_len]
                possible_phase.pop()
                phase.append(l)
                count_1 += 1
            # scenario 3: less than 3 cards of the same value so wild needed
            elif len(possible_phase[count_2]) < value_len and len(
                    wild_cards) >= diff:
                l = possible_phase[count_2] + (wild_cards[:(diff + 1)])
                del wild_cards[:(diff + 1)]
                phase.append(l)
                count_1 += 1
            count_2 -= 1
            if count_1 == 2:
                break
        return (phase, possible_phase)


def check_suit_play(hand, suit_len):
    '''Helper function designed to check if, given a set of cards in hand and
    a desired length of cards, whether a suit phase can be completed and if so
    what the paly hand should be returning a tuple of the phase (empty if not
    complete) and possible phase'''

    # Returning value:
    phase = []

    # setting context in which decisions will be made:
    # checking amount of aces in hand
    wild_count = 0
    wild_cards = []
    for card in hand:
        if card[0] == WILD:
            wild_count += 1
            wild_cards.append(card)

    # Removing wild cards
    hand_no_wild = []
    for card in hand:
        if card[0] != WILD:
            hand_no_wild.append(card)

    # sorting on basis of suit
    suit_sort = []
    for card in hand_no_wild:
        suit_sort.append(card[::-1])
    suit_sort = sorted(suit_sort)

    # checking to see which suites can be completed with wilds in mind
    possible_phase = []
    count = 1
    for mem in suit_sort:
        test_suit = mem[0]
        l = [mem[::-1]]
        for card in suit_sort[count:]:
            if card[0] == test_suit:
                l.append(card[::-1])
            else:
                break
        if len(l) + wild_count >= suit_len:
            possible_phase.append(l)
        count += 1

    # deciding which phase to complete and retrun if more than one possible
    max_score = 0
    max_phase = []
    for mem in possible_phase:
        if len(mem) < suit_len:
            diff = suit_len - len(mem)
            mem = mem + wild_cards[:(diff + 1)]
        if phasedout_score(mem) > max_score:
            max_score = phasedout_score(mem)
            max_phase = mem
        phase = max_phase
    return (phase, possible_phase)


def check_run_play(hand, run_len):
    '''Helper function designed to check if, given a set of cards in hand and
    a desired length of cards, whether a run phase can be completed and if so
    what the paly hand should be returning a tuple of the phase (empty if not
    complete) and possible phase'''

    # Returning value:
    phase = []

    # list to compare if hand is in run order
    run = '234567890JQKA'
    run_list = run = ['2', '3', '4', '5', '6', '7', '8', '9',
                      '0', 'J', 'Q', 'K', 'A']

    # setting context in which decisions will be made:
    # checking amount of aces in hand
    wild_count = 0
    wild_cards = []
    for card in hand:
        if card[0] == WILD:
            wild_count += 1
            wild_cards.append(card)

    # creating a dictionary of values to sort hand by
    score_dict = {'A': 25, 'K': 13, 'Q': 12, 'J': 11, '0': 10}
    for i in range(2, 10):
        score_dict[str(i)] = i

    # Removing wild cards
    hand_no_wild = []
    for card in hand:
        if card[0] != WILD:
            hand_no_wild.append(card)

    # sorting hand in order of increasing value
    hand_no_wild = sorted(hand_no_wild, key=lambda x: score_dict[x[0]])

    # scenario 1: run is already complete, no wild necessary
    count = 1
    sliced_list = []
    for card in hand_no_wild:
        sliced_list = hand_no_wild[(hand_no_wild.index(card)):(
            run_len + hand_no_wild.index(card))]
        l = []
        for mem in sliced_list:
            l.append(mem[0])
        if ''.join(l) in run:
            phase = sliced_list
            break

    # scenario 2: run needs aces to complete
    possible_phase = []
    for card in hand_no_wild:
        count = 0
        count_2 = 0
        l = []
        location_in_hand = hand_no_wild.index(card)
        start_point = run_list.index(card[0])
        wild_cards_check_count = 0
        for i in range(len(hand_no_wild[location_in_hand:])+1):
            try:
                if hand_no_wild[location_in_hand+count][0] == run_list[
                                                        (start_point+count_2)]:
                    l.append(hand_no_wild[location_in_hand+count])
                    count += 1
                    count_2 += 1
                elif wild_cards_check_count != wild_count:
                    l.append(wild_cards[0])
                    wild_cards_check_count += 1
                    count_2 += 1
                else:
                    break
            except IndexError:
                if hand_no_wild[-1][0] == run_list[(start_point+count_2)]:
                    l.append(hand_no_wild[location_in_hand+count])
                    count += 1
                    count_2 += 1
                elif wild_cards_check_count != wild_count:
                    l.append(wild_cards[0])
                    wild_cards_check_count += 1
                    count_2 += 1
                else:
                    break
        if len(l) == run_len:
            possible_phase.append(l)

    # checking which phase out of the ones possible to return
    max_score = 0
    max_phase = []
    for mem in possible_phase:
        if phasedout_score(mem) > max_score:
            max_score = phasedout_score(mem)
            max_phase = mem
        phase = max_phase
    return (phase, possible_phase)

def check_colour_run_play(hand, run_len):
    '''Helper function designed to check if, given a set of cards in hand and
    a desired length of cards, whether a run phase can be completed with cards
    of the same suit colour and if so what the paly hand should be returning
    a tuple of the phase (empty if not complete) and possible phase'''

    # Returning value:
    phase = []

    #creating list with no wilds to split by colour
    hand_no_wild = []
    wilds = []
    for card in hand:
        if card[0] != WILD:
            hand_no_wild.append(card)
        else:
            wilds.append(card)

    #spliting hand by colour
    red = ('D', 'H')
    black = ('S', 'C')
    red_hand = []
    black_hand = []
    for card in hand:
        if card[1] in red:
            red_hand.append(card)
        if card[1] in black:
            black_hand.append(card)
    # Adding wilds back in to both list to see if either complete run
    red_hand = red_hand + wilds
    black_hand = black_hand + wilds
    # checking which colour can complete hand
    possible_phase = []
    if len(check_run_play(red_hand, 1)[0]) != 0:
        possible_phase.append(red_hand)
    elif len(check_run_play(black_hand, 1)[0]) != 0:
        possible_phase.append(black_hand)

    # checking which colour is of derisred run_len and should be returned
    max_score = 0
    for mem in possible_phase:
        if len(mem) == run_len and phasedout_score(mem) > max_score:
            max_score = phasedout_score(mem)
    for mem in possible_phase:
        if phasedout_score(mem) == max_score and len(mem) == run_len:
            phase = mem
            break
    return (phase, possible_phase)

def phasedout_play(player_id, table, turn_history, phase_status, hand,
                   discard):
    ''' Looks at the game coinditions and returns best possible play in form
    of a tuple (play type, play_hand)'''

    # varialbe that will be assigned a value in code and then returned
    play_hand = []
    play_type = 0

    # Checking if phase complete and if not, assigning objective phase
    obj_phase = phase_status[player_id] + 1
    phase_complete = False
    if table[player_id][0] >= obj_phase:
        phase_complete = True

    # Case 1: Attempt to complete phase 1 or 3
    if obj_phase == 1 or obj_phase == 3 and not (phase_complete):

        # checking what length of list should be depending on phase
        if obj_phase == 1:
            value_len = 3
        else:
            value_len = 4
        # checking if phase has been completed
        if len(check_value_play(hand, value_len)[0]) != 0:
            play_hand.append(check_value_play(hand, value_len)[0])
            play_type = 3
            phase_complete = True

    # Case 2: Attempt to complete phase 2
    if obj_phase == 2 and not (phase_complete):

        # assiging the desried length of hand with cards of same suit
        suit_len = 7

        # checking if phase has been completed
        if len(check_suit_play(hand, suit_len)[0]) != 0:
            play_hand.append(check_suit_play(hand, suit_len)[0])
            play_type = 3
            phase_complete = True

    # Case 3: Attempt to complete phase 4
    if obj_phase == 4 and not (phase_complete):

        # assiging the desired length of hand with run of cards_list
        run_len = 8

        # checking if phase has been completed
        if len(check_run_play(hand, run_len)[0]) != 0:
            play_hand.append(check_run_play(hand, run_len)[0])
            play_type = 3
            phase_complete = True

    '''# Case 4: Attempt to complet phase 5
    if obj_phase == 5 and not (phase_complete):


        # removing chosen cards from hand to check same value group
        hand_copy = copy.copy(hand)
        for mem in max_phase_1


        play_hand = max_phase
        play_type = 3'''

    # Case 5: no phases can be completed and so draw a card from the deck or
    # from the top of the discard pile
    if len(play_hand) == 0:


        # Drawing from deck
        play_hand = None
        play_type = 1



# need to check if picking discard pile top card completes phase, else pick top
# of deck
# need to write function that gets rid of largest card each turn
# need to wirte function that places card onto other players phase

    return (play_type, play_hand)
