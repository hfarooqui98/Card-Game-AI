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
