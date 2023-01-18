---
title: safepoint
created: 2022-04-27 16:38:22
updated: 2022-04-27 16:41:36
tags: 
- atom
---
# safepoint

## 什么是safepoint

safepoint可以用在不同地方，比如GC、Deoptimization，在Hotspot VM中，GC safepoint比较常见，需要一个数据结构记录每个线程的调用栈、寄存器等一些重要的数据区域里什么地方包含了GC管理的指针。

从线程角度看，safepoint可以理解成是在代码执行过程中的一些特殊位置，当线程执行到这些位置的时候，说明虚拟机当前的状态是安全的，如果有需要，可以在这个位置暂停，比如发生GC时，需要暂停暂停所以活动线程，但是线程在这个时刻，还没有执行到一个安全点，所以该线程应该继续执行，到达下一个安全点的时候暂停，等待GC结束。

## 什么地方可以放safepoint

下面以Hotspot为例，简单的说明一下什么地方会放置safepoint  
1. 理论上，在解释器的每条字节码的边界都可以放一个safepoint，不过挂在safepoint的调试符号信息要占用内存空间，如果每条机器码后面都加safepoint的话，需要保存大量的运行时数据，所以要尽量少放置safepoint，在safepoint会生成polling代码询问VM是否要“进入safepoint”，polling操作也是有开销的，polling操作会在后续解释。

2. 通过JIT编译的代码里，会在所有方法的返回之前，以及所有非counted loop的循环（无界循环）回跳之前放置一个safepoint，为了防止发生GC需要STW时，该线程一直不能暂停。另外，JIT编译器在生成机器码的同时会为每个safepoint生成一些“调试符号信息”，为GC生成的符号信息是OopMap，指出栈上和寄存器里哪里有GC管理的指针。