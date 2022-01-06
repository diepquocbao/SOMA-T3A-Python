# --- SOMA Simple Program --- Version: SOMA T3A (V1.0) August 25, 2020 ----
# ------ Written by: Quoc Bao DIEP ---  Email: diepquocbao@gmail.com   ----
# -----------  See more details at the end of this file  ------------------
import numpy
import time
from List_of_CostFunctions import Schwefel as CostFunction

starttime = time.time()                                             # Start the timer
print('Hello! SOMA T3A is working, please wait... ')
dimension = 10                                                      # Number of dimensions of the problem
# -------------- Control Parameters of SOMA -------------------------------
N_jump = 45                                                         # Assign values ​​to variables: Step, PRT, PathLength
PopSize, Max_Migration, Max_FEs = 100, 100, dimension*10**4         # Assign values ​​to variables: PopSize, Max_Migration
m, n, k = 10, 5, 10
# -------------- The domain (search space) --------------------------------
VarMin = -500 + numpy.zeros(dimension)                              # By hand, for example: VarMin = numpy.array([-500, -501,..., -500])
VarMax = 500 + numpy.zeros(dimension)                               # Lenght of VarMin and VarMax have to equal dimension
# %%%%%%%%%%%%%%      B E G I N    S O M A    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ------------- Create the initial Population -----------------------------
VarMin = numpy.repeat(VarMin.reshape(dimension, 1),PopSize,axis=1)  # Change VarMin from vector (1 x dimension) to matrix (dimension x PopSize)
VarMax = numpy.repeat(VarMax.reshape(dimension, 1),PopSize,axis=1)  # Change VarMax from vector (1 x dimension) to matrix (dimension x PopSize)
pop = VarMin + numpy.random.rand(dimension, PopSize) * (VarMax - VarMin) # Create the initial Population
fitness = CostFunction(pop)                                         # Evaluate the initial population
FEs = PopSize                                                       # Count the number of function evaluations
the_best_cost = min(fitness)                                        # Find the Global minimum fitness value
# ---------------- SOMA MIGRATIONS ----------------------------------------
Migration = 0                                                       # Assign values ​​to variables: Migration
while FEs < Max_FEs:                                                # Terminate when reaching Max_Migration / User can change to Max_FEs
    Migration = Migration + 1                                       # Increase Migration value
    PRT = 0.05 + 0.90*(FEs/Max_FEs)                                 # Update PRT and Step parameters
    Step = 0.15 - 0.08*(FEs/Max_FEs)                                # Update PRT and Step parameters
    # ------------ Migrant selection: m -----------------------------------
    M = numpy.random.choice(range(PopSize),m,replace=False)         # Migrant selection: m
    M_sort = numpy.argsort(fitness[M])
    for j in range(n):                                              # Choose n individuals move toward the Leader
        Migrant = pop[:, M[M_sort[j]]].reshape(dimension, 1)        # Get the Migrant position (solution values) in the current population
        # ------------ Leader selection: k --------------------------------
        K = numpy.random.choice(range(PopSize),k,replace=False)     # Leader selection: k
        K_sort = numpy.argsort(fitness[K])
        Leader = pop[:, K[K_sort[1]]].reshape(dimension, 1)         # Get the Migrant position (solution values) in the current population
        if M[M_sort[j]] != K[K_sort[1]]:                            # Don't move if it is itself
            offspring_path = numpy.empty([dimension, 0])            # Create an empty path of offspring
            for move in range(N_jump):                              # From Step to PathLength: jumping
                nstep     = (move+1) * Step
                PRTVector = (numpy.random.rand(dimension,1)<PRT)*1  # If rand() < PRT, PRTVector = 1, else, 0
                offspring = Migrant + (Leader - Migrant) * nstep * PRTVector # Jumping towards the Leader
                offspring_path = numpy.append(offspring_path, offspring, axis=1) # Store the jumping path
            size = numpy.shape(offspring_path)                      # How many offspring in the path
            # ------------ Check and put individuals inside the search range if it's outside
            for cl in range(size[1]):                               # From column
                for rw in range(dimension):                         # From row: Check
                    if offspring_path[rw][cl] < VarMin[rw][0] or offspring_path[rw][cl] > VarMax[rw][0]:  # if outside the search range
                        offspring_path[rw][cl] = VarMin[rw][0] + numpy.random.rand() * (VarMax[rw][0] - VarMin[rw][0]) # Randomly put it inside
            # ------------ Evaluate the offspring and Update -------------
            new_cost = CostFunction(offspring_path)                 # Evaluate the offspring
            FEs = FEs + size[1]                                     # Count the number of function evaluations
            min_new_cost = min(new_cost)                            # Find the minimum fitness value of new_cost
            # ----- Accepting: Place the best offspring into the current population
            if min_new_cost <= fitness[M[M_sort[j]]]:               # Compare min_new_cost with fitness value of the moving individual
                idz = numpy.argmin(new_cost)                        # Find the index of minimum value in the new_cost list
                fitness[M[M_sort[j]]] = min_new_cost                # Replace the moving individual fitness value
                pop[:, M[M_sort[j]]] = offspring_path[:, idz]       # Replace the moving individual position (solution values)
                # ----- Update the global best value --------------------
                if min_new_cost <= the_best_cost:                   # Compare Current minimum fitness with Global minimum fitness
                    the_best_cost = min_new_cost                    # Update Global minimun fitness value
                    the_best_value = offspring_path[:, idz]         # Update Global minimun position
# %%%%%%%%%%%%%%%%%%    E N D    S O M A     %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
endtime = time.time()                                               # Stop the timer
caltime = endtime - starttime                                       # Caculate the processing time
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Show the information to User
print('Stop at Migration :  ', Migration)
print('The number of FEs :  ', FEs)
print('Processing time   :  ', caltime, '(s)')
print('The best cost     :  ', the_best_cost)
print('Solution values   :  ', the_best_value)
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# This algorithm is programmed according to the descriptions in the papers 
# listed below:

# Link of paper: https://ieeexplore.ieee.org/abstract/document/8790202/
# Diep, Q.B., 2019, June. Self-Organizing Migrating Algorithm Team To Team 
# Adaptive–SOMA T3A. In 2019 IEEE Congress on Evolutionary Computation (CEC)
# (pp. 1182-1187). IEEE.

# The control parameters PopSize, N_jump, m, n, and k are closely related 
# and greatly affect the performance of the algorithm. Please refer to the 
# above paper to use the correct control parameters.