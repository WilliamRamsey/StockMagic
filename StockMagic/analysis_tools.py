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
    list1_above = []
    for i in range(len(list1)):
        if list1[i] > list2[i]:
            list1_above.append(True)
        else:
            list1_above.append(False)
    print(list1_above)

    for i in range(len(list1_above)):
        i += 1
        if list1_above[i] != list1_above[i-1]:
            print(i)
            
        
