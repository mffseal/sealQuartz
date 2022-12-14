---
title: Python引用传递和值传递
created: 2022-09-21 21:54:42
updated: 2022-09-21 21:55:34
tags: 
- article
---

# Python引用传递和值传递

解释器会查看对象引用（内存地址）指示的那个值的类型，**如果变量指示一个可变的值，就会按引用调用语义。如果所指示的数据的类型是不可变的，则会应用按值调用语义**。

`列表 字典 集合`  
总是会按引用传入函数，函数代码组中对变量数据结构的任何改变都会**反映到调用代码中**。

`字符串 整数 元组`  
总是会按值传入函数，函数中对变量的任何修改是这个函数私有的，**不会反映到调用代码中**。
