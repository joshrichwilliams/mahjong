This code allows you to input scores from the MahJong tabletop game, and then automatically updates player money given the hand scores

Initialise the program in Python 3 using:

import mahjongpy3 as mj
game = mj.MahJong()

This sets up a MahJong class, which will contain all the game information.
The program will initially ask you for the names of the players, in order from East to North. These can be changed later.

In a standard game, if you run game.handend(), this represents the end of a hand and will ask you to input the scores for each person at the table.
After East makes a full rotation around the board, the round will end automatically, and save to a csv file with name formatting such as "BethChetanPatrickJosh.csv", in order of the players at the table.

The following functions are also available:
game.loadprevious()
	This allows you to import an ongoing game to continue player. Currently 		functionality is limited to importing a game where the previous round 			ended.
game.changesum()
	Change what the sum of scores should add up to, default is 8000, with 			2000 point starting hands
game.enternames()
	Change the names of players
game.enterstartscores()
	Change the starting score of each player
game.scoresondoors()
	Prints out current scores of players
game.handend()
	Ends the hand and allows you to input the scores. You can send the 			variable dead=True if it was a dead hand. Limit hand functionality is 			also automatically implemented, and you can change the size of limit 			hand by changing game.limithand
game.roundend()
	Ends the round. This will be called automatically once east does a full 		rotation.
game.winner()
	Automatic function which does some background work locating the winner.
game.codeint()
	Function for debugging, allows command line interface in the program.


#------------------------------------------------------------------------------#
Current plans for future functionality include:
	-Graphical user interface for non command line interaction
	-Plotting capabilities
	-Easy download and install
