# analysis.py
# -----------
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


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

def question2():
    answerDiscount = 0.9
    answerNoise = 0 #Door de noise 0 te maken volgt 
    return answerDiscount, answerNoise

def question3a():
    answerDiscount = 0.9
    answerNoise = 0.1
    answerLivingReward = -5.0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3b():
    answerDiscount = 0.3 #Hogere discount --> verdere pad, lagere discount --> werkt tot 0.1
    answerNoise = 0.1 #Weinig noise want hij volgt het optimale pad
    answerLivingReward = 0 #Geen reward voor te leven
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3c():
    answerDiscount = 0.9 #Hoge Discount nodig anders zal hij ALTIJD als eerste Noord kiezen
    answerNoise = 0 #Was eerst 0.05
    answerLivingReward = 0 #Er moet een hogere answerLivingReward zijn dan bij 3a anders kiest hij toch voor 1 ipv 10
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3d():
    answerDiscount = 0.5 #Gemiddelde discount
    answerNoise = 0.1 #Lage noise voor weinig afwijking van het optimale pad
    answerLivingReward = 0.2 #Een beetje reward als hij niet de klif neemt (kan in principe 0 zijn want hij wil altijd als eerste naar noord)
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3e():
    answerDiscount = 0.5
    answerNoise = 0.1
    answerLivingReward = 5 #simpelweg een heel hoge LivingReward zodat zoveel mogelijk stappen nemen beloond wordt
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question8():
    answerEpsilon = None
    answerLearningRate = None
    return answerEpsilon, answerLearningRate
    # If not possible, return 'NOT POSSIBLE'

if __name__ == '__main__':
    print('Answers to analysis questions:')
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print('  Question %s:\t%s' % (q, str(response)))
