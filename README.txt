# orchesstra
Chess to music transcription
python:
First, download a game in .pgn format from chess.com or similar, or create your own. Format should match the Firouzja vs Nakamura sample file provided
Next, install all required packages for gameanimator.py, gameextractor.py, datatoscore.py, pawnsequencer.py, tpprep.py  
-gameanimatorpy.py will create an animation and save to mp4 of the game, with the scaled durations represented accurately  
-gameextractor.py will create two txt files, fromt the pgn file that are more usable: a positions.txt file that contains board positions at a given time, and movelist.txt, that is just an easily readable version of the pgn file  
-datatoscore.py will read the movelist.txt file and produce score elements for the major pieces  
-pawnsequencer.py will read the positions.txt file and produce score elements for the pawns  
-tpprep.py will run all of the above in order, to produce two sal files, drumscore.sal and piecescore.sal which are loaded into nyquist script tp.sal. change the pgn_file argument to whatever the path to your .pgn file is, or use the one provided.   


nyquist:
A guide to install Nyquist can be found here: https://www.cs.cmu.edu/~15322/resources/

Make sure you have successfully run tpprep.py. Then, you can run tp.sal, which will use the score files to create music. There are some preloaded instruments in tp.sal, but these are meant to be played with to generate different sounds. As currently populated:
-The drum score will call different drum sounds that are saved to the same directory as .wav files
-The bishop sound (BSOUND) is a randomly generated baseline
-The knight sound is a simple chord
-The rook sound is a simple note
-The Queen sound is a flute sound
-The king sound takes the amplitude from grains in a wav file containing an interview of Hikaru Nakamura and applies them to the chord progression called strums.wav

Running tp.sal will result in a .wav sound file of roughly the specified duration that can be applied to the animation mp4 video to get the full audio/video product. 
