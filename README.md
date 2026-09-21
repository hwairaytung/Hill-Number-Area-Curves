# Hill-Number-Area-Curves
Code for https://arxiv.org/abs/2609.02365

crw_simulation_python.py samples from the stationary distribution and outputs a list of lists indicating which sites in the [0, N)^2 box belong to the same species. The output should look like [[x_1, x_2, ...], [y_1, y_2, ...], ....], and each inner list corresponds to sites with the same species (eg x_1, x_2, etc belong to the same species and y_1, y_2, etc belong to another). Each value in the list is an integer that is converted to a site by the map x->(x%N, x//N) where % is mod and // is integer division.

CRW_simulate.cpp was generated using AI and translates crw_simulation_python from python to C++. This runs significantly faster. No functionality is added.
