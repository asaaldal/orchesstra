import subprocess

def run_gameextractor(pgn_file, moves_output_file, positions_output_file):
    subprocess.run(["python", "gameextractor.py", pgn_file, moves_output_file, positions_output_file])

def run_datatoscore():
    subprocess.run(["python", "datatoscore.py"])

def run_pawnsequencer():
    subprocess.run(["python", "pawnsequencer.py"])

def main():
    # Define the arguments for gameextractor.py
    pgn_file = "Firouzja,_Alireza_vs_Nakamura,_Hikaru_2024.04.09.pgn"
    moves_output_file = "movelist.txt"
    positions_output_file = "positions.txt"

    # Run gameextractor.py with the provided arguments
    run_gameextractor(pgn_file, moves_output_file, positions_output_file)

    # Run datatoscore.py
    run_datatoscore()

    # Run pawnsequencer.py
    run_pawnsequencer()

if __name__ == "__main__":
    main()
