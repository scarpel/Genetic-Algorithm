def binary_search(arr, value):
  start = 0
  end = len(arr)

  while True:
    if(start == end-1): return start

    middle = start + (end-start)//2

    if(start == middle): return end

    if(arr[middle] == value): return middle
    elif(arr[middle]<value): start = middle
    else:
      previous = middle - 1

      if(previous < 0): return middle; 
      else:
        if(arr[previous]<value): return middle
        elif (arr[previous] == value): return previous
        else: end = middle
    

  
