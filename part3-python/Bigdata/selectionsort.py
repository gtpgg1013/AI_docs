if __name__ == '__main__':
    n = input()
    # print(n)
    list = []
    for _ in range(int(n)):
        list.append(int(input()))

    for i in range(0,len(list)):
        for k in range(i, len(list)):
            if list[i] > list[k]:
                list[i], list[k] = list[k], list[i]

    for number in list:
        print(number)