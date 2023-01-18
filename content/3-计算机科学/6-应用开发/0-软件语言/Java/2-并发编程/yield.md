---
title: yield
created: 2022-05-26 14:48:06
updated: 2022-05-26 14:48:47
tags: 
- atom
---
# yield

## 作用

1. 调用 yield 会让当前线程从 Running 进入 Runnable  就绪状态，然后调度执行其它线程。
2. 具体的实现依赖于操作系统的任务调度器。

