---
title: java线程上下文切换（Thread Context Switch）
created: 2022-05-26 11:42:10
updated: 2022-05-26 14:12:02
tags: 
- atom
---
# java线程上下文切换（Thread Context Switch）

因为以下一些原因导致 cpu 不再执行当前的线程，转而执行另一个线程的代码：
- 线程的 cpu 时间片用完
- 垃圾回收
- 有更高优先级的线程需要运行
- 线程自己调用了 sleep、yield、wait、join、park、synchronized、lock 等方法

- 当 Context Switch 发生时，需要由操作系统**保存当前线程的状态**，并恢复另一个线程的状态。
- Java 中对应的概念就是程序计数器（Program Counter Register），它的作用是记住下一条 jvm 指令的执行地址，是**线程私有**的。
- 状态包括程序计数器、虚拟机栈中每个栈帧的信息，如局部变量、操作数栈、返回地址等。
- Context Switch 频繁发生会影响性能。
