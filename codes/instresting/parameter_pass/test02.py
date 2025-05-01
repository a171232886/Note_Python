"""
test01.py中的问题可以提炼成test02.py

输出为
[1, 2]
[3, 3]
"""

def fun1(x):
    x[0] = 1
    x[1] = 2
def fun2(x):
    x = [1, 2]


def main():
    d1 = [3, 3]
    d2 = [3, 3]

    fun1(d1)
    fun2(d2)
    
    print(d1)
    print(d2)
    
if __name__ == "__main__":
    main()