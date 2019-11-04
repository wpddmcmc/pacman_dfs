# sampleAgents.py
# parsons/07-oct-2017
#
# Version 1.1
#
# Some simple agents to work with the PacMan AI projects from:
#
# http://ai.berkeley.edu/
#
# These use a simple API that allow us to control Pacman's interaction with
# the environment adding a layer on top of the AI Berkeley code.
#
# As required by the licensing agreement for the PacMan AI we have:
#
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# The agents here are extensions written by Simon Parsons, based on the code in
# pacmanAgents.py

from pacman import Directions
from game import Agent
import api
import random
import game
import util

# RandomAgent
#
# A very simple agent. Just makes a random pick every time that it is
# asked for an action.
class RandomAgent(Agent):

    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # Random choice between the legal options.
        return api.makeMove(random.choice(legal), legal)

# RandomishAgent
#
# A tiny bit more sophisticated. Having picked a direction, keep going
# until that direction is no longer possible. Then make a random
# choice.
class RandomishAgent(Agent):

    # Constructor
    #
    # Create a variable to hold the last action
    def __init__(self):
         self.last = Directions.STOP
    
    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # If we can repeat the last action, do it. Otherwise make a
        # random choice.
        if self.last in legal:
            return api.makeMove(self.last, legal)
        else:
            pick = random.choice(legal)
            # Since we changed action, record what we did
            self.last = pick
            return api.makeMove(pick, legal)

# SensingAgent
#
# Doesn't move, but reports sensory data available to Pacman
class SensingAgent(Agent):

    def getAction(self, state):

        # Demonstrates the information that Pacman can access about the state
        # of the game.

        # What are the current moves available
        legal = api.legalActions(state)
        print "Legal moves: ", legal

        # Where is Pacman?
        pacman = api.whereAmI(state)
        print "Pacman position: ", pacman

        # Where are the ghosts?
        print "Ghost positions:"
        theGhosts = api.ghosts(state)
        for i in range(len(theGhosts)):
            print theGhosts[i]

        # How far away are the ghosts?
        print "Distance to ghosts:"
        for i in range(len(theGhosts)):
            print util.manhattanDistance(pacman,theGhosts[i])

        # Where are the capsules?
        print "Capsule locations:"
        print api.capsules(state)
        
        # Where is the food?
        print "Food locations: "
        print api.food(state)

        # Where are the walls?
        print "Wall locations: "
        print api.walls(state)
        
        # getAction has to return a move. Here we pass "STOP" to the
        # API to ask Pacman to stay where they are.
        return api.makeMove(Directions.STOP, legal)

from util import Stack
class DFSAgent2(Agent):
    def __init__(self):
        self.states = Stack()
        self.detected = []
        print("DFS Pacman Runing:")

    def getAction(self, state):
        legal = api.legalActions(state)

        if Directions.STOP in legal:
            legal.remove(Directions.STOP)

        coners = api.corners(state)
        
        pacman = api.whereAmI(state)

        food = api.food(state)

        Capsules = api.capsules(state)

        ghosts = api.ghosts(state)

        if len(self.detected)==0:
            self.states.push((pacman,Directions.STOP))

        if not self.states.isEmpty():
            self.detected.append(pacman)
            success_node = []
            for directs in legal:
                if directs == Directions.WEST:
                    success_node.append((pacman[0]-1,pacman[1]))
                if directs == Directions.EAST:
                    success_node.append((pacman[0]+1,pacman[1]))
                if directs == Directions.NORTH:
                    success_node.append((pacman[0],pacman[1]+1))
                if directs == Directions.SOUTH:
                    success_node.append((pacman[0],pacman[1]-1))
            for index in range(len(success_node)):
                if not success_node[index] in self.detected and (success_node[index] in food or success_node[index] in Capsules):
                    self.states.push((success_node[index],legal[index]))
                    return (api.makeMove(legal[index], legal))

            last,acted = self.states.pop()
            if acted == Directions.NORTH:
                return (api.makeMove(Directions.SOUTH, legal))
            if acted == Directions.SOUTH:
                return (api.makeMove(Directions.NORTH, legal))
            if acted == Directions.WEST:
                return (api.makeMove(Directions.EAST, legal))
            if acted == Directions.EAST:
                return (api.makeMove(Directions.WEST, legal))

        return(api.makeMove(Directions.STOP, legal))


from util import Stack
class DFSAgent3(Agent):
    def __init__(self):
        self.states = Stack()
        self.detected = []
        self.capsulese_position = (0,0)
        self.capsulesed = False
        self.capsulesed_move = 0
        print("DFS Pacman Runing:")

    def getAction(self, state):
        legal = api.legalActions(state)

        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        
        pacman = api.whereAmI(state)

        food = api.food(state)

        Capsules = api.capsules(state)

        ghosts = api.ghosts(state)

        if not len(Capsules) == 0:
            self.capsulese_position = Capsules

        if pacman in self.capsulese_position:
            print("Eat Capsulese!")
            self.capsulesed_move = 0
            self.capsulese_position = (0,0)
            self.capsulesed = True

        if self.capsulesed == True:
            self.capsulesed_move = self.capsulesed_move+1
            if self.capsulesed_move==40:
                self.capsulesed_move = 0
                self.capsulese_position = (0,0)
                self.capsulesed=False

        if len(self.detected)==0:
            self.states.push((pacman,Directions.STOP))

        if not self.states.isEmpty():
            self.detected.append(pacman)
            moving_direction = legal
            if not len(ghosts)==0 and self.capsulesed==False:
                for ghost in ghosts:
                    for directs in moving_direction:
                        if directs == Directions.WEST and (ghost[0]-pacman[0])<0:
                            moving_direction.remove(Directions.WEST)
                        if directs == Directions.EAST and (ghost[0]-pacman[0])>0:
                            moving_direction.remove(Directions.EAST)
                        if directs == Directions.NORTH and (ghost[1]-pacman[1])>0:
                            moving_direction.remove(Directions.NORTH)
                        if directs == Directions.SOUTH and (ghost[1]-pacman[1])<0:
                            moving_direction.remove(Directions.SOUTH)

            if len(ghosts)==0 or self.capsulesed==True:
                success_node = []
                for directs in moving_direction:
                    if directs == Directions.WEST:
                        success_node.append((pacman[0]-1,pacman[1]))
                    if directs == Directions.EAST:
                        success_node.append((pacman[0]+1,pacman[1]))
                    if directs == Directions.NORTH:
                        success_node.append((pacman[0],pacman[1]+1))
                    if directs == Directions.SOUTH:
                        success_node.append((pacman[0],pacman[1]-1))
                for index in range(len(success_node)):
                    if self.detected and (success_node[index] in food or success_node[index] in Capsules):
                        self.states.push((success_node[index],moving_direction[index]))
                        if not len(ghosts)==0:
                            for ghost in ghosts:
                                if pacman[0] == ghost[0]:
                                    if abs(success_node[index][1]-ghost[1])<=1:
                                        print("Eat ghost")
                                        self.capsulesed_move = 0
                                        self.capsulese_position = (0,0)
                                        self.capsulesed=False
                                if pacman[1] == ghost[1]:
                                    if abs(success_node[index][0]-ghost[0])<=1:
                                        print("Eat ghost")
                                        self.capsulesed_move = 0
                                        self.capsulese_position = (0,0)
                                        self.capsulesed=False
                        return (api.makeMove(moving_direction[index], moving_direction))

                last,acted = self.states.pop()
                if acted == Directions.NORTH:
                    return (api.makeMove(Directions.SOUTH, moving_direction))
                if acted == Directions.SOUTH:
                    return (api.makeMove(Directions.NORTH, moving_direction))
                if acted == Directions.WEST:
                    return (api.makeMove(Directions.EAST, moving_direction))
                if acted == Directions.EAST:
                    return (api.makeMove(Directions.WEST, moving_direction))
            else:
                if not len(moving_direction)==0:
                    run_away = random.choice(moving_direction)
                    run_point = pacman
                    if run_away == Directions.WEST:
                        run_point=((run_point[0]-1,run_point[1]))
                    if run_away == Directions.EAST:
                        run_point=((run_point[0]+1,run_point[1]))
                    if run_away == Directions.NORTH:
                        run_point=((run_point[0],run_point[1]+1))
                    if run_away == Directions.SOUTH:
                        run_point=((run_point[0],run_point[1]-1))
                    self.states.push((run_point,run_away))
                    return api.makeMove(run_away, moving_direction)
                else:
                    if(len(ghosts)==2):
                        distance1 = 0
                        distance2 = 0
                        run_away = Directions.STOP
                        run_point = pacman
                        for ghost in ghosts:
                            if pacman[0] == ghost[0]:
                                distance_temp = pacman[1]-ghost[1]
                                if abs(distance_temp)>distance1:
                                    distance1 = distance_temp
                            if pacman[1] == ghost[1]:
                                distance_temp = pacman[0]-ghost[0]
                                if abs(distance_temp)>distance2:
                                    distance2 = distance_temp
                        if abs(distance1)>= abs(distance2):
                            if distance1>=0:
                                run_away = Directions.SOUTH
                                run_point=((run_point[0],run_point[1]-1))
                            else:
                                run_away = Directions.NORTH
                                run_point=((run_point[0],run_point[1]+1))
                        else:
                            if distance2>=0:
                                run_away = Directions.WEST
                                run_point=((run_point[0]-1,run_point[1]))
                            else:
                                run_away = Directions.EAST
                                run_point=((run_point[0]+1,run_point[1]))
                        self.states.push((run_point,run_away))
                        return(api.makeMove(run_away, legal))
        return(api.makeMove(Directions.STOP, legal))