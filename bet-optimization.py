# Script to calculate the amount of money to hedge on favorites to
# optimize EV and risk zero money. Only possible with the free bet
# promos the mass sports books are offering for first time users.

# game 1 lines
FAV_LINE_1 = 180
UNDER_LINE_1 = 170
# game 1 wager amounts
UNDER_WAGER_1 = 1000
# game 2 lines
FAV_LINE_2 = 135
UNDER_LINE_2 = 115
# game 2 wager amounts
UNDER_WAGER_2 = UNDER_WAGER_1

def getPercentageFromLine(line, isFav):
  if isFav:
    return line/(line+100)
  return 100/(line+100)

def calculateUnderProfit(line, wager):
  return wager*line/100

def calculateFavoriteProfit(line, wager):
  return wager*100/line

def calculateEV(favWager1, favWager2):
  # scenario 1, underdog wins first game
  wager1 = UNDER_WAGER_1 + favWager1
  return1 = UNDER_WAGER_1 + calculateUnderProfit(UNDER_LINE_1, UNDER_WAGER_1)
  net1 = return1 - wager1
  percentChance1 = getPercentageFromLine(UNDER_LINE_1, False)

  # scenario 2, underdog wins second game
  wager2 = UNDER_WAGER_2 + favWager1 + favWager2
  return2 = favWager1 + calculateFavoriteProfit(FAV_LINE_1, favWager1) + calculateUnderProfit(UNDER_LINE_2, UNDER_WAGER_2)
  net2 = return2 - wager2
  percentChance2 = getPercentageFromLine(FAV_LINE_1, True) * getPercentageFromLine(UNDER_LINE_2, False)

  # scenario 3, underdog loses second game
  wager3 = UNDER_WAGER_2 + favWager1 + favWager2
  return3 = favWager1 + calculateFavoriteProfit(FAV_LINE_1, favWager1) + favWager2 + calculateFavoriteProfit(FAV_LINE_2, favWager2)
  net3 = return3 - wager3
  percentChance3 = getPercentageFromLine(FAV_LINE_1, True) * getPercentageFromLine(FAV_LINE_2, True)

  # we don't want to lose any money, the whole point of this is that it's risk free
  # therefore, if any of the scenarios are negative, return 0
  if net1 < 0 or net2 < 0 or net3 < 0:
    return 0

  if net2 > net1 or net3 > net1 or abs(net1-net2) > 100:
    return 0

  return net1*percentChance1+net2*percentChance2+net3*percentChance3

# solves for the amount of money to hedge on favorite in first
# game and second game
def optimize():
  maxEV = 0
  firstWager = 0
  secondWager = 0
  for i in range(0, 5000):
    for j in range(0, 5000):
      ev = calculateEV(i, j)
      if(ev > maxEV):
        maxEV = ev
        firstWager = i
        secondWager = j
  return (firstWager, secondWager, maxEV)

if __name__ == '__main__':
  print(optimize())
