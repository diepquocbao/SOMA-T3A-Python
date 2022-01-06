# --- SOMA Simple Program --- Version: SOMA T3A (V2.0) January 06, 2022 ---
# ------ Written by: Quoc Bao DIEP ---  Email: diepquocbao@gmail.com   ----
# -----------  See more details at the end of this file  ------------------
import numpy
import time
from List_of_CostFunctions import Schwefel as CostFunction

starttime = time.time()
print('Hello! SOMA T3A is working, please wait... ')
Dim = 10
# -------------- Control Parameters of SOMA -------------------------------
N_jump = 45
NP, Max_Mig, Max_FEs = 100, 100, Dim*10**4
m, n, k = 10, 5, 15
# -------------- The domain (search space) --------------------------------
VarMin = -500 + numpy.zeros(Dim)
VarMax = 500 + numpy.zeros(Dim)
# %%%%%%%%%%%%%%      B E G I N    S O M A    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ------------- Create the initial Population -----------------------------
VarMin = numpy.repeat(VarMin.reshape(Dim, 1),NP,axis=1)
VarMax = numpy.repeat(VarMax.reshape(Dim, 1),NP,axis=1)
pop = VarMin + numpy.random.rand(Dim, NP) * (VarMax - VarMin)
fit = CostFunction(pop)
FEs = NP
best_fit = min(fit)
id = numpy.argmin(fit)
best_val = pop[:, id]
# ---------------- SOMA MIGRATIONS ----------------------------------------
Mig = 0
while FEs < Max_FEs:
    Mig = Mig + 1
    # ------------ Migrant selection: m -----------------------------------
    M = numpy.random.choice(range(NP),m,replace=False)
    M_sort = numpy.argsort(fit[M])
    newpop = numpy.zeros((Dim,n*N_jump))
    for j in range(n):
        Migrant = pop[:, M[M_sort[j]]].reshape(Dim, 1)
        # ------------ Leader selection: k --------------------------------
        K = numpy.random.choice(range(NP),k,replace=False)
        K_sort = numpy.argsort(fit[K])
        Leader = pop[:, K[K_sort[0]]].reshape(Dim, 1)
        if M[M_sort[j]] == K[K_sort[0]]:
            Leader = pop[:, K[K_sort[1]]].reshape(Dim, 1)
        PRT = 0.05 + 0.90*(FEs/Max_FEs)
        Step = 0.15 - 0.08*(FEs/Max_FEs)
        nstep = numpy.arange(0,N_jump)*Step+Step
        PRTVector = (numpy.random.rand(Dim, N_jump) < PRT) * 1
        indi_new = Migrant + (Leader - Migrant) * nstep * PRTVector
        # ------------ Check and put individuals inside the search range if it's outside
        for cl in range(N_jump):
            for rw in range(Dim):
                if indi_new[rw,cl] < VarMin[rw,0] or indi_new[rw,cl] > VarMax[rw,0]:
                    indi_new[rw,cl] = VarMin[rw,0] + numpy.random.rand() * (VarMax[rw,0] - VarMin[rw,0])
        newpop[:,N_jump*j:N_jump*(j+1)] = indi_new
    # ------------ Evaluate the offspring and Update -------------
    newfitpop = CostFunction(newpop)
    FEs = FEs + n*N_jump
    for j in range(n):
        newfit = newfitpop[N_jump*j:N_jump*(j+1)]
        min_newfit = min(newfit)
        # ----- Accepting: Place the best offspring into the current population
        if min_newfit <= fit[M[M_sort[j]]]:
            fit[M[M_sort[j]]] = min_newfit
            id = numpy.argmin(newfit)
            pop[:, M[M_sort[j]]] = newpop[:, (N_jump*j)+id]
            # ----- Update the global best value --------------------
            if min_newfit < best_fit:
                best_fit = min_newfit
                best_val = newpop[:, (N_jump*j)+id]
# %%%%%%%%%%%%%%%%%%    E N D    S O M A     %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
endtime = time.time()
caltime = endtime - starttime
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Show the information to User
print('Stop at Migration :  ', Mig)
print('The number of FEs :  ', FEs)
print('Processing time   :  ', caltime, '(s)')
print('The best cost     :  ', best_fit)
print('Solution values   :  ', best_val)
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

"""
This algorithm is programmed according to the descriptions in the papers 
listed below:

Link of paper: https://ieeexplore.ieee.org/abstract/document/8790202/
Diep, Q.B., 2019, June. Self-Organizing Migrating Algorithm Team To Team 
Adaptive–SOMA T3A. In 2019 IEEE Congress on Evolutionary Computation (CEC)
(pp. 1182-1187). IEEE.

The control parameters PopSize, N_jump, m, n, and k are closely related 
and greatly affect the performance of the algorithm. Please refer to the 
above paper to use the correct control parameters.
"""