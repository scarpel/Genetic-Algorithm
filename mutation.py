from random import random, randint

def swap(arr, pos1, pos2):
  aux = arr[pos1]
  arr[pos1] = arr[pos2]
  arr[pos2] = aux
  return arr


def generateTwoIndex(length):
  upperLimit = length-1
  first = randint(0, upperLimit)
  second = randint(0, upperLimit)

  while first == second: second = randint(0, upperLimit)

  return [first, second]


def applyMutation(arr, mutationRate=0.1, maxMutations=10):
  if(random() <= mutationRate):
    length = len(arr)

    for _ in range(randint(1, maxMutations)):
      arr['sample'] = swap(arr['sample'], *generateTwoIndex(length))
    
    arr['fitness'] = None
    
    return arr
  else: return arr
