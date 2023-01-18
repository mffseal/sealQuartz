---
title: sleep和wait的区别
created: 2022-04-28 16:38:27
updated: 2022-04-28 16:38:43
tags: 
- atom
---
# sleep和wait的区别

- **[[3-计算机科学/6-应用开发/0-软件语言/Java/2-并发编程/sleep|sleep]]方法是不会释放当前的锁的，而wait方法会。** 这也是最常见的一个多线程面试题。
-   wait可以指定时间，也可以不指定；而sleep必须指定时间。
-   wait释放cpu资源，同时释放锁；sleep释放cpu资源，但是不释放锁，所以易死锁。
-   wait必须放在同步块或同步方法中，而sleep可以在任意位置。