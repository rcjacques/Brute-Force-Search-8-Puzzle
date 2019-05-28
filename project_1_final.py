'''
@Author: Rene Jacques
February 25, 2019
'''

import node, random
import csv #used for creating text files

class App:
	'''Main Class'''
	def __init__(self,start,goal,user_input):
		self.initial_state = start #initial puzzle state
		self.goal_state = goal #goal puzzle state
		self.current_node = None #initialize current_node storage as None
		self.current_index = 0 #initialize current_index storage as None
		self.nodes = [] #initialize empty list for nodes storage
		self.data = {start} #use a set to store states for duplicate checking
		self.input_error_flag = False #flag if user input is invalid

		#get user input if user_input flag is true
		if user_input:
			self.get_input()
		print('Start State: ',self.initial_state)
		print('Goal State:  ',self.goal_state)
		print()

		#check if user input was invalid
		if not self.input_error_flag:
			#if valid input then run puzzle solver
			self.run()
		else:
			#if invalid input then do not run solver and inform user
			print("CODE NOT RUN - INPUT ERROR")

	def get_input(self):
		'''Get start state and end state input from user'''

		#user input starting state
		start = input('Enter Start State (example: 123456780): ') 

		#check if user input is the correct length and does not contain a hyphen (and is not negative)
		if len(start) != 9 or '-' in start:
			print("Invalid Input - Not Enough Numbers")
			self.input_error_flag = True #raise input error flag if invalid number
			return

		#check if user input is a number
		try:
			int(start)
		except:
			print("Invalid Input - Not a Number")
			self.input_error_flag = True #raise input error flag if not a number
			return

		#user input goal state
		end = input('Enter Goal State (example: 123456780): ')

		#check if user input is the correct length and does not contain a hyphen (and is not negative)
		if len(end) != 9 or '-' in start:
			print('Invalid Input')
			self.input_error_flag = True #raise input error flag if invalid number
			return

		#check if user input is number
		try:
			int(end)
		except:
			print("Invalid Input - Not a Number")
			self.input_error_flag = True #raise input error flag if not a number
			return

		self.initial_state = start #set initial state to user input start state
		self.goal_state = end #set goal state to user input goal state
		
	def run(self):
		'''Main function'''
		running = True #flag to close while loop 
		impossible_flag = False #flag if puzzle is impossible
		n = node.Node()
		n.setData(self.initial_state)
		n.setID(0) #set root node id as 0
		n.setCost(0) #set root node cost as 0
		self.current_node = n 
		self.nodes.append(self.current_node)

		print('running...')

		count = 0
		#while current state is not equal to goal state find new states
		while self.current_node.getData() != self.goal_state and running:
			states = self.find_states(self.current_node.getData()) #find all possible moves from current state
			cnt = 0 #used to increment child ids within for loop

			#iterate through all possible states, check if they are duplicates, and create new nodes if they are unique
			for state in states:
				#check for duplicates using set self.data
				if state != self.current_node.getData() and state not in self.data:
					cnt += 1
					#create new node
					n = node.Node()
					n.setData(state)
					n.setID(self.current_index+cnt)
					n.setParent(self.current_node)
					n.setCost(self.current_node.getCost()+1)
					self.nodes.append(n) #add new node to node list
					self.data.add(state) #add new state to state set

			self.current_index += 1
			try:
				#try to get the next node to be checked using the node index
				self.current_node = self.nodes[self.current_index] 
			except:
				#if self.current_index does not exist in self.nodes then make sure that all possible states have been searched
				if len(self.nodes)==len(self.data): #max number of reachable states is 9!/2
					running = False #end while loop
					impossible_flag = True #raise impossible puzzle flag

		#if current state is equal to goal state then goal has been reached and create text files accordingly
		if self.current_node.getData() == self.goal_state:
			print('solution found')
			self.output_nodes()
			self.output_nodes_info()
			self.output_node_path()
		#if puzzle is impossible then create text files accordinglys
		elif impossible_flag:
			print('no solution possible')
			self.output_nodes()
			self.output_nodes_info()
			self.output_empty_path()
		print(self.current_index)

	def get_path(self,n):
		'''Returns node path by backtracking through node parents'''
		path = []
		self.recursive_get_path(path,n)
		return path

	def recursive_get_path(self,path,n):
		'''Recursive function for get_path()'''
		if n != None: #if parent exists
			path.append(n)
			path = self.recursive_get_path(path,n.getParent())
		return path

	def output_nodes(self):
		'''Save all nodes to text file'''
		with open('nodes.txt','w',newline='') as csvfile:
			writer = csv.writer(csvfile,delimiter=' ')
			for n in self.nodes:
				output = n.getData()
				output = output[0]+output[3]+output[6]+output[1]+output[4]+output[7]+output[2]+output[5]+output[8]
				writer.writerow(list(output))

	def output_nodes_info(self):
		'''Save all nodes info to text file'''
		with open('nodes_info.txt','w',newline='') as csvfile:
			writer = csv.writer(csvfile,delimiter=' ')
			for n in self.nodes:
				info = [n.getID(),n.getParent().getID() if n.getID() != 0 else -1,n.getCost()]
				writer.writerow(info)

	def output_node_path(self):
		'''Save path from initial state to goal state to text file'''
		with open('node_path.txt','w',newline='') as csvfile:
			writer = csv.writer(csvfile,delimiter=' ')
			path = self.get_path(self.current_node)
			self.print_path(path)
			for i in range(len(path)):
				n = path[len(path)-i-1]
				output = n.getData()
				output = output[0]+output[3]+output[6]+output[1]+output[4]+output[7]+output[2]+output[5]+output[8]
				writer.writerow(list(output))

	def output_empty_path(self):
		'''Save empty text file for impossible puzzles'''
		with open('node_path.txt','w',newline='') as csvfile:
			writer = csv.writer(csvfile,delimiter=' ')

	def find_states(self,data):
		'''Finds all possible moves for some input state and returns them'''
		zero = data.find('0') #find index of 0 in data list

		moves = []
		#move right if index of zero+! is not greater than 8 and the modulus of the index of zero is not equal to 2
		#meaning that zero is not located on the right side of the puzzle
		moves.append((data[zero+1] if zero+1 <= 8 else None) if data.find('0')%3 != 2 else None)
		#move left if index of zero-1 is not less than 0 and the modulus of the index of zero is not equal to 0
		#meaning that zero is not located on the left side of the puzzle
		moves.append((data[zero-1] if zero-1 >= 0 else None) if data.find('0')%3 != 0 else None)
		#move up if the index of zero-3 is not less than 0
		moves.append(data[zero-3] if zero-3 >= 0 else None)
		#move down if the index of zero+3 is not greater than 8
		moves.append(data[zero+3] if zero+3 <= 8 else None)

		states = []
		#loop through all moves and create their corresponding states
		for m in moves:
			if m != None:
				state = list(data) #turn data string into list for processing
				state[zero] = m #put the move into the zero index
				state[data.find(m)] = '0' #set the move index as 0
				states.append(''.join(state)) #turn state back into string
		return states

	def print_path(self,path):
		'''print out path data'''
		print('===')
		for n in path:
			state = n.getData()
			print(state[:3])
			print(state[3:6])
			print(state[6:])
			print('---')

def ran_start():
	'''Create random puzzle initial state'''
	options = ['0','1','2','3','4','5','6','7','8']
	output = ''
	for i in range(9):
		num =  random.choice(options)
		options.remove(num)
		output += num
	return output

if __name__ == '__main__':
	'''Auto run block'''

	#different potential start and goal states including a random state (not necessarily possible)
	ran = ran_start()
	easy = '123456708'
	sud_start = '614837052'
	sud_end = '123804765'
	impossible_start = '321456780'
	standard_goal = '123456780'
	new = '283164705'

	#create main application
	a = App(ran,standard_goal,user_input=True) #set user_input to True to run in command line with user input