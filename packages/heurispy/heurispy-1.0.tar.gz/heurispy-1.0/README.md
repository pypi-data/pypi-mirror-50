HeurisPy
======

``HeurisPy`` is an object oriented framework developed in Python. Its objective is to help the user to obtain experience in the use of local search heuristics (l.s.h.) in 
discrete optimization problems (d.o.p.).

``HeurisPy`` has been desinged with the next principles in mind:

--It needs to be general enough to allow the definition of various discrete optimization problems.

--It needs to be accesible to users with low experiencie in the use of local search heuristics and programming.

--It needs to contain various local search heuristics available to use, and a general class to add new heuristics.

--It needs parallel processing to speed up the procces and tools to ease the statistical analysis.

It's expected that the user only needs to program its discrete optimization problem and choose the heuristics to run. ``HeurisPy`` will handle the heuristic searchs and get the
info needed for the user to make an informed decision.

``HeurisPy`` is programmed in Python 3.7, that can be downloaded [here](https://www.python.org/downloads/) and uses these external libraries:

--**numpy**: Cientific computing library. [Homepage](https://www.numpy.org/)

--**pathos**: Parallel processing library. [Homepage](https://pypi.org/project/pathos/)

--**pandas**: Data analysis library. [Homepage](https://pandas.pydata.org/)

--**pyFPDF**: PDF files library. [Homepage](https://pyfpdf.readthedocs.io/en/latest/)

--**PyPDF2**: A PDF toolkit. [Homepage](https://pypi.org/project/PyPDF2/)

--**matplotlib**: Plotting library. [Homepage](https://matplotlib.org/)

--**tqdm**: Progress bar library. [Homepage](https://tqdm.github.io/)

Installation
======

``HeurisPy`` is available as a library in PyPI and can be installed using the command:

	pip install heurispy
	
To verify the installation, run one of the examples scripts, like "coloracion_grafo_recsim.py" in the route /heurispy/ejemplos/. 

License
======

 Copyright 2019, LANIA, A.C.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

How does it work
======

``HeurisPy`` has three main classes that need the user to work properly:

--**Problema**: Handles the d.o.p. programmed by the user.

--**Heuristica**: Recieves attributes to do the heuristic exploration with defined user parameters.

--**Framework**: Directs all the internal processes, like the parallel processing, the data recollection and the method calls for the file generator.

Defining the d.o.p.
======

First we need to define the d.o.p. on ``HeurisPy``. To do this, we have to create:

--A method for the creation of new solutions.

--A method that changes an existing solution.

--The objective function to minimize.

For example, in the coloring graph problem, we assign colors to the nodes, trying to minimize the number of colors used without having repeated adyaent colors. The graph is
represented in ``HeurisPy`` with a dictionary. A dictionary is a set of values that have labels named "keys". So:

	adyacencies_in_graph = {"0": [1, 4, 6],
							"1": [0, 2, 7],
							"2": [1, 3, 8],
							"3": [2, 4, 9],
							"4": [0, 3, 5],
							"5": [4, 7, 8],
							"6": [0, 8, 9],
							"7": [1, 5, 9],
							"8": [2, 5, 6],
							"9": [3, 6, 7]}
							
	nodes_amount = len(adyacencies_in_graph)
	
The elements between the " " are the nodes, and the lists are their adyacent nodes. Plus, the length of the dictionary determines the amount of nodes.

To create a solution, we assing to each node a random color (represented with an integer). This can be defined as follows:

	import random

	def create_solution():
		new_solution = []
		for index in range(nodes_amount):
			new_solution.append(random.randint(0, nodes_amount - 1))
		return new_solution
	
The new solution is a list in which the indexes represent the node, and the index value is the color assigned. To change a solution, we chose a random edge in the solution, verify
the color of the adyacent nodes, and chose a different color to all of them. The adyacent colors are obtained with:

	def get_adyacent_colors(solution, node):
		nodes = adyacencies_in_graph[str(node)]
		adyacent_colors = []
		for current_node in nodes:
			adyacent_colors.append(solution[current_node])
		return adyacent_colors
		
And we change the solution with:

	def change_solution(solution):
		new_solution = solution.copy()
		length_solution = len(new_solution)
		node_to_change = random.randint(0, length_solution - 1)
		colors = list(range(nodes_amount))
		adyacent_colors = get_adyacent_colors(new_solution, node_to_change)
		available_colors = [color for color in colors if color not in adyacent_colors]
		new_solution[node_to_change] = random.choice(available_colors)
		return new_solution
		
The objective function checks the amount of different colors in a solution, and how many nodes have repeated adyacent colors. This is made as follows:

	def cost_different_colors(solution):
		different_colors = set(solution)
		return len(different_colors)
		
	def cost_adyacent_colors(solution):
		final_value = 0
		length_solution = len(solution)
		for index in range(length_solution)
			color = solution[index]
			adyacent_colors = get_adyacent_colors(solution, index)
			repeated = adyacent_colors.count(color)
			final_value = final_value + repeated
		return final_value
		
We add weights to each cost to allow the tuning of the objective function, and we define it:

	c_1 = 1
	c_2 = 1
	
	def objective_function(solution):
		color_cost = cost_different_colors(solution)
		adyacent_cost = cost_adyacent_colors(solution)
		return c_1*color_cost + c_2*adyacent_cost
		
Now, we need to create an instance of the Problema class, made as:

	from heurispy.problema import Problema
	
	coloration_problem = Problema(dominio=create_solution, funcion_objetivo=objective_function, varia_soluciones=change_solution)
	
This example is implemented in spanish in the scripy problema_coloracion_grafo.py in the /heurispy/ejemplos/ route.

Preparing a heuristic for its use
======

Every heuristic implemented in ``HeurisPy`` is a child class of Heuristica. To use them, we only need to import the correspondent class, assing it a Problema instance, and define
some general parameters. For example, to use tabu search, we do as follows:

	from heurispy.heuristicas.busqueda_tabu import BusquedaTabu
	
	tabu_search = BusquedaTabu(coloration_problem, max_iteraciones=100000)
	
Howerer, we still need to define specific heuristic parameters for ``HeurisPy`` to work.

Defining heuristic parameters
======

To define the specific heuristic parameters, we need to create a dictionary. For tabu search:

	tabu_search_parameters = dict(espacio_memoria=[50, 100, 150], max_busquedas_sin_mejoras=[100])
	
This dictionary is the base that ``HeurisPy`` needs to do the exploration. In this case, we have three block parameters:

-Memory Space = 50, Max Search Without Improvement = 100 (MS=50, MSWI=100)

-Memory Space = 100, Max Search Without Improvement = 100 (MS=100, MSWI=100)

-Memory Space = 150, Max Search Without Improvement = 100 (MS=150, MSWI=100)

Every value in the dictionary has to be a list with all the expected values of each parameter. The next step is to define the repetitions of every parameter block.

Determing repetitions
======

To determine the repetitions, we use the next method:

	from heurispy.framework import genera_bloque_parametros

	executions_list = genera_bloque_parametros(tabu_search_parameters, repeticiones=10)
	
With this, 30 executions are made: 10 for the MS=50, MSWI=100, 10 for MS=10, MSWI=100, and 10 for MS=150, MSWI=100.

Having the heuristic and the total executions, we can start the final ``HeurisPy`` process.

Starting the heuristic exploration
======

The inicia_exploracion_heuristica method starts the exploration:

	from heurispy.framework import inicia_exploracion_heuristica
	
	inicia_exploracion_heuristica(tabu_search, executions_list)
	
We can define the amount of cores used in the search with the nucleos_cpu parameter. By default, it uses all the cpu cores.

With the search initiated, ``HeurisPy`` shows a progress bar that counts the finalized executions, throws information of the progress and the files created as results.

Checking the files
======

With the exploration finisted, two folders are created: "Resultados", that stores the statistics and plots generated by the heuristic exploration, and "Informacion", that contains the
data and advanced information. In "Results", a folder is created with the name of the heuristic used, and inside of it there's a folder with the explorations done. Its name is the
date and hour in which the exploration was done. For example, if the example was executed in July 4to, 2019 at 12:31 pm, then it is stored in the folder "2019-07-04---12-31".
Inside this folder is a pdf file, which name contains the used heuristic, the corresponding parameter block, and the date and hour in which the file was created. The information
shown in this PDF file shows particular information of the heuristic used, so the information inside can vary.

Because the performance of the heuristic is very dependant of the used parameters and the discrete optimization problem, there's no rule that determines the ideal combination
between heuristic and parameters used, so it is advised to test the d.o.p. with various heuristics and varios sets of parameters, trying to diversify the executions and getting
the mayor amount of available information, to try and search for consistency in the results.



	