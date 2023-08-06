def get_checknum(num):
    num_list = list(map(int, num))
    o_list = num_list[-1::-2]
    return -sum(num_list + [(d > 4) + d for d in o_list]) % 10


def verify(num):
    return get_checknum(num) == num[-1]


def get_append(num):
    return num + str(get_checknum(num))
