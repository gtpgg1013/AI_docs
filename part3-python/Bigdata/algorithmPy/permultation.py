a = 'string'
str_length = len(a)
check = 0

string = ''.join(sorted(a))

def perm(string,str_list):
    global str_length, check
    if len(str_list) == str_length:
        print(''.join(str_list))
        check += 1
        return
    for i in range(len(string)):
        # if i==0:
        #     n_string = string[i+1:]
        #     # print(n_string)
        #     str_list.append(string[i])
        #     perm(n_string,str_list)
        #     str_list.pop(-1)
        # if 0 < i < len(string):
        #   
            n_string = string[:i] + string[i+1:]
            str_list.append(string[i])
            perm(n_string,str_list)
            str_list.pop(-1)

        # if i==len(string)-1:
        #     n_string = string[:i]
        #     str_list.append(string[i])
        #     perm(n_string,str_list)
        #     str_list.pop(-1)

perm(string,[])
print(check)