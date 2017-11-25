import copy

# Initialising golobal variable for 'A'/Wild card
WILD = 'A'

def check_run(group):
    ''' Helper function designed to check if the input list is in order'''
    index_point = {
        '2': 0,
        '3': 1,
        '4': 2,
        '5': 3,
        '6': 4,
        '7': 5,
        '8': 6,
        '9': 7,
        '0': 8,
        'J': 9,
        'Q': 10,
        'K': 11
    }
    run = ['2', '3', '4', '5', '6', '7', '8', '9', '0', 'J', 'Q', 'K', 'A']
    start_point = 0
    group_copy = copy.copy(group)

    # If a wild card is assigned to a value smaller than 2
    wild_count = 0
    first_non_wild = 2
    for mem in group:
        if mem[0] == WILD:
            wild_count += 1
        else:
            first_non_wild = index_point[mem[0]]
            break
    if (first_non_wild - wild_count) < 0:
        return False

    # Checking the start point of a run while accounting for wild cards
    for i in range(0, (len(group_copy) + 1)):
        if group_copy[0][0] != WILD:
            start_point = index_point[group_copy[0][0]]
            break
        else:
            del group_copy[0]
    # Validating run
    for mem in group_copy:
        if mem[0] != WILD:
            if mem[0] != run[start_point]:
                return False
            else:
                start_point += 1
        else:
            start_point += 1
    return True


def check_value(group):
    ''' Helper function designed to take as input a group of cards to test and
    a value the cards are supposed to have returning true if the statisfy'''
    # Assigning value to check against while ignoring for wild card
    value = 0
    for mem in group:
        if mem[0] != WILD:
            value = mem[0]
            break
    # Checking for same value
    for mem in group:
        if mem[0] == value or mem[0] == WILD:
            pass
        else:
            return False
    return True


def check_suit(group):
    ''' Helper function desinged to check if the input list of cards has the
    same suit returning true if they do'''
    # Assigning suit to check against while ignoring for wild card
    suit = ''
    for mem in group:
        if mem[0] != WILD:
            suit = mem[1]
            break
    # Checking for same suits
    for mem in group:
        if mem[0] != WILD:
            if mem[1] == suit:
                pass
            else:
                return False
    return True


def check_colour(group, black=('S', 'C'), red=('H', 'D')):
    ''' Helper function designed to check if the input list of cards have a
    suit that belongs to the same colour returning true if they do'''
    colour = red

    # Setting the default colour to be tested while accounting for wild cards
    for mem in group:
        if mem[0] != WILD:
            if mem[1] in black:
                colour = black
        break

    # Check if the colour is the same
    for mem in group:
        if mem[0] != WILD:
            if not (mem[1] in colour):
                return False
    return True


def phasedout_group_type(group):
    '''Takes as input a list cards in hand and checks group conditions the
    cards satisfy returning the group the set of cards belong to'''
    # Phase the deck satisfies and will be updated throughout code
    phase = None
    # Phase the deck satisfies if len == 4
    phase_1 = None
    phase_2 = None
    # Condition of at least 2 natural cards
    count = 0
    for mem in group:
        if mem[0] != WILD:
            count += 1
    if count < 2:
        return None

    # Checking if conditions for group 1 are satisfied
    if len(group) == 3:
        # Condition of 3 cards of same value
        if check_value(group):
            phase = 1

    # Checking if conditions for  2 group satisfied
    if len(group) == 7:

        # Checking condition of 7 cards of same suit
        if check_suit(group):
            phase = 2

    # Checking if conditions for group 3 are satisfied
    if len(group) == 4:

        # Condition of 4 cards of same value
        if check_value(group):
            phase_1 = 3

    # Checking if conditions for group 4 are satisfied
    if len(group) == 8:

        # Condition of 8 cards in a consecutive run
        if check_run(group):
            phase = 4

    # Checking if conditions for group 5 are satisfied
    if len(group) == 4:

        # Checking if cards in order/same run
        if check_run(group):

            # Condition of 4 cards of the same colour
            if check_colour(group):
                phase_2 = 5

    # Checking what phase to return in case group len 4
    if phase_1 == 3 and phase_2 is None:
        phase = 3
    elif phase_1 is None and phase_2 == 5:
        phase = 5
    return phase


def phasedout_phase_type(phase):
    '''Takes as input a list of lists of groups of cards in hand and checks
    which phase that group of cards is in returning the phase of player'''
    phase_return = None
    # Condition of phase 1, 3 or 5 satisfied
    if len(phase) == 2:
        # Phase 1
        if phasedout_group_type(phase[0]) == phasedout_group_type(phase[1]):
            if phasedout_group_type(phase[0]) == 1:
                phase_return = 1
        # Phase 3
        if phasedout_group_type(phase[0]) == phasedout_group_type(phase[1]):
            if phasedout_group_type(phase[0]) == 3:
                phase_return = 3
        # Phase 5
        set_0 = phasedout_group_type(phase[0])
        set_1 = phasedout_group_type(phase[1])
        if set_0 == 5 and set_1 == 3:
            phase_return = 5

    # Condition of phase 2 or 4 satisfied
    if len(phase) == 1:
        # Phase 2
        if phasedout_group_type(phase[0]) == 2 and len(phase[0]) == 7:
            phase_return = 2
        # Phase 4
        if phasedout_group_type(phase[0]) == 4 and len(phase[0]) == 8:
            phase_return = 4

    return phase_return
