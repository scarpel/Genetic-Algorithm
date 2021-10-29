from random import randint

def getSplitSize(parentLength, maxSplit=0.5):
  return randint(2, parentLength * maxSplit)

def getChild(otherParent, split, splittedAt):
  valueSet = set([movie['id'] for movie in split])
  parentValues = [value for value in otherParent[splittedAt:]+otherParent[0:splittedAt] if value['id'] not in valueSet]
  return parentValues[:splittedAt] + split + parentValues[splittedAt:]

def orderCrossover(p1, p2, maxSplitSize=0.5):
  length = len(p1)
  splitSize = randint(2, int(length * maxSplitSize))
  startSplitAt = randint(0, length - splitSize)
  endSplitAt = startSplitAt + splitSize

  return [ getChild(p2, p1[startSplitAt: endSplitAt], startSplitAt), 
    getChild(p1, p2[startSplitAt: endSplitAt], startSplitAt) ]
