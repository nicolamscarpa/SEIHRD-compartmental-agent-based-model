#!/usr/bin/env python
# coding: utf-8

class people:
    """This calss defines the agents involved in the simulations and contains
    the functions that generates transitions between compartments, generating 
    a random number and comparing it with the rate of the related transition"""
    
    def __init__(self,beta,mu,ex,mu_r,mu_d,d,fimm):
        self.beta = beta
        self.mu = mu
        self.ex = ex
        self.mu_r = mu_r
        self.mu_d = mu_d
        self.d = d
        self.fimm = fimm
        self.state = 's' #susceptible
     
    def susceptible_exposed(self):
        import random
        if random.random() < self.beta:
            if self.state == 's':
                self.state = 'e' #exposed
    
    def exposed_infected(self):
        import random
        if random.random() < self.ex:
            if self.state == 'e':
                self.state = 'i'    #infected
    
    def infected_hospetalized_r(self):
        import random
        if random.random() < ((1-self.d)*self.mu):
            if self.state == 'i':
                self.state = 'h_r' #hospitalized(destined to recovering)
                self.beta = self.beta*0.7
                
    def infected_hospetalized_d(self):
        import random
        if random.random() < ((self.d)*self.mu):
            if self.state == 'i':
                self.state = 'h_d' #hospitalized(destined to death)
                self.beta = self.beta*0.7
                
    def hospetalized_recovered(self):
        import random
        if random.random() < self.mu_r:
            if self.state == 'h_r':
                self.state = 'r' #recovered
                
    def hospetalized_dead(self):
        import random
        if random.random() < self.mu_d:
            if self.state == 'h_d':
                self.state = 'd' #dead
    
    def susceptible_immunized(self):
        import random
        if random.random() < self.fimm/float(10):
            if self.state == 's':
                self.state = 'imm'
