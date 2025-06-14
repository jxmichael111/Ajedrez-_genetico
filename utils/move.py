def move_to_tuple(move_str):
    col_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    x1 = col_map[move_str[0]]
    y1 = 8 - int(move_str[1])
    x2 = col_map[move_str[2]]
    y2 = 8 - int(move_str[3])
    return (x1, y1, x2, y2)

def tuple_to_move(move):
    col_map = 'abcdefgh'
    x1, y1, x2, y2 = move
    return f"{col_map[x1]}{8 - y1}{col_map[x2]}{8 - y2}"

