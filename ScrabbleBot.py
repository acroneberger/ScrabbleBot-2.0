
import pytrie
import random
BOARD_BAG = ['a','a','a','a','a','a','a','a','a','b','b','c','c','d','d','d','d','e','e','e','e','e',
             'e','e','e','e','e','e','e','f','f','g','g','g','h','h','i','i','i','i','i','i','i','i','i',
             'j','k','l','l','l','l','m','m','n','n','n','n','n','n','o','o','o','o','o','o','o','o',
             'p','p','q','r','r','r','r','r','r','s','s','s','s','t','t','t','t','t','t','u','u','u','u',
             'v','v','w','w','x','y','y','z']
SCORES = {'a': 1, 'b': 3, 'c': 3, 'd':2, 'e':1, 'f':4, 'g':2, 'h':4, 'i':1, 'j':8, 'k':5, 'l':1,
          'm': 3, 'n':1, 'o':1, 'p':3, 'q':10, 'r':1, 's':1, 't':1, 'u':1, 'v':4, 'w': 4, 'x': 8, 'y':4, 'z':10}

BOARD_SIZE = 15
BINGO = 30

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
                'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']



board = [[0 for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]
game_bag = BOARD_BAG.copy()
random.shuffle(game_bag)
rack_1 = []
rack_2 = []
legal_move_candidates = []
num_bingoes = 0

scrabble_dictionary = []
base_dictionary=[]
base_precomputed = []
small_random_dictionary = []
small_random_precomputed = []
government_dictionary = []
government_precomputed = []
classic_lit_dictionary = []
classic_lit_precomputed = []
science_dictionary = []
science_precomputed = []
internet_dictionary = []
internet_precomputed = []



def precompute_small_subtrees(trie, precomputed_tries, depth):
    temp_list = []
    for i in range(len(alphabet)):
        current_letter_trie = trie.iterkeys(alphabet[i])
        for word in current_letter_trie:
            if len(word) >= depth:
                temp_list.append(word[0:depth+1])
    precomputed_tries.append(set(temp_list))


def build_tries():
    base_trie = pytrie.SortedStringTrie()
    for key in base_dictionary:
        base_trie[key] = key
    for i in range(1, 15):
        precompute_small_subtrees(base_trie, base_precomputed, i)

    small_random_trie = pytrie.SortedStringTrie()
    for key in small_random_dictionary:
        small_random_trie[key] = key
    for i in range(1, 15):
        precompute_small_subtrees(small_random_trie, small_random_precomputed, i)

    government_trie = pytrie.SortedStringTrie()
    for key in government_dictionary:
        government_trie[key] = key
    for i in range(1, 15):
        precompute_small_subtrees(government_trie, government_precomputed, i)

    classic_lit_trie = pytrie.SortedStringTrie()
    for key in classic_lit_dictionary:
        classic_lit_trie[key] = key
    for i in range(1, 15):
        precompute_small_subtrees(classic_lit_trie, classic_lit_precomputed, i)

    science_trie = pytrie.SortedStringTrie()
    for key in science_dictionary:
        science_trie[key] = key
    for i in range(1, 15):
        precompute_small_subtrees(science_trie, science_precomputed, i)

    internet_trie = pytrie.SortedStringTrie()
    for key in internet_dictionary:
        internet_trie[key] = key
    for i in range(1, 15):
        precompute_small_subtrees(internet_trie, internet_precomputed, i)


def initialize_dictionaries():
    with open("scrabble_dict.txt") as f:
        for line in f:
            val = line.rstrip().lower()
            scrabble_dictionary.append(val)
    with open("NYT_Sample_Dict.txt") as g:
        for line in g:
            val = line.rstrip().lower()
            base_dictionary.append(val)
    with open("government.txt") as h:
        for line in h:
            val = line.rstrip().lower()
            government_dictionary.append(val)
    with open("classics.txt") as i:
        for line in i:
            val = line.rstrip().lower()
            classic_lit_dictionary.append(val)
    with open("science.txt") as j:
        for line in j:
            val = line.rstrip().lower()
            science_dictionary.append(val)
    with open("emails.txt") as k:
        for line in k:
            val = line.rstrip().lower()
            internet_dictionary.append(val)


def get_small_random_dictionary():
    temp_list=random.sample(scrabble_dictionary, 40000)
    for i in range(len(temp_list)):
        small_random_dictionary.append(temp_list[i])


def find_all_anchors(board):
    candidate_anchors = []
    for i in range(15):
        for j in range(15):
            if ((board[i][j] == '-') and is_anchor_square(i,j)):
                this_anchor= (i,j)
                candidate_anchors.append(this_anchor)
    return set(candidate_anchors)


#Left and up anchors seem to be special cases where we also need to check if they are sandwiched between
#two columns/rows, and if this is the case do not allow them to be left anchors. Handled in getLegalMoves for now
def is_anchor_square(row, col):
    if board[row][col] == '-':
        up = row - 1
        if up >= 0 and board[up][col] != '-':
            return True
        down = row + 1
        if down <= 14 and board[down][col] != '-':
            return True
        left = col - 1
        if left >= 0 and board[row][left] != '-':
            return True
        right = col + 1
        if right <= 14 and board[row][right] != '-':
            return True
    return False


def draw_tiles(rack):
    while(len(rack) < 7 and len(game_bag) > 0):
        rack.append(game_bag.pop())


def cross_check_vert(letter, row, col, dictionary):
    tempRow = row
    tempCol = col
    word = []
    board[row][col] = letter
    #think we need to account for when there is no collision at all
    while(tempRow - 1 >= 0 and board[tempRow-1][col] != '-'):
        tempRow -= 1
    word.append(board[tempRow][tempCol])
    while(tempRow + 1 <= 14 and board[tempRow+1][col] != '-'):
        tempRow += 1
        word.append(board[tempRow][tempCol])
    board[row][col] = '-'
    word =''.join(word)
    return word in dictionary or len(word) == 1


def cross_check_horz(letter, row, col, dictionary):
    tempRow = row
    tempCol = col
    word = []
    board[row][col] = letter
    while(tempCol- 1 >= 0 and board[row][tempCol-1] != '-'):
        tempCol -= 1
    word.append(board[tempRow][tempCol])
    while(tempCol + 1 <= 14 and board[row][tempCol + 1] != '-'):
        tempCol += 1
        word.append(board[tempRow][tempCol])
    board[row][col] = '-'
    word =''.join(word)
    return word in dictionary or len(word) == 1


def calc_limit_vert(row,col, anchors):
    limit = 0
    while(row - 1 >= 0 and board[row-1][col] == '-' and (row-1, col) not in anchors):
        limit += 1
        row -= 1
    return min(limit, 7)


def calc_limit_horz(row, col, anchors):
    limit = 0
    while(col - 1 >= 0 and board[row][col-1] == '-' and (row, col-1) not in anchors):
        limit += 1
        col -= 1
    return min(limit, 7)


#We removed the node parameter because we can use partial worde as the prefix which will give us the children (really hopeful)
#(N' is edge here)
def extend_left(partial_word, limit, anchor_row, anchor_col, rack, valid_flag, scrabble_words, precomputed_tries):
    extend_right(partial_word, anchor_row, anchor_col, anchor_col+1, rack, valid_flag, scrabble_words, precomputed_tries)
    if limit > 0:
        for edge in get_edges(partial_word, precomputed_tries):
            letter = edge[-1]
            if ((letter in rack)):
                rack.remove(letter)
                valid_flag = True
                extend_left(edge, limit-1, anchor_row, anchor_col, rack, valid_flag, scrabble_words, precomputed_tries)
                rack.append(letter)


#CALL THIS DIRECTLY IF YOU ARE DIRECTLY TO THE RIGHT OF AN EXISTING TILE with partial word starting with that tile
def extend_right(partial_word, row, col, original_column, rack, valid_flag, scrabble_words, precomputed_tries):
    if(col == 15):
        if ((partial_word in scrabble_words) and valid_flag):
            this_move_tuple = (partial_word, row, col - len(partial_word), 'h',0)
            legal_move_candidates.append(this_move_tuple)
    elif( board[row][col] == '-'):
        #Ensures that we reach the letter we play off of
        if (col > original_column):
            if ((partial_word in scrabble_words) and valid_flag):
                this_move_tuple = (partial_word, row, col-len(partial_word), 'h',0)
                legal_move_candidates.append(this_move_tuple)
        for edge in get_edges(partial_word, precomputed_tries):
            letter = edge[-1]
            if ((letter in rack) and (cross_check_vert(letter, row, col, scrabble_words)) and (col<=14) and (edge != partial_word)):
                rack.remove(letter)
                valid_flag = True
                extend_right(edge, row, col + 1, original_column, rack, valid_flag, scrabble_words, precomputed_tries)
                rack.append(letter)
    else:
        letter = board[row][col]
        partial_plus_letter = partial_word + letter
        possible_sub_tries = get_edges(partial_plus_letter, precomputed_tries)
        if (len(possible_sub_tries) != 0 and (col+1 <= 14)):
            extend_right(partial_plus_letter, row, col+1, original_column, rack, valid_flag, scrabble_words, precomputed_tries)
        else:
            tempCol = col
            while((tempCol+1 <= 14) and (board[row][tempCol+1] != '-')):
                partial_plus_letter += board[row][tempCol+1]
                tempCol += 1
            if ((partial_plus_letter in scrabble_words)):
                this_move_tuple = (partial_plus_letter, row, col - (len(partial_plus_letter) -1), 'h',0)
                legal_move_candidates.append(this_move_tuple)


def extend_up(partial_word, limit, anchor_row, anchor_col, rack, valid_flag, scrabble_words, precomputed_tries):
    extend_down(partial_word, anchor_row, anchor_col, anchor_row+1, rack, valid_flag, scrabble_words, precomputed_tries)
    if limit > 0:
        for edge in get_edges(partial_word, precomputed_tries):
            letter = edge[-1]
            if ((letter in rack)):
                rack.remove(letter)
                valid_flag = True
                extend_up(edge, limit-1, anchor_row, anchor_col, rack, valid_flag, scrabble_words, precomputed_tries)
                rack.append(letter)


def extend_down(partial_word, row, col, original_row, rack, valid_flag, scrabble_words, precomputed_tries):
    if (row == 15):
        if ((partial_word in scrabble_words) and valid_flag):
            this_move_tuple = (partial_word, row - len(partial_word), col, 'v',0)
            legal_move_candidates.append(this_move_tuple)
    elif( board[row][col] == '-'):
        #Ensures that we reach the letter we play off of
        if (row > original_row):
            if ((partial_word in scrabble_words) and valid_flag):
                this_move_tuple = (partial_word, row-len(partial_word), col, 'v',0)
                legal_move_candidates.append(this_move_tuple)
        for edge in get_edges(partial_word, precomputed_tries):
            letter = edge[-1]
            if ((letter in rack) and (cross_check_horz(letter, row, col, scrabble_words)) and (row<=14) and (edge != partial_word)):
                rack.remove(letter)
                valid_flag = True
                extend_down(edge, row+1, col, original_row, rack, valid_flag, scrabble_words, precomputed_tries)
                rack.append(letter)
    else:
        letter = board[row][col]
        partial_plus_letter = partial_word + letter
        possible_sub_tries = get_edges(partial_plus_letter, precomputed_tries)
        if (len(possible_sub_tries) != 0 and (row+1 <= 14)):
            extend_down(partial_plus_letter, row+1, col, original_row, rack, valid_flag, scrabble_words, precomputed_tries)
        else:
            tempRow = row
            while ((tempRow + 1 <= 14) and (board[tempRow+1][col] != '-')):
                partial_plus_letter += board[tempRow + 1][col]
                tempRow += 1
            if ((partial_plus_letter in scrabble_words)):
                this_move_tuple = (partial_plus_letter, row - (len(partial_plus_letter) -1), col, 'v',0)
                legal_move_candidates.append(this_move_tuple)


def calc_score(move_tuple):
    word, original_row, original_col, direction, score = move_tuple
    row = original_row
    col = original_col
    bingo_counter = 0
    if (direction == 'v' ):
        for i in range(len(word)):
            if (board[row][col] == '-'):
                tempRow = row
                tempCol = col
                board[row][col] = word[i]
                bingo_counter += 1
                # think we need to account for when there is no collision at all
                while (tempCol - 1 >= 0 and board[tempRow][tempCol - 1] != '-'):
                    tempCol -= 1
                score += SCORES[board[tempRow][tempCol]]
                while (tempCol + 1 <= 14 and board[tempRow][tempCol + 1] != '-'):
                    tempCol += 1
                    score += SCORES[board[tempRow][tempCol]]
                board[row][col] = '-'
                if(((col-1 >= 0) and board[row][col-1] != '-') or ((col+1 <= 14) and board[row][col+1] != '-')):
                    score += SCORES[word[i]]
            else:
                score += SCORES[board[row][col]]
            row += 1
    else:
        for i in range(len(word)):
            if (board[row][col] == '-'):
                tempRow = row
                tempCol = col
                board[row][col] = word[i]
                bingo_counter += 1
                # think we need to account for when there is no collision at all
                while (tempRow - 1 >= 0 and board[tempRow - 1][tempCol] != '-'):
                    tempRow -= 1
                score += SCORES[board[tempRow][tempCol]]
                while (tempRow + 1 <= 14 and board[tempRow + 1][tempCol] != '-'):
                    tempRow += 1
                    score += SCORES[board[tempRow][tempCol]]
                board[row][col] = '-'
                if (((row - 1 >= 0) and board[row - 1][col] != '-') or ((row + 1 <= 14) and board[row + 1][col] != '-')):
                    score += SCORES[word[i]]
            else:
                score += SCORES[board[row][col]]
            col += 1
    if(bingo_counter == 7):
        score += BINGO
        global num_bingoes
        num_bingoes += 1
    return (word, original_row, original_col, direction, score)


def get_edges(word, precomputed_tries):
    temp_keys = []
    if (word == ''):
        return alphabet
    layer = precomputed_tries[len(word)-1]#offset by 1 because the precomputed_tries list starts at 2 letter words
    for key in layer:
        if (key != word and word == key[0:len(word)]):
            temp_keys.append(key)
    return set(temp_keys)


def place_legal_move(move_tuple, rack):
    word, row, col, direction,score = move_tuple
    if (direction == 'v' ):
        for i in range(len(word)):
            if (board[row][col] == '-'):
                board[row][col] = word[i]
                rack.remove(word[i])
            row += 1
    else:
        for i in range(len(word)):
            if (board[row][col] == '-'):
                board[row][col] = word[i]
                rack.remove(word[i])
            col += 1


def initialize_board():
    board_row = []
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            board[i][j] = "-"


def print_board():
    for i in range(BOARD_SIZE) :
        line = '  '.join(board[i])
        print(line)


def get_legal_moves(rack, dictionary, precomputed_trie):
    anchor_list = find_all_anchors(board)
    for anchor in anchor_list:
        row, col = anchor
        #Right anchor square
        if ((col-1 >= 0) and board[row][col-1] != '-'):
            tempCol = col
            while (tempCol - 1 >= 0 and board[row][tempCol - 1] != '-'):
                tempCol -= 1
            partial = board[row][tempCol:col]
            partial = ''.join(partial)
            extend_right(partial, row, col, col-len(partial), rack, False, dictionary, precomputed_trie)
            if ((row-1 >= 0) and board[row-1][col] == '-'):
                limit = calc_limit_vert(row, col, anchor_list)
                extend_up("", limit, row, col, rack, False, dictionary, precomputed_trie)
        #Left anchor square, new check added, need to fix bounds checking slightly due to prohibited edge of board cases
        if ((col+1 <= 14) and board[row][col+1] != '-' and (col-1 >= 0) and board[row][col-1] == '-'):
            limit = calc_limit_horz(row, col, anchor_list)
            extend_left("", limit, row, col, rack, False, dictionary, precomputed_trie)
            if ((row-1 >= 0) and board[row-1][col] == '-'):
                limit = calc_limit_vert(row, col, anchor_list)
                extend_up("", limit, row, col, rack, False, dictionary, precomputed_trie)
        #Down anchor square
        if ((row-1 >= 0) and board[row-1][col] != '-'):
            tempRow = row
            while (tempRow - 1 >= 0 and board[tempRow-1][col] != '-'):
                tempRow -= 1
            partial=[]
            for i in range(tempRow, row):
                partial.append(board[i][col])
            partial = ''.join(partial)
            extend_down(partial, row, col, row-len(partial), rack, False, dictionary, precomputed_trie)
            if ((col-1 >= 0) and board[row][col-1] == '-'):
                limit = calc_limit_horz(row, col, anchor_list)
                extend_left("", limit, row, col, rack, False, dictionary, precomputed_trie)
        #Up anchor square may throw error and need to do another bounds check
        if ((row+1 <= 14) and board[row+1][col] != '-' and (row-1 >= 0) and board[row-1][col] == '-'):
            limit = calc_limit_vert(row, col, anchor_list)
            extend_up("", limit, row, col, rack, False, dictionary, precomputed_trie)
            if ((col-1 >= 0) and board[row][col-1] == '-'):
                limit = calc_limit_horz(row, col, anchor_list)
                extend_left("", limit, row, col, rack, False, dictionary, precomputed_trie)


def play_game(D_Control, P_Control, D_Variable, P_Variable):
    final_score_1 = 0
    final_score_2 = 0
    turn_count_1 = 0
    turn_count_2 = 0
    draw_tiles(rack_1)
    draw_tiles(rack_2)

    #Special case for first move where player'1 will always call extend_right() on the center square.
    extend_right('', 7, 7, 7, rack_1, False, D_Control, P_Control)
    if (len(legal_move_candidates) == 0):
        print("Failed on first turn. Draw better.")
        return 0, final_score_1, final_score_2, turn_count_1, turn_count_2
    legal_moves_final = []
    for move in legal_move_candidates:
        move = calc_score(move)
        legal_moves_final.append(move)
    legal_move_candidates.clear()
    print("Player 1")
    print("All legal moves: " + str(legal_moves_final))
    actual_move = max(legal_moves_final,key=lambda item:item[4])
    print("Picking move " + str(actual_move))
    place_legal_move(actual_move, rack_1)
    draw_tiles(rack_1)
    move_score = actual_move[4]
    final_score_1 += move_score
    print_board()
    turn_count_1 += 1

    while((len(rack_1) > 0) and (len(rack_2) > 0)):
        pass_flag_1 = False
        pass_flag_2 = False
        #player 2's turn
        get_legal_moves(rack_2, D_Variable, P_Variable)
        if (len(legal_move_candidates) != 0):
            pass_flag_2 = False
            legal_moves_final = []
            for move in legal_move_candidates:
                move = calc_score(move)
                legal_moves_final.append(move)
            legal_move_candidates.clear()
            print("Player 2")
            print("All legal moves: " + str(legal_moves_final))
            actual_move = max(legal_moves_final, key=lambda item: item[4])
            print("Picking move " + str(actual_move))
            place_legal_move(actual_move, rack_2)
            draw_tiles(rack_2)
            move_score = actual_move[4]
            final_score_2 += move_score
            turn_count_2 += 1
            print_board()
        else:
            pass_flag_2 = True
        #player 1's turn
        get_legal_moves(rack_1, D_Control, P_Control)
        if (len(legal_move_candidates) != 0):
            pass_flag_1 = False
            legal_moves_final = []
            for move in legal_move_candidates:
                move = calc_score(move)
                legal_moves_final.append(move)
            legal_move_candidates.clear()
            print("Player 1")
            print("All legal moves: " + str(legal_moves_final))
            actual_move = max (legal_moves_final, key=lambda item: item[4])
            print("Picking move " + str(actual_move))
            place_legal_move(actual_move, rack_1)
            draw_tiles(rack_1)
            move_score = actual_move[4]
            final_score_1 += move_score
            turn_count_1 += 1
            print_board()
        else:
            pass_flag_1 = True
        if(pass_flag_1 and pass_flag_2):
            return 0, final_score_1, final_score_2, turn_count_1, turn_count_2
    print("End of game. Recording Statistics")
    return 1, final_score_1, final_score_2, turn_count_1, turn_count_2


def get_statistics(game_stats):
    game_state, final_score_1, final_score_2, turn_count_1, turn_count_2 = game_stats
    with open("results.txt", 'a') as results:
        results.write(str(final_score_1) + '\t' + str(final_score_2) + '\t' + str(turn_count_1) + '\t' +
                      str(turn_count_2) + '\t' + str(num_bingoes) + "\n")


def main_game_loop(n, dict, preC):
    i = 0
    while(i < n):
        #clear globals for each game and record stats
        initialize_board()
        global num_bingoes
        num_bingoes = 0
        game = play_game(base_dictionary, base_precomputed, dict, preC)
        global legal_move_candidates
        legal_move_candidates.clear()
        global game_bag
        game_bag = BOARD_BAG.copy()
        random.shuffle(game_bag)
        global rack_1
        global rack_2
        rack_1 = []
        rack_2 = []
        if(game[0] == 1):
            get_statistics(game)
            i += 1





initialize_dictionaries()
get_small_random_dictionary()
build_tries()

main_game_loop(1, government_dictionary, government_precomputed)
main_game_loop(1, internet_dictionary, internet_precomputed)
main_game_loop(1, classic_lit_dictionary, classic_lit_precomputed)
main_game_loop(1, science_dictionary, science_precomputed)
main_game_loop(1, small_random_dictionary, small_random_precomputed)
