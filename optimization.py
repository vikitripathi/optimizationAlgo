# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 23:11:26 2014

@author: Abhishek Dutt
"""

import time
import random
import math

#list containing people and their location 
people=[('Seymour','BOS'),
        ('Franny','DAL'),
        ('Zooey','CAK'),
        ('Walt','MIA'),
        ('Buddy','ORD'),
        ('Les','OMA')]
        
#to access 'Seymour' use people[0][0]  and for 'BOS' use people[0][1]  as these are lists        
        
# LaGuardia airport in New York
destination='LGA'

"""
The family members are from all over the country and wish to meet up in New York.
They will all arrive on the same day and leave on the same day, and they would like
to share transportation to and from the airport. There are dozens of flights per day to
New York from any of the family members’ locations, all leaving at different times.
The flights also vary in price and in duration.
"""

#a sample file of flight data from http://kiwitobes.com/optimize/
#schedule.txt
#This file contains origin, destination, departure time, arrival time, and price for a set
#of flights in a comma-separated format

flights={}
#a dictionary with key as origin and dest and values the other remaining flight data


for line in file('schedule.txt'):
    origin,dest,depart,arrive,price=line.strip( ).split(',')
    flights.setdefault((origin,dest),[])
    # Add details to the list of possible flights
    flights[(origin,dest)].append((depart,arrive,int(price)))
    
#calculates how many minutes into the day a given time is
#makes it easy to calculate flight times and waiting times    
def getminutes(t):
    x=time.strptime(t,'%H:%M')
    return x[3]*60+x[4]    
    
"""
The challenge now is to decide which flight each person in the family should take. Of
course, keeping total price down is a goal, but there are many other possible factors
that the optimal solution will take into account and try to minimize, such as total
waiting time at the airport or total flight time
"""

"""
it’s important to choose a
simple representation that’s not specific to the group travel problem. A very common
representation is a list of numbers. 
"""
#each number can represent which flight a person chooses to take, where 0 is the first flight
# of the day, 1 is the second,and so on    
#Since each person needs an outbound flight and a return flight, the length
#of this list is twice the number of people.

"""
 the list:
[1,4,3,2,7,3,6,3,2,4,5,3]
Represents a solution in which Seymour takes the second flight of the day from Boston to 
New York, and the fifth flight back to Boston on the day he returns.
"""


def printschedule(r):
    for d in range(len(r)/2):
        name=people[d][0]
        origin=people[d][1]
        out=flights[(origin,destination)][int(r[d])]
        ret=flights[(destination,origin)][int(r[d+1])]
        print '%10s%10s %5s-%5s $%3s %5s-%5s $%3s' % (name,origin,
                                                      out[0],out[1],out[2],
                                                      ret[0],ret[1],ret[2])
                                                      

#cost function
"""
The goal of any optimization algorithm is
to find a set of inputs—flights, in this case—that minimizes the cost function, so the
cost function has to return a value that represents how bad a solution is. There is no
particular scale forbadness; the only requirement is that the function returns larger
values for worse solutions
"""
#After choosing some variables that impose costs, you’ll need to determine how to
#combine them into a single number.
"""
There are a huge number of possibilities for the getcost function defined here. This
function takes into account the total cost of the trip and the total time spent waiting
at airports for the various members of the family. It also adds a penalty of $50 if the
car is returned at a later time of the day than when it was rented
"""

def schedulecost(sol):
    totalprice=0
    latestarrival=0
    earliestdep=24*60 #to charge extra 50 for a extra day of car , time in minutes
    
    for d in range(len(sol)/2):
        # Get the inbound and outbound flights
        origin=people[d][1]
        outbound=flights[(origin,destination)][int(sol[d])]
        returnf=flights[(destination,origin)][int(sol[d+1])]

        # Total price is the price of all outbound and return flights
        totalprice+=outbound[2]
        totalprice+=returnf[2]

        # Track the latest arrival and earliest departure
        if latestarrival < getminutes(outbound[1]): latestarrival=getminutes(outbound[1])
        if earliestdep > getminutes(returnf[0]): earliestdep=getminutes(returnf[0])

    # Every person must wait at the airport until the latest person arrives.
    # They also must arrive at the same time and wait for their flights.
    totalwait=0
    for d in range(len(sol)/2):            
            origin=people[d][1]
            outbound=flights[(origin,destination)][int(sol[d])]
            returnf=flights[(destination,origin)][int(sol[d+1])]
            totalwait+=latestarrival-getminutes(outbound[1])
            totalwait+=getminutes(returnf[0])-earliestdep 

    # Does this solution require an extra day of car rental? That'll be $50!
    if latestarrival > earliestdep: totalprice+=50
    return totalprice+totalwait
"""
right now, the total wait time assumes that all the family
members will leave the airport together when the last person arrives, and will all go
to the airport for the earliest departure
"""


#random searching
def randomoptimize(domain,costf):
    best=999999999
    bestr=None
    for i in range(1000):
        # Create a random solution
        r=[random.randint(domain[i][0],domain[i][1])
           for i in range(len(domain))]
        # Get the cost
        cost=costf(r)  
        # Compare it to the best one so far
        if cost<best:
            best=cost
            bestr=r 
            
    return r  



      
        

                                                      

    
    