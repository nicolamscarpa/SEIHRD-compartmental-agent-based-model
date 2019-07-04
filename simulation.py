#!/usr/bin/env python
# coding: utf-

from functions import *

network_size = int(input("What is the network size (number of nodes)? "))
t = int(input("How long is the simulation? "))
initial_infected = int(input("How many are the initial infected? "))
beta = float(input("What is the infection rate? "))
mu = float(input("What is the recovery rate? (The inverse of the mean infection period) ")) 
ex = float(input("What is the exposed rate? (The inverse of the mean exposed period) ")) 
mu_r = float(input("What is the hospitalized-to-recovered rate? (The inverse of the mean hospitalized period for people who wille be recovered) ")) 
mu_d = float(input("What is the hospitalized-to-dead rate? (The inverse of the mean hospitalized period for people who will die) ")) 
d = float(input("What is the mortality rate?")) 
fimm = float(input("What is the immunization rate? ")) 

gt = create_dyn_net(network_size,t)

set_nodes_as_agents(gt,beta, mu, ex, mu_r, mu_d, d, fimm)

edgelist = set_edgelist(gt)

seed, susceptible_nodes, infected_nodes, exposed_nodes, hr_nodes, hd_nodes, recovered_nodes, d_nodes, imm_nodes, pos, color_map = set_graph(gt,initial_infected,network_size)

G_dyn = dynamic_graph(edgelist,gt, beta, mu, ex, mu_r, mu_d, d, fimm,infected_nodes)

print "The temporal network has", network_size,"nodes on day", 0
print initial_infected,"nodes are infected on day", 0
print "The temporal network has", len(gt[0].edges()),"edges on day", 0
print "The degree of the initial infected is", (gt[0].degree(seed))

prevalence_size,s_size,r_size,ex_size,d_size,imm_size,h_size = run_simulation(G_dyn, t, edgelist,infected_nodes, susceptible_nodes, hr_nodes, hd_nodes,recovered_nodes,
           exposed_nodes,d_nodes,imm_nodes,gt,color_map,pos)
