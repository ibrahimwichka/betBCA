# converts the chance of a team winning to a betting odds: ex: +300
# does not artificially inflate the percentages
def set_odds(percent_chance):
    if (percent_chance < 50):
        return (1/(percent_chance/100) * 100)
    return -(1/(percent_chance/100) * 100)

# artificially set the sum of the probabilities to a probability higher than 100
def inflate_probability(chance, goal_percent):
    chance *= goal_percent
    return chance


def determine_return_value(correct, moneybet, odds):
    if correct == True:
        if (odds > 0):
            return moneybet + (moneybet/100) * odds
        else:
            return moneybet + (moneybet/odds) * 100
        
def checkMinimumBet(userBet):
        if userBet >= 0.10:
            return True
        return False