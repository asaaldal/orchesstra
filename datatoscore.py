def convert_to_pitch(square, piece):
    # Mapping squares to pitches
    square_map = {
        'a1': 57, 'b8': 74, 'c7': 57, 'd6': 64, 'e5': 72, 'f4': 79, 'g3': 62, 'h2': 69,
        'a2': 76, 'b1': 60, 'c8': 76, 'd7': 60, 'e6': 67, 'f5': 74, 'g4': 57, 'h3': 64,
        'a3': 72, 'b2': 79, 'c1': 62, 'd8': 79, 'e7': 62, 'f6': 69, 'g5': 76, 'h4': 60,
        'a4': 67, 'b3': 74, 'c2': 57, 'd1': 67, 'e8': 57, 'f7': 64, 'g6': 72, 'h5': 79,
        'a5': 62, 'b4': 69, 'c3': 76, 'd2': 60, 'e1': 67, 'f8': 60, 'g7': 67, 'h6': 74,
        'a6': 57, 'b5': 64, 'c4': 72, 'd3': 79, 'e2': 62, 'f1': 69, 'g8': 62, 'h7': 69,
        'a7': 76, 'b6': 60, 'c5': 67, 'd4': 74, 'e3': 57, 'f2': 64, 'g1': 72, 'h8': 64,
        'a8': 72, 'b7': 79, 'c6': 62, 'd5': 69, 'e4': 76, 'f3': 60, 'g2': 67, 'h1': 74
    }

    # For other pieces, use the standard square to pitch mapping
    return square_map[square.lower()]  # Convert input square to lowercase before mapping


def generate_rook_score(moves):
    rook_score = ""
    total_duration = 0

    for move in moves:
        parts = move.split(",")
        if len(parts) != 4:
            print(f"Ignoring invalid line: {move.strip()}")
            continue
        
        piece = parts[0].strip()
        square_from = parts[1].strip()
        square_to = parts[2].strip()
        duration = float(parts[3].strip())
        total_duration += duration
        if piece == 'R' and total_duration<185:
            rook_pitch_from = convert_to_pitch(square_from, piece)
            rook_pitch_to = convert_to_pitch(square_to, piece)

            # Start the rook sequence
            rook_start_time = total_duration
            interval = 0.25  # Interval between each note

            # Determine the direction of the sequence
            pitch = rook_pitch_from
            while pitch != rook_pitch_to:
                rook_score += f"\n{{{round(rook_start_time * 4) / 4} {1} {{RSOUND pitch: {pitch}}}}}"
                total_duration += interval  # Increment total duration by the interval
                pitch += 1 if rook_pitch_to > rook_pitch_from else -1  # Increment pitch by 1 or -1 depending on direction
                rook_start_time += .125
            rook_score += f"\n{{{round(rook_start_time * 4) / 4} {1} {{RSOUND pitch: {pitch}}}}}"
    return rook_score



def generate_bishop_score(moves):
    bishop_score = ""
    total_duration = 0
    last_bishop_pitch = None
    time_since_last_bishop_move = float('inf')

    for move in moves:
        parts = move.split(",")
        if len(parts) != 4:
            print(f"Ignoring invalid line: {move.strip()}")
            continue
        
        piece = parts[0].strip()
        square_to = parts[2].strip()
        duration = float(parts[3].strip())

        if piece == 'B':
            bishop_pitch = convert_to_pitch(square_to, piece)
            bishop_score += f"\n{{{round(duration * 4) / 4} {10} {{BSOUND pitch: {bishop_pitch}}}}}"

            if last_bishop_pitch is None:
                last_bishop_pitch = bishop_pitch
            time_since_last_bishop_move = 0
        else:
            time_since_last_bishop_move += duration

        if time_since_last_bishop_move >= 12 and last_bishop_pitch is not None:
            bishop_score += f"\n{{{round(total_duration * 4) / 4} {10} {{BSOUND pitch: {last_bishop_pitch}}}}}"
            time_since_last_bishop_move = 0

        total_duration += duration

    return bishop_score


def generate_score(moves):
    score = "{{0 0 {SCORE-BEGIN-END 0 185}}"
    total_duration = 0
    knight_moves = []

    white_queen_moves = []
    black_queen_moves = []
    is_white_turn = True

    for move in moves:
        parts = move.split(",")
        if len(parts) != 4:
            print(f"Ignoring invalid line: {move.strip()}")
            continue
        
        piece = parts[0].strip()
        square_to = parts[2].strip()
        duration = float(parts[3].strip())

        if piece == 'P':
            total_duration += duration
            continue
        elif piece == 'R':
            # Ignore rook moves here, as they're handled separately
            continue
        else:
            total_duration += duration
        
        pitch = None
        try:
            pitch = convert_to_pitch(square_to, piece)
        except KeyError:
            print(f"Square not found in map: {square_to}")

        if piece == 'Q':
            queenduration = total_duration
            if is_white_turn:
                white_queen_moves.append((square_to, total_duration))
                queen_moves = white_queen_moves
                for queen_square, queen_time in white_queen_moves:
                    queen_pitch = convert_to_pitch(queen_square, piece)
                    queen_start_time = total_duration - (queenduration - queen_time)
                    score += f"\n{{{round(queen_start_time * 4) / 4} {1} {{QSOUND pitch: {queen_pitch}}}}}"
                    queenduration+=.5
                #print(queen_moves)
            else:
                black_queen_moves.append((square_to, total_duration))
                queen_moves = black_queen_moves
                for queen_square, queen_time in black_queen_moves:
                    queen_pitch = convert_to_pitch(queen_square, piece)
                    queen_start_time = total_duration - (queenduration - queen_time)
                    score += f"\n{{{round(queen_start_time * 4) / 4} {1} {{QSOUND pitch: {queen_pitch}}}}}"
                    queenduration+=.5
        elif piece == 'N':
            knight_moves.append((square_to, total_duration))
        elif piece != 'B':
            sound_type = {
                'R': 'RSOUND',
                'K': 'KSOUND',
                'N': 'NSOUND',
                'B': 'BSOUND'
            }[piece]
            score += f"\n{{{round((total_duration - duration) * 4) / 4} {1} {{{sound_type} pitch: {pitch}}}}}"

        # Toggle turn
        is_white_turn = not is_white_turn

    return score


def generate_knight_score(moves):
    knight_score = ""
    timer = 0
    line_number = 0
    knight_moves = []

    while line_number < len(moves):
        parts = moves[line_number].split(",")
        duration = float(parts[3].strip())
        if timer + duration >= 2.5:
            timer = 0
            line_number += 1

        else:
            timer += duration
            line_number += 1

        # Look for knight moves and add them to the list
        if parts[0].strip() == 'N':
            knight_moves.append((parts[2].strip(), timer))

    # Generate a score element using the knight moves list
    if knight_moves:
        knight_start_time = 0
        while knight_start_time < 185:  # Add knight score elements until 185 seconds
            for knight_move in knight_moves:
                if knight_start_time<185:
                    knight_square_to, _ = knight_move
                    knight_pitch = convert_to_pitch(knight_square_to, 'N')
                    knight_score += f"\n{{{round(knight_start_time * 4) / 4} {1} {{NSOUND pitch: {knight_pitch}}}}}"
                    knight_start_time += 2.5  # Update start time for the next knight score element

    return knight_score


# Read moves from file
with open("movelist.txt", "r") as file:
    moves = file.readlines()

# Generate separate scores
knight_score = generate_knight_score(moves[1:])
bishop_score = generate_bishop_score(moves[1:])
rook_score = generate_rook_score(moves[1:])
nyquist_score = generate_score(moves[1:])

# Combine all scores
combined_score = nyquist_score + knight_score + bishop_score + rook_score

# Add required lines at the beginning and end of the content
combined_score = "set *piecescore* = " + combined_score + "\n}"

# Write the modified content to a new file with a .sal extension
with open("piecescore.sal", "w") as sal_file:
    sal_file.write(combined_score)
