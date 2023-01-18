---
title: wait&notify
created: 2022-05-28 16:50:43
updated: 2022-05-29 23:03:13
tags: 
- atom
---
# wait&notify

## wait

### 为什么需要wait

- 由于条件不满足，小南不能继续进行计算
- 但小南如果一直占用着锁，其它人就得一直阻塞，效率太低
![[z-oblib/z2-attachments/Pasted image 20220528165543.png]]
- 于是老王单开了一间休息室（调用 wait 方法），让小南到休息室（WaitSet）等着去了，但这时锁释放开，
- 其它人可以由老王随机安排进屋
- 直到小M将烟送来，大叫一声 [ 你的烟到了 ] （调用 notify 方法）
![[z-oblib/z2-attachments/Pasted image 20220528165605.png]]
- 小南于是可以离开休息室，重新进入竞争锁的队列
![[z-oblib/z2-attachments/Pasted image 20220528165629.png]]

### 原理

![[z-oblib/z2-attachments/Pasted image 20220528170242.png]]

1. Owner 线程发现条件不满足，调用 wait 方法，即可进入 WaitSet 变为 WAITING 状态
> 不管是等外卖的还是等烟的都会在一个房间里等待，唤醒的时候不能区分。[[3-计算机科学/6-应用开发/0-软件语言/Java/2-并发编程/ReentrantLock|ReentrantLock]]改进了这一点。
3. BLOCKED 和 WAITING 的线程都处于阻塞状态，不占用 CPU 时间片
4. BLOCKED 线程会在 Owner 线程释放锁时唤醒
5. WAITING 线程会在 Owner 线程调用 notify 或 notifyAll 时唤醒，但唤醒后并不意味者立刻获得锁，仍需进入 EntryList 重新竞争

> waiting和blocked状态下的线程在本质上都是blocked状态，但waiting线程是在等待叫号（所以用Set），而blocked是在排队（所以用List）。

### 使用

- wait和notify是针对重量级锁的。
- obj.wait() 让进入 object 监视器的线程到 waitSet 等待。
- obj.notify() 在 object 上正在 waitSet 等待的线程中挑一个唤醒 。
- obj.notifyAll() 让 object 上正在 waitSet 等待的线程全部唤醒。
它们都是线程之间进行协作的手段，都属于 Object 对象的方法。必须获得此对象的锁，才能调用这几个方法。

## notify

notify若遇到多个wait线程，不能指定叫醒谁，只能随机叫醒或者都叫醒。这种情况叫做**虚假唤醒**。

通过notifyAll唤醒所有wait线程，并在被唤醒中改用while循环判断条件，这样能防止虚假唤醒。

## 正确使用方式

```java
synchronized(lock) {
    while(条件不成立) {
        lock.wait();
    }
    // 干活
}
 
//另一个线程
synchronized(lock) {
    lock.notifyAll();
}
```

注意wait线程使用while(条件)，唤醒者使用notifyAll()。

