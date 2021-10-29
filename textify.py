import numpy as np

def textify(numTries, best, bestIterationIndex, fitnesses, filepathToWrite='log.txt'):
  days = best['days']
  fitness = best['fitness']

  if len(fitnesses)>1:
    worse = min(fitnesses)
    average = sum(fitnesses)/len(fitnesses)
    std = np.std(fitnesses, ddof=1)
    variance = std**2

  with open(filepathToWrite, 'w', encoding='utf-8') as file:
    file.write(f' - Informações da execução -\n\n')
    file.write(f'Número de tentativas: {numTries}\n')
    
    if len(fitnesses)>1:
      file.write(f'Média do valor fitness: {average}\n')
      file.write(f'Desvio padrão: {std}\n')
      file.write(f'Variância: {variance}\n')
      file.write(f'Pior valor fitness obtido: {worse}\n')
      file.write(f'Melhor valor fitness obtido: {fitness}\n')
      file.write(f'Obtido na iteração: {bestIterationIndex}\n')  
    else: file.write(f'Fitness obtido: {fitness}\n')
    
    file.write(f'\n------------------------\n\n')
    file.write(f' - Melhor solução - \n\n')
    file.write(f'Dias necessários para assistir todos os filmes: {len(days)}\n')
    file.write(f'Cronograma sugerido:\n')

    for index, day in enumerate(days, start=1):
      file.write(f' - Dia {index}\n')

      for movie in day:
        file.write(f"  {movie['title']}\n")
      
      file.write('\n')