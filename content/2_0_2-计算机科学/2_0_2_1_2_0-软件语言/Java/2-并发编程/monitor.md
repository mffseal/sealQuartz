---
title: monitor
created: 2022-05-27 16:58:46
updated: 2022-05-27 18:44:30
tags: 
- atom
---
# monitor

监视器/管程。

每个 Java 对象都可以关联一个 Monitor 对象，如果使用 [[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/Java/2-并发编程/synchronized|synchronized]] 给对象上锁（重量级）之后，该[[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/Java/1-高级特性/对象头|对象头]]的[[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/Java/1-高级特性/Mark Word|Mark Word]] 中就被设置指向 Monitor 对象的指针。

Monitor 结构：
![[z-oblib/z2-attachments/Pasted image 20220527172014.png]]

1. Monitor 中 Owner 初始为 null。
2. 当 Thread-2 执行 synchronized(obj) 就会将 Monitor 的所有者 Owner 置为 Thread-2，Monitor中只能有一个 Owner。
3. 在 Thread-2 上锁的过程中，如果 Thread-3，Thread-4，Thread-5 也来执行synchronized(obj)，就会进入 EntryList BLOCKED。
4. Thread-2 执行完同步代码块的内容，然后唤醒 EntryList 中等待的线程来竞争锁，竞争的时是非公平的。
5. 图中 WaitSet 中的 Thread-0，Thread-1 是之前获得过锁，但条件不满足进入 WAITING 状态的线程，后面讲 wait-notify 时会分析。

> 注意：
synchronized 必须是进入同一个对象的 monitor 才有上述的效果，
不加 synchronized 的对象不会关联监视器，不遵从以上规则。

