#For storing elo scripts
import math


# Function to calculate the Probability
def Probability(rating1, rating2):
    return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400))

def average(v1, v2):
    val = v1 + v2
    val = val / 2
    return round(val,1)

# K is K-factor
# First player entered wins
def EloRating(Ra, Rb):
    avrank = average(Ra,Rb)
    K = 32
    if avrank > 2099:
        K = K - 8
    if avrank > 2400:
        K = K - 8
    # To calculate the Winning
    # Probability of Player a+b
    Pb = Probability(Ra, Rb)
    Pa = Probability(Rb, Ra) 
    Ra = Ra + K * (1 - Pa)
    Rb = Rb + K * (0 - Pb) 

    Ra = round(Ra, 2)
    Rb = round(Rb, 2)
    return Ra, Rb
