from collections import deque

possibleMoves = [(1, 0), (2, 0), (1, 1), (0, 1), (0, 2)]
### moving from right to left
endState = (3,3,'R')

class ProblemState:
    def __init__(self, stateValue, parentState=None, numberOfMoves=0):
        self.stateValue = stateValue
        self.parentState = parentState
        self.numberOfMoves = numberOfMoves

    
    def isStateLegal(self):
        missionaries = self.stateValue[0]
        cannibals = self.stateValue[1]
        
        if (missionaries < 0 or missionaries > 3) or (cannibals < 0 or cannibals > 3): 
            return False
        return True        

    def computeNextLegalStates(self):
        allStateList = list()
        missionariesRightShore, cannibalsRightShore, boatLocation = self.stateValue
        for move in possibleMoves:
            missionariesChanged, cannibalChanged = move
            if boatLocation == 'R':  
                newComputedStateValue = (missionariesRightShore-missionariesChanged, cannibalsRightShore-cannibalChanged, 'L')
            else:
                newComputedStateValue = (missionariesRightShore+missionariesChanged, cannibalsRightShore+cannibalChanged, 'R')
            
            newComputedState = ProblemState(newComputedStateValue, self, self.numberOfMoves+1)
            if newComputedState.isStateLegal():
                allStateList.append(newComputedState)

        return allStateList
    
    def isWrongState(self):
        missionariesRightShore, cannibalsRightShore, boatLocation = self.stateValue        
        if missionariesRightShore > 0 and missionariesRightShore < cannibalsRightShore:
            return True
        if missionariesRightShore < 3 and cannibalsRightShore <  missionariesRightShore:
            return True
        return False

    def isFinalState(self):
        if self.stateValue == endState:
            return True
        return False
    
    def __str__(self):
        missionariesRightShore, cannibalsRightShore, boatLocation = self.stateValue
        if boatLocation == 'R':
            return f"{missionariesRightShore} Missionaries and {cannibalsRightShore} cannibals on the right shore"
        else:
            missionaries = 3 - missionariesRightShore
            cannibals = 3 - cannibalsRightShore
            return f"{missionaries} Missionaries and {cannibals} cannibals on the left shore"

def search():
    searchingStateDeque = deque()
    rootState = ProblemState((0,0, 'L'))
    searchingStateDeque.append(rootState)
    solutionList = list()
    trackedStates = set()

    while len(searchingStateDeque) > 0:
        currentState = searchingStateDeque.pop()
        listOfNextStates = currentState.computeNextLegalStates()
        
        for nextState in listOfNextStates:
            currentStateValue = nextState.stateValue
            
            if currentStateValue not in trackedStates:
                
                if nextState.isWrongState():
                    #print(f"Wrong solution - {nextState}")
                    continue
                elif nextState.isFinalState():
                    solutionList.append(nextState)
                    print (f'Solution is done in {nextState.numberOfMoves} moves')
                    continue
                
                ## append to the left of dequeue
                searchingStateDeque.appendleft(nextState)
                ##add to seen states
                trackedStates.add(currentStateValue)
                
    return solutionList

def visualizeSolution(currentState):
    print(currentState)
    if currentState.parentState != None:
        newMissionariesOnRight, newCannibalsOnRight, newBoatLocation = currentState.parentState.stateValue
        missionariesOnRight, cannibalsOnRight, boatLocation = currentState.stateValue
        print(f'-- {abs(missionariesOnRight-newMissionariesOnRight)} missionaries and {abs(newCannibalsOnRight-cannibalsOnRight)} cannibals on the boat')
        print(f'-- Boat Direction {boatLocation} -> {newBoatLocation}')
        
allSolutions = search()
solutionCount = 1
for solution in allSolutions:
    print('*******')
    print(f'Solution {solutionCount}')
    solutionCount += 1
    currentState = solution
    while currentState:
        visualizeSolution(currentState)
        currentState = currentState.parentState


