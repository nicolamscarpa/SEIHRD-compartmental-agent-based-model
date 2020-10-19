#!/usr/bin/env python
# coding: utf-


from functions import *
from numpy import *
network_size = 10000 #int(input("What is the network size (number of nodes)? "))
t = 300 #int(input("How long is the simulation? "))
initial_infected = 6 #int(input("How many are the initial infected? "))
beta = 0.6 #float(input("What is the infection rate? "))
mu = 0.1 #float(input("What is the recovery rate? (The inverse of the mean infection period) ")) 
ex = 0.1 #float(input("What is the exposed rate? (The inverse of the mean exposed period) ")) 
mu_r = 0.025 #float(input("What is the hospitalized-to-recovered rate? (The inverse of the mean hospitalized period for people who wille be recovered) ")) 
mu_d = 0.01 #float(input("What is the hospitalized-to-dead rate? (The inverse of the mean hospitalized period for people who will die) ")) 
d = 0.2 #float(input("What is the mortality rate?")) 
fimm = 0 #float(input("What is the immunization rate? "))
frec = 0.06 #float(input("What is recidive probability? "))

gt = create_dyn_net(network_size,t)

set_nodes_as_agents(gt,beta, mu, ex, mu_r, mu_d, d, fimm,frec)

edgelist = set_edgelist(gt)

seed, susceptible_nodes, infected_nodes, exposed_nodes, hr_nodes, hd_nodes, recovered_nodes, d_nodes, imm_nodes, rec_nodes, pos, color_map = set_graph(gt,initial_infected,network_size)

G_dyn = dynamic_graph(edgelist,gt, beta, mu, ex, mu_r, mu_d, d, fimm, frec, infected_nodes)

connected_nodes = most_connected_nodes(gt)
#list(random.randint(network_size,size=int((network_size*0.1)+0.5)))
#most_connected_nodes(gt)
#list(random.randint(network_size,size=int((network_size*0.1)+0.5)))
#

#print "The temporal network has", network_size,"nodes on day", 0
#print initial_infected,"nodes are infected on day", 0
#print "The temporal network has", len(gt[0].edges()),"edges on day", 0
#print "The degree of the initial infected is", (gt[0].degree(seed))

prevalence_size,s_size,r_size,ex_size,d_size,imm_size,h_size = run_simulation(G_dyn, t, edgelist,infected_nodes, susceptible_nodes, hr_nodes, hd_nodes,recovered_nodes,
           exposed_nodes,d_nodes,imm_nodes,rec_nodes,gt,connected_nodes,color_map,pos)
