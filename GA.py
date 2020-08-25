import random
import copy
import enum
import math
from datetime import datetime

class Element:
	cost = 0
	val = 0

	def __init__(self, val, cost):
		self.val = val
		self.cost = cost
	
	def setVal(self, val):
		self.val = val

	def setCost(self, cost):
		self.cost = cost

	def getCost(self):
		return self.cost
	
	def getVal(self):
		return self.val

def parseDataset(fp, delim):
	dataset = []
	i = 0
	for line in fp:
		line = line.strip('\n')
		if line != 'EOF':
			row = line.split(delim)
			#Append the coordinates
			dataset.append((i, [float(row[1]), float(row[2])]))
			i += 1
	return dataset

def calcCost(arr, dist):
	total_dist = 0
	for i in range(len(arr)):
		j = i + 1
		if j == len(arr):
			j = 0
		total_dist += math.sqrt(pow(arr[i][1][0] - arr[j][1][0], 2) + pow(arr[i][1][1] - arr[j][1][1], 2))
	return total_dist

def mutate(val, mutation_rate):
	val_len = len(val)
	if random.random() < mutation_rate:
		rand1 = random.randrange(0, val_len)
		rand2 = random.randrange(0, val_len)
		while rand1 == rand2:
			rand2 = random.randrange(0, val_len)

		temp = val[rand1]
		val[rand1] = val[rand2]
		val[rand2] = temp
	return val

def crossover(chrom1, chrom2, mutation_rate):
	val1 = chrom1.getVal()
	val2 = chrom2.getVal()

	city_lists = [val1, val2]

	answers = []
	for switch in range(2):
		default_iter = 0
		last_idx = 0
		new_val = []
		track_val = []
		rev_idx = [{}, {}]
		for i in range(len(val1)):
			new_val.append((-1, [-1.0, -1.0]))
			track_val.append(-1)
			rev_idx[0][val1[i][0]] = i
			rev_idx[1][val2[i][0]] = i
		next_city = 0
		match_offset = 0
		while default_iter < len(new_val):
			if city_lists[0][default_iter][0] in track_val and city_lists[1][default_iter][0] in track_val:
				default_iter += 1
			#For the first case, randomly pick either the first or second chromosome's contents
			elif default_iter == 0 or next_city in track_val:
				#Insert the city in the new list
				switch = (switch + default_iter) % 2
				new_val[default_iter] = city_lists[switch][default_iter]
				track_val[default_iter] = city_lists[switch][default_iter][0]

				#Flip switch and set the next city to look for
				next_city = city_lists[not switch][default_iter][0]
				default_iter += 1
			else:
				insert_idx = rev_idx[switch][next_city]

				#Flip switch and set the next city to look for
				next_city = city_lists[not switch][insert_idx][0]
				#Insert the city in the new list
				new_val[insert_idx] = city_lists[switch][insert_idx]
				track_val[insert_idx] = city_lists[switch][insert_idx][0]
			
		answers.append(new_val)
	
	return (mutate(answers[0], mutation_rate), mutate(answers[1], mutation_rate))

def GA():
	#Read in data
	print("Please specify an input file:")
	fin_str = input()
	fin = open(fin_str, "r")

	#Go past the header info
	for i in range(7):
		line = fin.readline()
	
	#Parse the data
	dataset = parseDataset(fin, ' ')

	#Seeding random
	random.seed(datetime.now())

	#Getting input
	pop_sz = int(input("Please specify a population size: "))
	mutation_rate = float(input("Please specify a mutation rate: "))
	crossover_rate = float(input("Please specify a crossover rate (recommended to be close to one since swapping sometimes isn't possible): "))
	iter_num = int(input("Please specify a number of iterations: "))

	#Initialize the x population
	pop = []
	min_cost = 4265489751
	min_val = 0
	#Gen random 32-bit nums
	for i in range(pop_sz):
		val = copy.copy(dataset)
		random.shuffle(val)
		cost = calcCost(val, dataset)
		pop.append(Element(val, cost))
		if cost < min_cost:
			min_cost = cost
			min_val = val
	

	#Sort so that the lowest cost is at the top for the first iter
	#pop.sort(key=lambda element: element.getCost())

	#Put inside of some while not converged
	#Calculate current cost
	gen_count = 0
	convergence = {}
	while gen_count < iter_num:
		new_gen = []
		random.shuffle(pop)
		mating_pool = []
		for i in range(0, len(pop), 2):
			if i > len(pop) - 2:
				break
			if(pop[i].getCost() < pop[i+1].getCost()):
				mating_pool.append(pop[i])
			else:
				mating_pool.append(pop[i+1])

		#Breeding
		for i in range(0, len(mating_pool)):
			#Create the new crossed over entity (possibly with mutation)
			#Setting the second val
			j = i + 1
			if i == len(mating_pool) - 1:
				j = 0

			new_vals = (0,0)
			if random.random() < crossover_rate:
				new_vals = crossover(mating_pool[i], mating_pool[j], mutation_rate)
			else:
				new_vals = (mating_pool[i].getVal(), mating_pool[j].getVal())
			new_costs = (calcCost(new_vals[0], dataset), calcCost(new_vals[1], dataset))
			new_gen.append(Element(new_vals[0], new_costs[0]))
			new_gen.append(Element(new_vals[1], new_costs[1]))
			for j in range(2):
				if new_costs[j] < min_cost:
					min_cost = new_costs[j]
					min_val = new_vals[j]

		#Update the population
		pop = new_gen

		gen_count += 1


	return (min_val, min_cost)
	
opt_path, opt_cost = GA()
print("Optimal path:")
for i in range(len(opt_path)):
	print(opt_path[i][0])
print("Optimal cost:", opt_cost)

fout = open("results.txt", "w")
fout.write("Optimal path (in order of visitation):\n")
for i in range(len(opt_path)):
	fout.write(str(opt_path[i][0]) + '\n')
fout.write(str(opt_path[0][0]) + '\n\n')
fout.write("Optimal cost: " + str(opt_cost))
fout.close()
