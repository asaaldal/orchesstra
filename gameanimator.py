import chess
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from matplotlib.animation import FuncAnimation

# Function to draw chess board image
def draw_board(fen):
    board = chess.Board(fen)
    pieces = board.piece_map()
    image_dict = {
        'p': 'pieces/blackP.png', 'r': 'pieces/blackR.png', 'n': 'pieces/blackN.png',
        'b': 'pieces/blackB.png', 'q': 'pieces/blackQ.png', 'k': 'pieces/blackK.png',
        'P': 'pieces/whiteP.png', 'R': 'pieces/whiteR.png', 'N': 'pieces/whiteN.png',
        'B': 'pieces/whiteB.png', 'Q': 'pieces/whiteQ.png', 'K': 'pieces/whiteK.png',
    }

    for square, piece in pieces.items():
        file, rank = chess.square_file(square), 7 - chess.square_rank(square)  # Flip the rank
        image = plt.imread(image_dict[piece.symbol()])
        im = OffsetImage(image, zoom=0.7)
        ab = AnnotationBbox(im, (file + 0.5, rank + 0.5), xycoords='data', frameon=False)
        ax.add_artist(ab)

# Function to update animation
def update(frame):
    print(frame)
    ax.clear()
    ax.set_axis_off()
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 8)
    ax.invert_yaxis()
    if frame < len(frame_cache):
        draw_board(frame_cache[frame])
    else:
        frame_cache.append(total_frames[frame][0])
        draw_board(total_frames[frame][0])
    draw_chessboard()
    return []

# Function to draw empty chessboard
def draw_chessboard():
    for file in range(8):
        for rank in range(8):
            color = 'wheat' if (file + rank) % 2 == 0 else 'saddlebrown'
            ax.add_patch(Rectangle((file, rank), 1, 1, color=color))

# Parse positions and durations from text file
frames = []
with open('positions.txt', 'r') as file:
    lines = file.readlines()
    for line in lines[1:]:
        fen, duration = line.split(',')[0], float(line.split(',')[1])
        frames.append((fen, duration))

# Insert duplicate frames to match durations
total_frames = []
for fen, duration in frames:
    num_frames = int(duration * 30)  # Change FPS to 30
    total_frames.extend([(fen, duration)] * num_frames)

# Cache to store generated frames for each move
frame_cache = []

# Create animation
fig, ax = plt.subplots(figsize=(6, 6))
ani = FuncAnimation(fig, update, frames=len(total_frames), blit=True)

# Save animation as MP4 with 30 FPS
ani.save('chess_animation.mp4', writer='ffmpeg', fps=30, extra_args=['-pix_fmt', 'yuv420p'])
plt.close(fig)
