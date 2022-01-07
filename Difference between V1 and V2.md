Dear User,

<h2>Why this change?</h2>

- When other researchers apply the SOMA T3A algorithm to solve their real-world problems, their cost function is complex and takes a long time (seconds, even minutes) to complete one FEs (function evaluations).
- Therefore, parallel computation using multiple cores is necessary ("multiprocessing" in python).
- The old version (V1) was not designed for that purpose.
- Therefore, I have re-structured the algorithm so that it can be applied to parallel computation (on a PC, or a supercomputer - already tested/run on my PC Core i9-9900k 8 cores and on Karolina Cluster at https://www.it4i.cz/en Czech Republic).

<h2>What has changed?</h2>

- In V1, the cost function is calculated after each move of an individual.
- In V2, the cost function is calculated after all (selected) individuals move.
- Obviously, there is a slight performance difference between the 2 versions, but for me it is not significant (will investigate later).

The SOMA T3A code using multiprocessing in python is not show here. Please add some (simple) lines in Version 2 depending on your design.
