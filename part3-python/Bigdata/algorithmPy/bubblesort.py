if __name__ == '__main__':
    n = input()
    # print(n)
    list = []
    for _ in range(int(n)):
        list.append(int(input()))

    for i in range(0,len(list)-1):
        for k in range(0, len(list)-i-1):
            if list[k] > list[k+1]:
                list[k], list[k+1] = list[k+1], list[k]

    for number in list:
        print(number)