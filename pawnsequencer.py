def preprocess_input_data(input_data):
    """
    Preprocess input data by replacing integers with 'o' to represent empty squares.
    """
    processed_data = []
    lines = input_data.strip().split('\n')
    # Skip the header line
    lines = lines[1:]
    for line in lines:
        fen, duration = line.split(',')[0], float(line.split(',')[1])
        processed_fen = ''
        for char in fen:
            if char.isdigit():
                # Replace digits with 'o' repeated the corresponding number of times
                processed_fen += 'o' * int(char)
            else:
                processed_fen += char
        processed_data.append((processed_fen, duration))
    return processed_data

def read_input_data(input_data):
    """
    Read input data and extract pawn positions and durations.
    """
    pawn_positions = []
    processed_data = preprocess_input_data(input_data)
    # Initialize accumulated duration
    accumulated_duration = 0.0
    
    for fen, duration in processed_data:
        ranks = fen.split()[0].split('/')
        white_pawn_squares = []
        black_pawn_squares = []
        for idx, rank in enumerate(reversed(ranks[1:])):  # Reverse the ranks to match FEN notation
            for col, char in enumerate(rank):
                if char == 'P':
                    # Convert file index to algebraic notation
                    file_notation = chr(97 + col)
                    # Convert rank index to algebraic notation
                    rank_notation = str(idx+1)
                    white_pawn_squares.append(f'{file_notation}{rank_notation}')
                elif char == 'p':
                    file_notation = chr(97 + col)
                    rank_notation = str(idx+1)
                    black_pawn_squares.append(f'{file_notation}{rank_notation}')
        pawn_positions.append((white_pawn_squares, black_pawn_squares, accumulated_duration))
        accumulated_duration += duration
    return pawn_positions

def pawns_at_time(pawn_positions):
    """
    Extract white and black pawn positions at different times and generate Nyquist score.
    """
    current_time = 0.0
    file_index = 0
    pawn_positions_at_times = []
    line = 0
    white_pawn_squares, black_pawn_squares, boardtime = pawn_positions[line]
    # Loop until the end time is reached (3 minutes and 5 seconds)
    while current_time <= 185.0:
        while boardtime <= current_time and line < len(pawn_positions) - 1:
            line += 1
            white_pawn_squares, black_pawn_squares, boardtime = pawn_positions[line]
        if white_pawn_squares or black_pawn_squares:
            # Extract white pawns and black pawns in the current file
            white_pawns_in_file = [(pawn, rank) for pawn, rank in white_pawn_squares]
            black_pawns_in_file = [(pawn, rank) for pawn, rank in black_pawn_squares]
            file_index_alph = chr(97 + file_index)
            white_pawns_in_file_at_time = []
            black_pawns_in_file_at_time = []
            for pawn in white_pawns_in_file:
                if pawn[0] == file_index_alph:
                    white_pawns_in_file_at_time.append(pawn[1]) 
            for pawn in black_pawns_in_file:
                if pawn[0] == file_index_alph:
                    black_pawns_in_file_at_time.append(pawn[1])
            pawn_positions_at_times.append((current_time, white_pawns_in_file_at_time, black_pawns_in_file_at_time))
            #print([current_time, white_pawns_in_file_at_time, black_pawns_in_file_at_time])
        # Increment current time by 0.5 seconds
        current_time += 0.25
        # Increment file index
        file_index = (file_index + 1) % 8

    return pawn_positions_at_times

def generate_score_elements(data):
    white_drum_sounds = {
        '2': 'hihathit',
        '3': 'tom',
        '4': 'snare',
        '5': 'hihat',
        '6': 'kick',
        '7': 'cymbal',
        '8': 'crashcymbal'
    }
    black_drum_sounds = {
        '7': 'hihathit',
        '6': 'tom',
        '5': 'snare',
        '4': 'hihat',
        '3': 'kick',
        '2': 'cymbal',
        '1': 'crashcymbal'
    }
    score_elements = []
    
    for item in data:
        start_time = item[0]
        white_drum_sound_list = item[1]
        black_drum_sound_list = item[2]
        
        for drum_sound_str in white_drum_sound_list:
            drum_sound = white_drum_sounds.get(drum_sound_str)
            if drum_sound:
                score_element = "{%g .5 {%s}}" % (start_time, drum_sound)
                score_elements.append(score_element)
        for drum_sound_str in black_drum_sound_list:
            drum_sound = black_drum_sounds.get(drum_sound_str)
            if drum_sound:
                score_element = "{%g .5 {%s}}" % (start_time, drum_sound)
                score_elements.append(score_element)

    with open("drumscore.sal", "w") as file:
        file.write("set *drumscore* = {\n")
        for score_element in score_elements:
            file.write(score_element + "\n")
        file.write("}")

input_file = "positions.txt"
try:
    with open(input_file, "r") as file:
        # Read the input data
        input_data = file.read()
except FileNotFoundError:
    print(f"File '{input_file}' not found.")
    exit(1)

# Extract pawn positions from input data
pawn_positions = read_input_data(input_data)

# Generate Nyquist score using pawn positions
generate_score_elements(pawns_at_time(pawn_positions))
