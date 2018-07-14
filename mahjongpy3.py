#!/usr/bin/python
#code which loads,calculates and saves MahJong scores
#author: Joshua Williams

import numpy as np
import csv 
import copy
import code


#setting up the class for the MahJong game
class MahJong:
	def __init__(self):
		self.setup()	
	
	#setting up the initial score and the east values
	def setup(self):
		"""
		Setting up the initial state of the MahJong class
		"""
		#setting all the original scores
		self.totscore = np.array([2000,2000,2000,2000])
		
		#setting up matrix for saving the scores of each round
		self.handscores = []
		self.handscores.append(np.array([0,0,0,0]))
		
		#setting up east 
		self.east = np.array([True,False,False,False])

		#setting up saving the scores during each round
		self.scoresave = []
		self.scoresave.append(copy.copy(self.totscore))

		#counter for saving score backup files
		self.count = 1
		
		#default what all the scores should add up to
		self.allscoresum = 8000
		
		#default what the limit hand is
		self.limithand = 500.
		
		#default names
		self.names = np.array(['ffffffffffffffffffffffffffffffffffffffffffffffff','ffffffffffffffffffffffffffffffffffffffffffffffff','ffffffffffffffffffffffffffffffffffffffffffffffff','ffffffffffffffffffffffffffffffffffffffffffffffff'])
		self.windnames = np.array(['East','South','West','North'])
		
		#setting up saving who was the winner and who was east
		self.eastsave = []
		self.eastsave.append(self.names[0])
		self.winsave = []
		self.winsave.append('n/a')
		
		#asking the user what the names are
		self.enternames(self)
		
	
	#NEED TO TEST THIS
	#for the case where a game is already in progress, load the csv file with the previous scores in
	def loadprevious(self,fname,delimiter = None):
		"""
		Work in progress
		"""
		#checking delimiter is not different
		if delimiter is None:
			delimiter = '\t'

		self.scoresave = []

		#opening the file to be read
		with open(fname,'r') as f:
			reader = csv.reader(f,delimiter=delimiter)
			ii = 0
			for row in reader:
				if ii == 0:
					#getting the names out of the csv file
					namtemp = []
					for jj in range(4):
						namtemp.append(row[jj])
					self.names = np.array(namtemp)
				else:
					#getting the scores out of the csv file
					scoretemp = []
					tottemp = []
					for jj in range(len(row)):
						if jj <4:
							scoretemp.append(float(row[jj]))
						elif jj >3 and jj< 8:
							tottemp.append(float(row[jj]))
						elif jj == 8:
							self.eastsave.append(row[jj])
						elif jj == 9:
							self.winsave.append(row[jj])
					self.scoresave.append(np.array(tottemp))
					self.handscores.append(np.array(scoretemp))
				ii += 1
		self.totscore = np.array(tottemp)
		self.eastsave = np.delete(self.eastsave,0,0)
		self.eastsave = list(self.eastsave)
		self.winsave = np.delete(self.winsave,0,0)
		self.winsave = list(self.winsave)
	
	#changing value that all the scores should sum tofor people who don't work with classes
	def changesum(self,value):
		"""
		self.changesum(value)
		Changing what the sum of the scores should add up to if the setup is different
		var value:  Value to be substituted in as the sum of all scores
		"""
		self.allscoresum = value
	
	#getting names of people playing
	def enternames(self,name1=None,name2=None,name3=None,name4=None,quick=False):
		"""
		self.enternames(name1=None,name2=None,name3=None,name4=None,quick=False)
		Entering the names of the players, these should be easy to 
		remember for convenience sake
		var name1: Name of first player etc.
		var quick: When set to True, this means the user has sent the 
			   the names in already in the function call
		"""
		#resetting saving who is east
		self.eastsave = []
		
		#when quick is True then pull the scores directly from the function call
		if quick is True:
			#setting up name array
			self.names = np.array([name1,name2,name3,name4])
		else: 
			#when quick is not true than we need to ask the user for each
			#name (this is for normal people)
			#looping through the four players
			for i in range(4):
				self.names[i] = input('Please enter name of Player '+str(i+1)+' ('+self.windnames[i]+'):')
		
		#saving the first east
		self.eastsave.append(self.names[0])
				
		
	#setting scores if I'm doing scores round by round
	def enterstartscores(self,score1=None,score2=None,score3=None,score4=None,quick=False):
		"""
		self.enterscores(score1=None,score2=None,score3=None,score4=None,quick=False)
		If you're redefining the scores at the start of a round then
		you can enter them in this function
		var score1: Score of first name, etc.
		var quick:  When true, the scores will be read directly from the function call
		"""
		
		#when quick is true grabbing the scores directly from the function call
		if quick is True:
			#redefining totscore
			self.totscore = np.array([score1,score2,score3,score4])
		else:
			#when quick is not true than we need to ask the user for each
			#score (this is for normal people)
			
			for i in range(4):
				self.totscore[i] = input('Please enter score of Player '+str(self.names[i])+' ('+self.windnames[i]+'):')

		
		
		#checking the scores add up correctly
		if np.sum(self.totscore) != self.allscoresum:
			raise ValueError('Total score must add up to '+str(self.allscoresum)+'!')
		
		#resetting scoresave
		self.scoresave = []
		self.scoresave.append(copy.copy(self.totscore))
		
	#printing out the scores of the round
	def scoresondoors(self):
		"""
		self.scoresondoors()
		Print out the scores of the last hand
		"""
		#printing each name and score
		for ii in range(0,len(self.names)):
			print(self.names[ii]+' has '+str(self.totscore[ii]))
	
	#function for calculating scores at the end of the hand
	def handend(self,winname=None,roundscores=None,resetlast=False,dead=False):
		"""
		self.handend(winname,roundscores,resetlast=False,dead=False)
		At the end of each hand run this function to input the scores
		var winname: String, name of the winner
		var score1:  Score of the first name in the names array
		var score2:  Second name score
		var score3:  Third name score
		var score4:  Fourth name score
		var resetlast:  Allows the user to overwrite the previous saved
				values if they were input wrong
		var dead:    For cases where we have a dead hand and therefore you pass along
		You can use self.scoresondoors() to check the names
		"""
		#in the case where we do have a dead hand
		if dead is True:
			#saving the scores as the previous round
			self.scoresave.append(copy.copy(self.totscore))
			self.handscores.append(np.array([0.0,0.0,0.0,0.0]))
			
			#saving east as east
			#self.codeint(locals(),globals())
			eastloc = np.argwhere(self.east==True).flatten()
			self.eastsave.append(self.names[eastloc][0])
			
			#saving the winner as dead hand 
			self.winsave.append('Dead Hand')
		
		#when the hand wasn't a dead hand
		elif dead is False:
			#checking if I'm trying to reset the last round
			if resetlast is True:
				#resetting east
				eastloc = np.argwhere(self.names==self.eastsave[-2])
				self.east = np.array([False,False,False,False])
				self.east[eastloc] = True

				#resetting win locations
				winloc = np.argwhere(self.names==self.winsave[-2])

				#resetting total scores
				self.totscore = copy.copy(self.scoresave[-2])
				self.count = self.count-1

				#removing last values saved
				self.scoresave.pop(-1)
				self.eastsave.pop(-1)
				self.winsave.pop(-1)

			#getting the user to input the winners name
			winname = input("Please enter the name of the winner:")
			
			#getting the scores of each player
			roundscores = np.empty(4)
			for ik in range(4):
				roundscores[ik] = input('Please enter score of Player '+str(self.names[ik])+' ('+self.windnames[ik]+'):')
			
			
			#first allocating the winner
			winloc = self.winner(winname)

			#now calculating the scores
			#first finding which player is east
			eastloc = np.argwhere(self.east==True).flatten()

			#handscores array
			handscore = roundscores
			self.handscores.append(copy.copy(handscore))
			
			#allocating score calculation arrays
			scorec = np.array([1,1,1,1])
			scorec[eastloc] = 2
			
			
			#looping through and calculating the scores
			for ii in range(len(self.totscore)):
				#setting up score calculation for array
				scorectemp = copy.copy(scorec)
				scorectemp[ii] = 0 #set player not to pay it
				scorectempmin = copy.copy(scorectemp)
				scorectemp[winloc] = 0 #set winner not to pay it

				#making adjustments to values that will be removed
				scorectempmin[winloc] = 1.0 #pay winners score
				scorectempmin[eastloc] = 2.0 #double east
				scorectempmin[ii] = 0 #player doesn't pay

				
				#if player is east
				if ii == eastloc:
					scorectemp = scorectemp*2.0
					scorectempmin = scorectempmin*2.0
				
				
				#updating scores with scores from this hand
				for xval in range(len(scorectemp)):
					#adding on what the player won
					if np.multiply(scorectemp[xval],handscore[ii]) < self.limithand:
						self.totscore[ii] = self.totscore[ii]+np.multiply(scorectemp[xval],handscore[ii])
					else:
						self.totscore[ii] = self.totscore[ii] + self.limithand
					#if the player is not the winner then remove points
					if ii != winloc:
						#checking for cases where you're removing more than the limit hand
						if np.multiply(scorectempmin[xval],handscore[xval]) < self.limithand:
							self.totscore[ii] = self.totscore[ii] - np.multiply(scorectempmin[xval],handscore[xval])
						#if the score is more than the limit	
						else:
							self.totscore[ii] = self.totscore[ii] - self.limithand
				
				

			#saving the scores
			self.scoresave.append(copy.copy(self.totscore))

			#saving who was the winner and who was east
			self.eastsave.append(self.names[eastloc][0])
			self.winsave.append(self.names[winloc][0])

			#reallocating east
			if eastloc != winloc:
				self.east[eastloc] = False
				if eastloc+1 > 3:
					#in this case it must be the end of the round
					self.roundend()
				else:	
					self.east[eastloc+1] = True

			#for each hand back up the scores in a csv file
			with open('backup'+str(self.count)+'.csv','w') as f:
				writer = csv.writer(f,delimiter='\t')
				writer.writerows(zip(self.names,self.totscore))
			self.count+= 1


	#doing end of round things
	def roundend(self):
		"""
		Writing the final results out to file at the end of the round, format below
		Headers
		Scores of hand, total scores after hand, east, winner
		"""
		#setting up headers array
		headers = []
		for ii in self.names:
			headers.append(ii)
		for ii in self.names:
			headers.append(ii)
		headers.append('East')
		headers.append('Winner')
		
		#writing out a csv file with the names as headers, and then the scores of each hand
		with open(self.names[0]+self.names[1]+self.names[2]+self.names[3]+'.csv','w') as f:
			writer = csv.writer(f,delimiter='\t')
			writer.writerow(headers)
			for ix in range(len(self.scoresave)):
				tlist = []
				for val in self.handscores[ix]:
					tlist.append(val)
				for val in self.scoresave[ix]:
					tlist.append(val)
				tlist.append(self.eastsave[ix])
				tlist.append(self.winsave[ix])
				
				writer.writerow(tlist)
		
		print('End of Round!!!')
	

	#---------------------------------------------------------------------------#
	#small functions, which include error jump outs

	#setting the winner (called in handend)
	def winner(self,winname):
		"""
		Identifying the winner from the given name
		var winname:	Name of winner (string)
		"""
		
		#finding the location of winner in numpy array
		winloc = np.argwhere(self.names==winname).flatten()
		#self.codeint(locals(),globals())
		
		#if name does not exist for this game
		if np.in1d(winname,self.names) == False:
			#checking for 
			raise ValueError('Name does not exist, pick one of the following: '+
						self.names[0]+', '+self.names[1]+', '+self.names[2]+
						', '+self.names[3])
			
		else:
			#if the name does exist
			return winloc

	#code interact function
	def codeint(self,localsvar,globalsvar):
		"""
		Allows the user to jump in whether they insert this function
		function should be called as self.codeint(locals(),globals())
		var localsvar:	locals()
		var globalsvar:	globals()
		"""
		#to call self.codeint(locals(),globals())
		code.interact(local=dict(globalsvar, **localsvar))
