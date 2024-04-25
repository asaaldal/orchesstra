import argparse
import chess.pgn

# Function to convert square index to algebraic notation
def square_to_algebraic(square):
    return chess.square_name(square)

# Function to generate the move list and board positions
def generate_movelist_and_boardpositions(pgn_file, moves_output_file, positions_output_file):
    # Load the PGN file
    pgn = open(pgn_file)
    game = chess.pgn.read_game(pgn)
    board = game.board()

    # Initialize clock times for White and Black
    white_clock = 2 * 60 * 60  # 2 hours in seconds
    black_clock = 2 * 60 * 60  # 2 hours in seconds

    # Initialize move counts for White and Black
    white_moves = 0
    black_moves = 0

    # Initialize total duration
    total_duration = 0

    # Open the output files
    with open(moves_output_file, "w") as moves_file, open(positions_output_file, "w") as positions_file:
        moves_file.write("Piece,From Square,To Square,Duration\n")
        positions_file.write("Board Position,Time\n")

        # Iterate through the mainline moves
        for move_node in game.mainline():
            move = move_node.move

            # Get piece, from square, and to square
            moving_piece = board.piece_at(move.from_square)
            piece_symbol = moving_piece.symbol().upper()
            from_square = square_to_algebraic(move.from_square)
            to_square = square_to_algebraic(move.to_square)

            # Calculate move duration
            if board.turn == chess.WHITE:
                white_moves += 1
                move_time = move_node.clock()
                if white_moves == 40:
                    white_clock += 30 * 60  # Add 30 minutes after move 40
                if white_moves > 0:
                    white_clock += 30  # Add 30 seconds increment
                duration = white_clock - move_time
                white_clock = move_time
            else:
                black_moves += 1
                move_time = move_node.clock()
                if black_moves == 40:
                    black_clock += 30 * 60  # Add 30 minutes after move 40
                if black_moves > 0:
                    black_clock += 30  # Add 30 seconds increment
                duration = black_clock - move_time
                black_clock = move_time

            # Convert duration to seconds
            duration_seconds = duration

            # Update total duration
            total_duration += duration_seconds

            # Write move info to the moves file
            moves_file.write(f"{piece_symbol},{from_square},{to_square},{duration_seconds}\n")

            # Write board position and time to the positions file
            fen = board.fen()
            positions_file.write(f"{fen},{duration_seconds}\n")

            # Update the board
            board.push(move)

    # Scale durations to ensure total duration is 3 minutes and 5 seconds
    #print(total_duration)
    scaling_factor = (3 * 60 + 5) / total_duration
    with open(moves_output_file, "r") as moves_file:
        moves_data = moves_file.readlines()
    with open(moves_output_file, "w") as moves_file:
        moves_file.write("Piece,From Square,To Square,Duration\n")
        for line in moves_data[1:]:
            pieces, from_square, to_square, duration = line.strip().split(',')
            scaled_duration = float(duration) * scaling_factor
            moves_file.write(f"{pieces},{from_square},{to_square},{scaled_duration}\n")

    with open(positions_output_file, "r") as positions_file:
        positions_data = positions_file.readlines()
    with open(positions_output_file, "w") as positions_file:
        positions_file.write("Board Position,Time\n")
        for line in positions_data[1:]:
            fen, time = line.strip().split(',')
            scaled_time = float(time) * scaling_factor
            positions_file.write(f"{fen},{scaled_time}\n")

def main():
    parser = argparse.ArgumentParser(description="Generate a movelist and boardpositions files from a PGN file.")
    parser.add_argument("pgn_file", type=str, help="Path to the PGN file containing the chess game.")
    parser.add_argument("moves_output_file", type=str, help="Path to save the movelist.csv file.")
    parser.add_argument("positions_output_file", type=str, help="Path to save the boardpositions.txt file.")
    args = parser.parse_args()

    # Extract command-line arguments
    pgn_file = args.pgn_file
    moves_output_file = args.moves_output_file
    positions_output_file = args.positions_output_file

    # Generate the move list and board positions
    generate_movelist_and_boardpositions(pgn_file, moves_output_file, positions_output_file)

if __name__ == "__main__":
    main()
