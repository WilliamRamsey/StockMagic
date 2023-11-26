# alternitivly df.rolling()
def simple_moving_average(data: object, period: int):
    # iterates through the index of the list to give each index an sma

    sma_list = []

    # iterates through the index of the list to give each index an sma
    for i in range(len(data)):
        # print(data[i])

        if i < period - 1:
            sma = None
        else:
            # print(i)
            window = data[i - period + 1:i+1]
            # sum values in window
            numerator = 0
            for value in window:
                numerator += value
            # print(numerator)
            # divide by window size
            sma = numerator / period
        sma_list.append(sma)
    # print(sma_list)
    return sma_list

def crossover(list1: list, list2: list):
    # Determine when list 1 is above list 2
    list1_above = []
    for i in range(len(list1)):
        if list1[i] > list2[i]:
            list1_above.append(True)
        else:
            list1_above.append(False)

    # Dertermine when list 1 crosses over list 2
    crossing_up_indices = []
    crossing_down_indices = []
    for i in range(len(list1_above)):
        # Crossing up
        if list1_above[i] == True and list1_above[i-1] == False:
            crossing_up_indices.append(i)
        # Crossing down
        elif list1_above[i] == False and list1_above[i-1] == True:
            crossing_down_indices.append(i)
        
    return crossing_up_indices, crossing_down_indices
       
def sma_crossover(data: object, period: int):
    sma_list = simple_moving_average(data, period)
    return crossover(data, sma_list)        

