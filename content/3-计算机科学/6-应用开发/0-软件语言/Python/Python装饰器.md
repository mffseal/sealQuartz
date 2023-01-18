---
title: Python装饰器
created: 2022-09-21 16:37:20
updated: 2022-09-21 21:54:24
tags: 
- article
- featured
---

# Python装饰器

## 简述

- 装饰器是闭包的语法糖
- 装饰器就是在目标函数"周围"加上附加的代码
- 一般如插入日志、性能测试、事务处理、缓存、权限校验等场景
- 装饰器是面向切面编程的设计思想

## 简单装饰器

### 目标函数

```python
def foo():
    print('i am foo')
```

### 额外代码

打印log:

```python
def foo():
    print('i am foo')
    print("foo is running")
```

### 独立 log 函数

```python
def use_logging(func):
    print("%s is running" % func.__name__)
    func()

def foo():
    print('i am foo')

use_logging(foo)
```

### 问题

- 想要加强原函数，要修改函数调用处的代码逻辑，暴露了修改。

## 改进装饰器

```python
def use_logging(func):

    def wrapper():
        print("%s is running" % func.__name__)
        return func()   ## 把 foo 当做参数传递进来时，执行func()就相当于执行foo()
    return wrapper

def foo():
    print('i am foo')

foo = use_logging(foo)  ## 因为装饰器 use_logging(foo) 返回的时函数对象 wrapper，这条语句相当于  foo = wrapper
foo()                   ## 执行foo()就相当于执行 wrapper()
```

### 为什么要用两层函数来表示装饰器?

> 因为要把增强功能和原始函数打包在一起，返回一个新的函数对象，而不是原地调用。

#### 错误写法

```python
def use_logging(func):
    print("%s is running" % func.__name__)
    return func


def foo():
    print('i an foo')
    return 1


foo = use_logging(foo)
foo()
```

乍一看这么写和前面的代码效果一致, 但是其实很有问题:

- 在 `foo = use_logging(foo)` 时就打印了`foo()`正在执行, 而实际还未执行, 逻辑错误
- 无法实现在 `foo()` 执行后添加代码, 例如处理 `foo()` 的返回值

#### 个人理解

- 装饰器的外层代码起到**打包**的动作，**函数对象定义时不会执行**。
    - 接收目标函数(不执行), 交给内层函数(打包), 返回内层函数(不执行)
- 内层函数实现对目标函数的扩展, 并且**承担执行目标函数的功能**
    - 内层函数的 `return func()` 时就 执行了目标函数了
    - 因此 `wapper()` 可以在做到执行目标函数后再添加代码
    
    ```python
    def wrapper():
        print("%s is running" % func.__name__)
        func()
        result = func()  ## 此时已经执行了目标函数
        print(result)
        return result
    ```    
    

## @ 语法糖

```python
def use_logging(func):

    def wrapper():
        print("%s is running" % func.__name__)
        return func()
    return wrapper

@use_logging
def foo():
    print("i am foo")

foo()
```

- 有了 @ 就可以省去 `foo = use_logging(foo)` 这一句, 直接调用 `foo()` 即可得到想要的结果
- foo() 函数不需要做任何修改, 只需在定义的地方加上装饰器
- 如果我们有其他的类似函数, 可以继续调用装饰器来修饰函数, 而不用重复修改函数或者增加新的封装

装饰器在 Python 使用如此方便都要归因于 Python 的函数也是一个对象，能像普通的对象一样能作为参数传递给其他函数, 可以被赋值给其他变量, 可以作为返回值, 可以被定义在另外一个函数内。

## 目标函数需要接受参数

```python
def foo(name):
    print("i am %s" % name)
```

### 定义 wrapper 函数时候指定(目标函数的)参数

```python
def wrapper(name):
	logging.warn("%s is running" % func.__name__)
	return func(name)
return wrapper
```

### 装饰器不知道目标函数到底有多少个参数时

用 `*args` 来代替:

```python
def wrapper(*args):
	logging.warn("%s is running" % func.__name__)
	return func(*args)
return wrapper
```

### 目标函数定义了一些关键字参数

例如:  

```python
def foo(name, age=None, height=None):
    print("I am %s, age %s, height %s" % (name, age, height))
```

wrapper 函数指定关键字函数:  

```python
def wrapper(*args, **kwargs):
	## args是一个数组，kwargs一个字典
	logging.warn("%s is running" % func.__name__)
	return func(*args, **kwargs)
return wrapper
```

## 增强功能部分需要参数

参数控制操作外层打包程序的逻辑:  
指定日志级别

```python
def use_logging(level):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if level == "warn":
                logging.warn("%s is running" % func.__name__)
            elif level == "info":
                logging.info("%s is running" % func.__name__)
            return func(*args)
        return wrapper
    return decorator

@use_logging(level="warn")
def foo(name='foo'):
    print("i am %s" % name)

foo()
```

- 它实际上是对原有装饰器的一个函数封装, 并返回一个装饰器
- 可以将它理解为一个含有参数的闭包
- 使用 `@use_logging(level="warn")` 调用的时, Python 能够发现这一层的封装, 并把参数传递到装饰器的环境中

> 要定义三层就是因为有三类据说需要传递，但是不能混在同一个参数列表中：
> fun指针 / fun函数的参数 / 装饰器的参数

## 类装饰器

使用类装饰器主要依靠类的 `__call__` 方法, 当使用 `@` 形式将装饰器附加到函数上时, 就会调用此方法

```python
class Foo(object):
    def __init__(self, func):
        self._func = func

    def __call__(self):
        print ('class decorator runing')
        self._func()
        print ('class decorator ending')

@Foo
def bar():
    print ('bar')

bar()
```

## 找回目标函数元信息

### 装饰器抹除了目标函数的元信息

原函数的元信息不见了, 比如函数的 `docstring、__name__、参数列表`:

```python
## 装饰器
def logged(func):
    def with_logging(*args, **kwargs):
        print func.__name__      ## 输出 'with_logging'
        print func.__doc__       ## 输出 None
        return func(*args, **kwargs)
    return with_logging

## 函数
@logged
def f(x):
   """does some math"""
   return x + x * x

logged(f)
```

函数 `f` 被 `with_logging` 取代了, 它的 `docstring，__name__` 就是变成了 `with_logging` 函数的信息了.

### functools.wraps

- wraps本身也是一个装饰器
- 它能把原函数的元信息拷贝到装饰器里面的 `func` 函数中
- 使得装饰器里面的 `func` 函数也有和原函数 `foo` 一样的元信息

```python
from functools import wraps
def logged(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        print func.__name__      ## 输出 'f'
        print func.__doc__       ## 输出 'does some math'
        return func(*args, **kwargs)
    return with_logging

@logged
def f(x):
   """does some math"""
```

## 装饰器顺序

一个函数还可以同时定义多个装饰器:

```py
@a
@b
@c
def f ():
    pass
```

执行顺序:  

从里到外, **最先调用最里层的装饰器**, 最后调用最外层的装饰器:

```py
f = a(b(c(f)))
```
