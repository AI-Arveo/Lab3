# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        self.qvalue = util.Counter()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        if not action:
            return 0.0
        return self.qvalue[state, action]

    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        maxLegal = self.getLegalActions(state)
        if not maxLegal:
            return 0.0
        maxQValue = -math.inf
        for maxAction in maxLegal:
            if self.getQValue(state, maxAction) > maxQValue:
                maxQValue = self.getQValue(state, maxAction)

        return maxQValue

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"

        if state == "TERMINAL_STATE":
            return None

        maxValue = -math.inf
        bestAction = []

        # Iterate through possible actions
        for action in self.getLegalActions(state):
            if self.getQValue(state, action) > maxValue:
                maxValue = self.getQValue(state, action)
                bestAction.clear()
                bestAction.append(action)
            elif self.getQValue(state, action) == maxValue:
                bestAction.append(action)

        return random.choice(bestAction)

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"
        if not legalActions:
            return None
        if util.flipCoin(self.epsilon):
            return random.choice(legalActions)
        else:
            return self.computeActionFromQValues(state)


    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        # print("state: "+str(state))
        # print("action: "+str(action))
        # print("nextState: "+str(nextState))
        # print("reward: "+str(reward))
        # maxNextQ = 0
        # for nextAction in self.getLegalActions(nextState):
        #     Qval = self.getQValue(nextState,nextAction)
        #     if (abs(Qval) > maxNextQ):
        #         maxNextQ = Qval
        maxNextQ = self.computeValueFromQValues(nextState)
        updateQ = (1-self.alpha)*self.getQValue(state,action) + self.alpha*(reward+self.discount*maxNextQ)
        self.qvalue[state,action] = updateQ
        return updateQ

        util.raiseNotDefined()

    def getPolicy(self, state):

        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        feat = self.featExtractor.getFeatures(state, action)
        #features = feat.getFeatures(state, action)
        qval = 0
        for feature in feat.keys():
            qval += self.weights[feature] * feat[feature]
        return qval

    def update(self, state, action, nextState, reward):
        """
           Update the weights based on the transition.
           Implements the weight update rule for Approximate Q-Learning.
        """
        # Calculate max Q-value for the next state
        actionsFromNextState = self.getLegalActions(nextState)
        if not actionsFromNextState:
            maxQnext = 0  # No legal actions means terminal state
        else:
            maxQnext = max(self.getQValue(nextState, a) for a in actionsFromNextState)

        # Compute the temporal difference (TD error)
        difference = (reward + self.discount * maxQnext) - self.getQValue(state, action)

        # Get features for the current (state, action) pair
        features = self.featExtractor.getFeatures(state, action)

        # Update weights for each feature
        for feature, value in features.items():
            self.weights[feature] += self.alpha * difference * value

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
