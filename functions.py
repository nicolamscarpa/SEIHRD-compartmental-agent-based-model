#!/usr/bin/env python
# coding: utf-8

def create_dyn_net(n,t):
    """Creates as many configurations of Barbasi-Albert network as timesteps
    and a dictionary in which assigns to each node an agent"""
    import networkx as nx
    gt = []
    for i in range(t):
        gt.append(nx.barabasi_albert_graph(n,1))
    for i in range(t):
        gt[i].agent = {}
    return(gt)

def set_nodes_as_agents(gt,beta,mu,ex,mu_r,mu_d,d,fimm):
    """Assigns to each agent(node of the network) an instance of the class "People" """
    from agents import people
    for j in range(len(gt)):
        gt[j].agent={}    
        for i in gt[j].nodes():
            gt[j].agent[i]=people(beta,mu,ex,mu_r,mu_d,d,fimm)

def set_edgelist(gt):
    """Creates a dictionary with all the links of each network configuration,
    to insert at each run the appropriate links """
    from collections import defaultdict
    edgelist=defaultdict(list)
    for i in range(len(gt)):
        edgelist[i].append(gt[i].edges())
    return(edgelist)


def set_graph(gt,initial_infected,network_size):
    """Creates the lists(compartments) for the compartmental model and two lists 
    for nodes color and position"""
    import random
    seed = random.sample(list(gt[0]), initial_infected)
    susceptible_nodes = []
    infected_nodes=seed
    exposed_nodes = []
    hr_nodes = []
    hd_nodes = []
    recovered_nodes = []
    d_nodes = []
    imm_nodes= []
    pos = []
    color_map = []
    for i in range(network_size):
        if i in infected_nodes:
            color_map.append('red') 
        else:
            color_map.append('blue')
    for i in range(1000):
        pos.append((random.randrange(0, 1000), random.randrange(0, 1000)))
    return(seed, susceptible_nodes, infected_nodes, exposed_nodes, hr_nodes, hd_nodes, recovered_nodes, d_nodes, imm_nodes, pos, color_map)


def dynamic_graph(edgelist,gt,beta,mu,ex,mu_r,mu_d,d,fimm,infected_nodes):
    """Creates a graph with all the nodes of the simulation in which 
    at each run inserts the related links from edgelist"""
    from agents import people
    import networkx as nx
    import random
    G_dyn=nx.Graph()
    G_dyn.agent = {} 
    G_dyn.add_edges_from(edgelist[0][0]) #inizializzo la rete dinamica con la prima configurazione
    G_dyn.add_nodes_from(list(gt[0].nodes()))
    for i in G_dyn.nodes():
        G_dyn.agent[i]=people(beta,mu,ex,mu_r,mu_d,d,fimm)
    for n in G_dyn.nodes():
        if n in infected_nodes:
            G_dyn.agent[n].state='i'
            #infected
        else:
            G_dyn.agent[n].state='s'
            #susceptible
    return(G_dyn)


def update_compartments(network,imm_nodes,d_nodes,recovered_nodes):
    """Updates compartmental model lists"""
    infected_nodes=[]
    susceptible_nodes = []
    hr_nodes = []
    hd_nodes = []
    exposed_nodes = []
    for n in network.nodes():
        if network.agent[n].state=='i':
            infected_nodes.append(n)
            
        if network.agent[n].state=='s':
               susceptible_nodes.append(n)
            
        if network.agent[n].state=='h_r':
            hr_nodes.append(n)
            
        if network.agent[n].state=='h_d':
            hd_nodes.append(n)
            
        if network.agent[n].state=='r':
            if n not in recovered_nodes:
                recovered_nodes.append(n)
            
        if network.agent[n].state=='e':
            exposed_nodes.append(n)
            
        if network.agent[n].state=='d':
            if n not in d_nodes:
                d_nodes.append(n) 
            
        if network.agent[n].state=='imm':
            if n not in imm_nodes:
                imm_nodes.append(n) 
            
    return(infected_nodes, susceptible_nodes, hr_nodes, hd_nodes,recovered_nodes,
           exposed_nodes,d_nodes,imm_nodes)


def run_simulation(G_dyn, t, edgelist,infected_nodes, susceptible_nodes, hr_nodes, hd_nodes,recovered_nodes,
           exposed_nodes,d_nodes,imm_nodes,gt,color_map,pos):
    
    """Run the simluation of the compartmental model"""
    
    import matplotlib
    import pandas as pd
    import random
    from matplotlib import pyplot as plt
    import networkx as nx
    from IPython.display import clear_output
    import random
    
    #initial infection size
    prevalence_size = [float(len(infected_nodes))/float(len(G_dyn.nodes()))]
    s_size = [float(len(G_dyn.nodes())-len(infected_nodes))/float(len(G_dyn.nodes()))]
    r_size = [float(len(recovered_nodes))/float(len(gt[0]))]
    ex_size = [float(len(exposed_nodes))/float(len(gt[0]))]
    d_size = [float(len(d_nodes))/float(len(gt[0]))]
    imm_size = [float(len(imm_nodes))/float(len(gt[0]))]
    h_size = [float(len(hr_nodes+d_nodes))/float(len(gt[0]))]
    fig, axs = plt.subplots(1, 2,figsize=(15,5))
    print("setting simulation...")
    axs[1] = nx.draw(gt[0], pos, node_color = color_map, edge_color = 'grey', node_size = 150)
    plt.pause(10)
    clear_output(wait=True)

    
    #Infection rate changes during simulation(al 30%,60% ed 80%)
    for time in range(t):
    
        if time > int(t*0.3):
            for i in range(len(G_dyn)):
                if G_dyn.agent[i].state == 'h_d':
                    G_dyn.agent[i].beta = G_dyn.agent[i].beta*0.7*0.8
                if G_dyn.agent[i].state == 'h_r':
                    G_dyn.agent[i].beta = G_dyn.agent[i].beta*0.7*0.8
                else:
                    G_dyn.agent[i].beta = G_dyn.agent[i].beta*0.8
    
        if time > int(t*0.6):
            for i in range(len(G_dyn)):
                if G_dyn.agent[i].state == 'h_d':
                    G_dyn.agent[i].beta = G_dyn.agent[i].beta*0.7*0.7
                if G_dyn.agent[i].state == 'h_r':
                    G_dyn.agent[i].beta = G_dyn.agent[i].beta*0.7*0.7
                else:
                    G_dyn.agent[i].beta = G_dyn.agent[i].beta*0.7
    
        if time > int(t*0.8):
            for i in range(len(G_dyn)):
                if G_dyn.agent[i].state == 'h_d':
                    G_dyn.agent[i].beta = G_dyn.agent[i].beta*0.7*0.5
                if G_dyn.agent[i].state == 'h_r':
                    G_dyn.agent[i].beta = G_dyn.agent[i].beta*0.7*0.5
                else:
                    G_dyn.agent[i].beta = G_dyn.agent[i].beta*0.5
    
        #Links are added at ech step
        links=edgelist[time]#these are the links active on day t    
        if time > 0:
            G_dyn.add_edges_from(links[0])
            for e in links[0]:
                if e[0] not in G_dyn.agent:
                    G_dyn.agent[e[0]].state='s'
                if e[1] not in G_dyn.agent: 
                    G_dyn.agent[e[1]].state='s'
                
            
        #random immunization process:
        for i in G_dyn.nodes:
            if G_dyn.agent[i].state=='s':
                G_dyn.agent[i].susceptible_immunized()
        
        #infection propagation by infected 
        for i in infected_nodes:
            for j in G_dyn.neighbors(i):
                if G_dyn.agent[j].state=='s':
                    G_dyn.agent[j].susceptible_exposed()
            #infected->hospetalized_r
            G_dyn.agent[i].infected_hospetalized_r()
    
        #infected->hodpetalized_d
        for i in infected_nodes:
            G_dyn.agent[i].infected_hospetalized_d()
        
        #infection propagation by hospetalized            
        for i in (hr_nodes+hd_nodes):
            for j in G_dyn.neighbors(i):
                if G_dyn.agent[j].state=='s':
                    G_dyn.agent[j].susceptible_exposed()
        #exposed->infected
        for k in exposed_nodes:
            G_dyn.agent[k].exposed_infected()
        
        #hospetalize->recovered
        for x in (hr_nodes):
            G_dyn.agent[x].hospetalized_recovered()
        
        #hospetalized->dead            
        for x in (hd_nodes):   
            G_dyn.agent[x].hospetalized_dead()
       
        #updates compartments
    
        infected_nodes, susceptible_nodes, hr_nodes, hd_nodes,recovered_nodes,exposed_nodes,d_nodes,imm_nodes = update_compartments(G_dyn,imm_nodes,d_nodes,recovered_nodes)
        
        for i in recovered_nodes:
            color_map[i] = 'yellow'
        
        for i in infected_nodes:
            color_map[i] = 'red'
        
        for i in d_nodes:
            color_map[i] = 'black'
        
        for i in imm_nodes:
            color_map[i] = 'violet'
            
        for i in (hr_nodes+hd_nodes):
            color_map[i] = 'green'
            
        for i in exposed_nodes:
            color_map[i] = 'orange'
        
        perc = str(((time+1)/float(t))*100)
        
        fig, axs = plt.subplots(1, 2,figsize=(15,5))
        axs[1] = nx.draw(G_dyn, pos, node_color = color_map, edge_color = 'grey', node_size = 150)
            
        axs[0].plot(s_size, color = 'blue', label="Fraction of susceptible people")
        axs[0].plot(prevalence_size, 'r', label="Prevalence")
        axs[0].plot(r_size, 'y', label="Fraction of recovered people")
        axs[0].plot(d_size, 'k', label="Fraction of dead people")
        axs[0].plot(h_size, color = 'green', label="Fraction of hospitalized people")
        axs[0].plot(imm_size, color = 'violet', label="Fraction of immunized people")
        axs[0].plot(ex_size, color = 'orange', label="Fraction of exposed people")
        axs[0].title.set_text(perc+"%")
        axs[0].legend()
        
        
        plt.pause(0.0005)
        if time != (t-1):
            clear_output(wait=True)
    
        #remove edges to update the network at next step
        G_dyn.remove_edges_from(list(links[0]))
    
        #update size of infection
        prevalence_size.append(float(len(infected_nodes))/float(len(gt[0])))
        s_size.append(float(len(susceptible_nodes))/float(len(gt[0])))
        r_size.append(float(len(recovered_nodes))/float(len(gt[0])))
        ex_size.append(float(len(exposed_nodes))/float(len(gt[0])))
        d_size.append(float(len(d_nodes))/float(len(gt[0])))
        imm_size.append(float(len(imm_nodes))/float(len(gt[0])))
        h_size.append(float(len(hr_nodes+hd_nodes))/float(len(gt[0])))
       
    if ((len(exposed_nodes) != 0) | (len(hr_nodes+hd_nodes) != 0) | (len(infected_nodes) != 0)):
        print 'More time is needed to get the epidemic equilibrium'
    
    if len(exposed_nodes) != 0:
        print 'There are still ', len(exposed_nodes), ' exposed people'
        
    if len(hr_nodes+hd_nodes) != 0:
        print 'There are still ', len(hr_nodes+hd_nodes), ' hospitalized people'
        
    if len(infected_nodes) != 0:
        print 'There are still ', len(infected_nodes), ' infected people'
    return(prevalence_size,s_size,r_size,ex_size,d_size,imm_size,h_size)
