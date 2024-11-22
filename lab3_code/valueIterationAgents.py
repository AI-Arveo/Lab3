# valueIterationAgents.py
# -----------------------
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

import mdp, util
from learningAgents import ValueEstimationAgent


class ValueIterationAgent(ValueEstimationAgent):
    """
        A ValueIterationAgent takes a Markov decision process (MDP) on
        initialization and runs value iteration for a given number of iterations
        using the supplied discount factor.
    """

    def __init__(self, mdp, discount=0.9, iterations=100):
        """
        Initialize the ValueIterationAgent:
        - mdp: The Markov decision process.
        - discount: Discount factor for future rewards.
        - iterations: Number of iterations for value iteration.
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()  # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        """
        Perform value iteration to compute the optimal policy.
        """
        print("\nStates using MDP:", self.mdp.getStates())

        for i in range(self.iterations):
            newValues = self.values.copy()  # Create a copy of current values for update

            # Iterate over all states in the MDP
            for state in self.mdp.getStates():
                if self.mdp.isTerminal(state):
                    # For terminal states, set the value explicitly and skip computation
                    newValues[state] = 0  # Assign a reward of 0 for terminal states
                    continue

                maxQValue = -99999  # Initialize max Q-value as negative infinity

                # Iterate over all possible actions from the current state
                for action in self.mdp.getPossibleActions(state):
                    qValue = self.computeQValueFromValues(state, action)
                    maxQValue = max(maxQValue, qValue)  # Update the max Q-value

                # Update the value for the state
                newValues[state] = maxQValue

            # Update the values for the next iteration
            self.values = newValues

    def getValue(self, state):
        """
        Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
        Compute the Q-value of action in state from the value function stored in self.values.
        """
        Bellman = 0
        for nextState, probability in self.mdp.getTransitionStatesAndProbs(state, action):
            Bellman += probability * (
                    self.mdp.getReward(state, action, nextState) + self.discount * self.values[nextState]
            )
        return Bellman

    def computeActionFromValues(self, state):
        """
        The policy is the best action in the given state
        according to the values currently stored in self.values.

        If the state is terminal, return None.
        """
        if state == "TERMINAL_STATE":
            return None

        maxValue = -99999  #Gebruik een zeer lage waarde zodat alle values sowieso hoger zijn
        bestAction = None  #Initialize best action as None

        # Iterate through possible actions
        for action in self.mdp.getPossibleActions(state):
            qValue = self.computeQValueFromValues(state, action)
            if qValue > maxValue:
                maxValue = qValue
                bestAction = action

        return bestAction

    def getPolicy(self, state):
        """
        Return the optimal policy (best action) for the given state.
        """
        return self.computeActionFromValues(state)

    def getAction(self, state):
        """
        Returns the policy at the state (no exploration).
        """
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        """
        Returns the Q-value for the given state and action.
        """
        return self.computeQValueFromValues(state, action)


class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        An AsynchronousValueIterationAgent takes a Markov decision process (MDP) on
        initialization and runs cyclic value iteration for a given number of iterations
        using the supplied discount factor.
    """

    def __init__(self, mdp, discount=0.9, iterations=1000):
        """
        Initialize the AsynchronousValueIterationAgent:
        - mdp: The Markov decision process.
        - discount: Discount factor for future rewards.
        - iterations: Number of iterations for cyclic updates.
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        """
        Perform asynchronous value iteration.
        """
        states = self.mdp.getStates()
        for i in range(self.iterations):
            state = states[i % len(states)]
            if not self.mdp.isTerminal(state):
                maxQValue = -99999
                for action in self.mdp.getPossibleActions(state):
                    qValue = self.computeQValueFromValues(state, action)
                    maxQValue = max(maxQValue, qValue)
                self.values[state] = maxQValue


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        on initialization and runs prioritized sweeping value iteration.
    """

    def __init__(self, mdp, discount=0.9, iterations=100, theta=1e-5):
        """
        Initialize the PrioritizedSweepingValueIterationAgent:
        - mdp: The Markov decision process.
        - discount: Discount factor for future rewards.
        - iterations: Number of iterations for prioritized updates.
        - theta: Threshold for priority queue updates.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        """
        Perform prioritized sweeping value iteration.
        """
        # Placeholder for prioritized sweeping logic.
        "*** YOUR CODE HERE ***"
