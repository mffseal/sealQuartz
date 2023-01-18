---
title: GOT表
created: 2022-09-07 19:10:43
updated: 2022-09-11 01:47:37
tags: 
- atom
---
# GOT表

> [深入理解GOT表和PLT表 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/130271689)

GOT(Global Offset Table)全局偏移表，链接器为外部符号填充的实际偏移地址表。

位于数据段，内容可修改。

## 结构

- GOT[1]：一个指向内部数据结构的指针，类型是 link_map，在动态装载器内部使用，包含了进行[[3-计算机科学/3-操作系统/Linux/符号解析|符号解析]]需要的当前 ELF 对象的信息。在它的 `l_info` 域中保存了 `.dynamic` 段中大多数条目的指针构成的一个数组，我们后面会利用它。
- GOT[2]：一个指向动态装载器中 [[3-计算机科学/3-操作系统/Linux/_dl_runtime_resolve|_dl_runtime_resolve]] 函数的指针。