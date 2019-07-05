# SEIHRD-compartmental-agent-based-model
This code written in Python2 simulate an SEIRD (Susceptible-Exposed-Infected-Hospitalized-Recovered or Dead) epidemic model 
with immunization process on a Scale Free network.

The network is built with the Barabási-Albert model and nodes are set as agents.

Varying the parameters of the model different epidemic scenarios can be explored and the effect of a random immunization 
process can be tested.

Each node can change is state due to a spontaneous transition which occours after a certain time or due to an 
interaction with an infected node.

All the parameters are inserted by the user at the beginning of the simulation.
The state of the nodes and epidemic progression is shown.
