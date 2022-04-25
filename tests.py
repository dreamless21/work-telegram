def f1():
     print('Called by f2()')


def f2():
    print('Called by main func')
    return f1()


print(f2())