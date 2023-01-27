---
title: gcc编译动态链接库
created: 2022-10-16 00:37:39
updated: 2022-10-23 19:54:37
tags: 
- article
---

# gcc编译动态链接库

`gcc -shared -fPIC xxx.c -o libxxx.so`

- -shared告诉gcc我正在编译一个dll而不是一个可执行文件，不要去找main函数等生成入口点。
- -fPIC 表示生成地址无关代码，实际上是
