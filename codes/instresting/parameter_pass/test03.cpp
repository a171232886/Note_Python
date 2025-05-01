#include <iostream>


/*
参考C++的方式
1. Python的函数传参方式类似于C++的指针传递（详细地说是指针按值传递，pointer passing by value）

指针按值传递，pointer passing by value
 - 可以修改指针指向的内容（fun 和 fun1）
 - 但不能修改指针自身指向

指针按引用传递，pointer passing by reference
 - 可以修改指针指向的内容
 - 也能修改指针自身指向（fun3）

fun3 的参数 int *& x
 - 可理解为int指针的引用，即 (int * ) &x


执行结果为
10
This is function1. 20
10
This is function2. 30
30
*/

void fun(int *x){
    // simple use of pointer
    // the operation on `*x` will affect `*a`. Because `x` and `a` are pointers.
    *x = 10;
}

void fun1(int *x){
    // pointer passed by value
    // `x` of func1 is the formal parameter（形参）, `a` of main is the actual Parameter（实参）
    // therefore, the operation on `x` will not affect `a`
    // But the operation on `*x` will affect `*a`. like `fun1`
    x = new int(20);
    std::cout << "This is function1. " << *x << std::endl;
}

void fun2(int *&x){
    // pointer passed by reference
    // `x` of func2 is the reference of `a`
    // the operation on `x` will affect `a`
    // the operation on `*x` will affect `*a` too.
    x = new int(30);
    std::cout << "This is function2. " << *x << std::endl;
}

int main(){
    int *a = new int(1);
    fun(a);
    std::cout << *a << std::endl;
    fun1(a);
    std::cout << *a << std::endl;
    fun2(a);
    std::cout << *a << std::endl;

    return 0;
}