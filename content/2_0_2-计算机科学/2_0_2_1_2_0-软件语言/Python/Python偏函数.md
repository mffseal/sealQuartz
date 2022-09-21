---
title: Python偏函数
created: 2022-09-22 01:28:44
updated: 2022-09-22 01:32:53
tags: 
- atom
---

# Python偏函数

## 使用

`functools`模块提供的一个功能，

int('123', base=2) 可以根据base将字符串解析成对应的进制，偏函数可以用来固定函数的参数：

```python
def int2(x, base=2):
    return int(x, base)
```

`functools.partial`就是帮助我们创建一个偏函数的，不需要我们自己定义`int2()`，可以直接使用下面的代码创建一个新的函数`int2`：

```python
>>> import functools
>>> int2 = functools.partial(int, base=2)
>>> int2('1000000')
64
>>> int2('1010101')
85
```

## 原理

偏函数运用了闭包的特性，大体上partial的功能可以表示成下边的形式：

```python
def partial(func, *part_args):
    def wrapper(*extra_args):
        args = list(part_args)
        args.extend(extra_args)
        return func(*args)
return wrapper
```

利用闭包的特性记忆了部分参数的值。

## 参考

- [偏函数 - 廖雪峰的官方网站 (liaoxuefeng.com)](https://www.liaoxuefeng.com/wiki/1016959663602400/1017454145929440)
- [(1条消息) Python中partial函数的工作原理_sigma65535的博客-CSDN博客](https://blog.csdn.net/u010301542/article/details/78376279)
