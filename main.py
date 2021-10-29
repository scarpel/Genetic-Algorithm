import csv
from mutation import applyMutation
from random import shuffle, random
from crossover import orderCrossover
from binary_search import binary_search
from textify import textify
import argparse

def getMovies(filepath='data.csv'):
  movies = []

  with open(filepath) as file:
    values = csv.reader(file, delimiter=',')
    next(values)
    index = 0

    for value in values:
      movies.append({
        'rating': float(value[3]),
        'duration': int(value[4]),
        'title': value[0],
        'id': index
      })
      index += 1
    
  return movies


# Sort movies in two groups: can and cannot group
def sortMovies(movies, minDuration = 90, watchTime = 240):
  canGroup = []
  cannotGroup = []

  for movie in movies:
    if(movie['duration'] + minDuration <= watchTime): canGroup.append(movie)
    else: cannotGroup.append(movie)
  
  return [canGroup, cannotGroup]


def getSampleId(sample):
  return ','.join([ str(value['id']) for value in sample ])


def getSampleObject(sample):
  return {
      'sample': sample,
      'fitness': None,
      'days': None
    }

# Generate n samples based on array
def getSamples(array, numSamples = 100):
  samples = []
  alreadAdded = set()

  for _ in range(numSamples):
    sample = array.copy()
    shuffle(sample)
    sampleId = getSampleId(sample)

    while sampleId in alreadAdded:
      shuffle(sample)
      sampleId = getSampleId(sample)

    alreadAdded.add(sampleId)
    samples.append(getSampleObject(sample))

  return samples


def getFitness(movies, cannotGroupRatings, cannotGroupDays, watchTime):
  days = []
  ratings = cannotGroupRatings
  duration = 0
  currentRating = 0
  selectedMovies = []

  for movie in movies:
    if(duration + movie['duration'] <= watchTime):
      selectedMovies.append(movie)
      duration += movie['duration']
      currentRating += movie['rating']
    else:
      if(len(selectedMovies)>0):
        days.append(selectedMovies)
        ratings += currentRating

      selectedMovies = [movie]
      currentRating = movie['rating']
      duration = movie['duration']

  days.append(selectedMovies)
  ratings += currentRating
  
  return [days, ratings/(len(days) + cannotGroupDays)]


def applyFitnessToPopulation(population, cannotGroupRatings, cannotGroupDays, watchTime=240):
  for value in population:
    if(value['fitness'] is None):
      days, fitness = getFitness(value['sample'], cannotGroupRatings, cannotGroupDays, watchTime=watchTime)
      value['fitness'] = fitness
      value['days'] = days 
  
  return population


def getRandomSamples(samples, numSelected = 2, fitnessSum=None):
  if(fitnessSum is None):
    fitnessSum = sum([sample['fitness'] for sample in samples])
  
  percentages = []
  summatory = 0

  for sample in samples:
    summatory += sample['fitness']/fitnessSum
    percentages.append(summatory)
  
  selectedIndexes = []

  for _ in range(numSelected):
    index = binary_search(percentages, random())
    while(index in selectedIndexes): index = binary_search(percentages, random())
    selectedIndexes.append(index)

  return [samples[index] for index in selectedIndexes]
  

def joinBothMovies(sample, cannotGroupMovies):
  for movie in cannotGroupMovies:
    sample.append([movie])
  
  return sample

def validateMovies(sample):
  firstIndex = -1
  secondIndex = -1

  for index, day in enumerate(sample):
    titles = [movie['title'] for movie in day]

    if('The Godfather' in titles): 
      firstIndex = index
      if(secondIndex != -1): break
    elif('The Godfather: Part II' in titles):
      secondIndex = index
      if(firstIndex != -1): break
  
  if(secondIndex<firstIndex):
    aux = sample[firstIndex]
    sample[firstIndex] = sample[secondIndex]
    sample[secondIndex] = aux
  
  return sample


def geneticAlgorithm(filepath='data.csv', watchTime=240, numSamples=100, generations=100, maxCrossoverSplitSize=0.5):
  movies = getMovies(filepath)
  minDuration = min(movies, key=lambda movie: movie['duration'])['duration']

  canGroup, cannotGroup = sortMovies(movies, minDuration=minDuration, watchTime=watchTime)
  cannotGroupRatings = sum([movie['rating'] for movie in cannotGroup])
  cannotGroupDays = len(cannotGroup)

  # Generate samples
  samples = getSamples(canGroup, numSamples)

  for _ in range(generations):
    # Calculate the fitness of all the population
    applyFitnessToPopulation(samples, cannotGroupRatings=cannotGroupRatings, cannotGroupDays=cannotGroupDays, watchTime=watchTime)
    samples.sort(key=lambda movie: movie['fitness'], reverse=True)
    
    # Apply order crossover to the best parents
    sample1, sample2 = getRandomSamples(samples, 2)
    child1, child2 = orderCrossover(sample1['sample'], sample2['sample'], maxSplitSize=maxCrossoverSplitSize)
    samples[-1] = getSampleObject(child1)
    samples[-2] = getSampleObject(child2)

    # Apply mutation
    for index in range(numSamples):
      samples[index] = applyMutation(samples[index])

  applyFitnessToPopulation(samples, cannotGroupRatings=cannotGroupRatings, cannotGroupDays=cannotGroupDays)
  samples.sort(key=lambda movie: movie['fitness'], reverse=True)

  finalSample = samples[0]

  # Join both movies and shuffle
  finalSample['days'] = joinBothMovies(finalSample['days'], cannotGroup)
  shuffle(finalSample['days'])

  # Verify if The Godfather comes before The Godfather: Part II
  finalSample['days'] = validateMovies(finalSample['days'])

  return finalSample

def run(numSamples=100, generations=1000, watchTime=240, numTries=10, maxCrossoverSplitSize=0.5, filepath='data.csv', writeFilepath='log.txt'):
  best = None
  bestIteration = None
  fitnesses = []

  print('Começando a execução...')

  for index in range(numTries):
    print (f'Executando a iteração {index+1} de {numTries}', end="\r")
    result = geneticAlgorithm(filepath, watchTime, numSamples, generations, maxCrossoverSplitSize)

    fitnesses.append(result['fitness'])

    if(best is None or result['fitness'] > best['fitness']):
      best = result
      bestIteration = index

  print('\x1b[2K', end='')
  print('Execução completa!')
  print('Escrevendo resultados...')
  textify(numTries, best, bestIteration, fitnesses, writeFilepath)
  print('Pronto!')

if(__name__ == '__main__'):
  parser = argparse.ArgumentParser()
  parser.add_argument('--numSamples', default=100, type=int)
  parser.add_argument('--generations', default=1000, type=int)
  parser.add_argument('--watchTime', default=240, type=float)
  parser.add_argument('--numTries', default=20, type=int)
  parser.add_argument('--maxCrossoverSplitSize', default=0.5, type=float)
  parser.add_argument('--filepath', default='data.csv')
  parser.add_argument('--writeFilepath', default='log.txt')
  args = parser.parse_args()

  run(**vars(args))