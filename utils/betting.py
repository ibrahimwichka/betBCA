def set_odds(percent_chance):
    if (percent_chance < 50):
        return (1/(percent_chance/100) * 100)
    return -(1/(percent_chance/100) * 100)


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

def kjasdfjaewko():
    return "yes"