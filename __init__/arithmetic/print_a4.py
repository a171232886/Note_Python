import arithmetic as a4


def print_a4(x,y):
    print("{} {} {} = {}".format(x, '+', y, a4.add(x,y)))
    print("{} {} {} = {}".format(x, '-', y, a4.sub(x,y)))
    print("{} {} {} = {}".format(x, '*', y, a4.mul(x,y)))
    print("{} {} {} = {}".format(x, '/', y, a4.dev(x,y)))
    return

def print_hello():
    print(" hello from arithmetic/hello/print_hello")

if __name__ == "__main":
    print_a4(3,8)