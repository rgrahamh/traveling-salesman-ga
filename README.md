# Traveling Salesman Genetic Algorithm
This was basically our Machine Learning final; we had to implement a genetic algorithm to come close to a solution to the Traveling Salesman problem. This saw moderate success as it got within 3,000 units of the actual calculated shortest path, and could probably be dialed in further if one were to figure out what the optimal set of parameters are.

------------

The write-up I gave alongside this project was:

The official best path:
27,603 (units?)

My found path:
30,447.0155940894 (units?)

Visiting order:
6
8
13
15
23
26
24
19
25
27
28
22
21
20
16
17
18
14
12
2
3
4
0
1
5
9
10
11
7
6

(Cities are zero indexed rather than one; just add one to the numbers pre-print if you'd prefer one indexing like the input)

I'd guess that the reason my solution is so far off is because I didn't get a good chance to dial in the crossover/mutation parameters (I thought we were doing the Swiss version (which was taking a REALLY long time on my computer due to ensuring that the crossover resulted in a valid path) until I double checked the assignment). I also think my mutation methodology, while good for the first genetic algorithm problem, doesn't scale very well with an increasing number of cities (since it only swaps two cities, it makes a smaller and smaller overall impact as the number of cities grows). I also was only able to do 500,000 generations before calling it (since I had a very short amount of time before the deadline). If I could dial in the parameters for my genetic algorithm, I'm decently confident I could get the shortest path.
