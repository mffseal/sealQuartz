---
title: java线程状态
created: 2022-05-26 17:41:07
updated: 2022-07-23 14:53:00
tags: 
- atom
---
# java线程状态

> [[3-计算机科学/2-计算机组成原理/线程状态|线程状态]]

根据Java API Thread.State枚举，有6种状态：

![[z-oblib/z2-attachments/Pasted image 20220526174139.png]]

> BLOCKED是指线程正在等待获取锁；WAITING是指线程正在等待其他线程发来的通知（notify），收到通知后，可能会顺序向后执行（RUNNABLE），也可能会再次获取锁，进而被阻塞住（BLOCKED）。

## 状态转换

### 1. NEW --> RUNNABLE
- NEW [[3-计算机科学/2-计算机组成原理/线程|线程]]刚被创建，但是还没有调用 start() 方法，**还未与操作系统线程相关联**。
- 当调用 t.start() 方法时，由 NEW --> RUNNABLE。

> 注意，Java API 层面的 RUNNABLE 状态涵盖了 操作系统 层面的【可运行状态】、【运行状态】和【阻塞状态】（由于 BIO 导致的线程阻塞，在 Java 里无法区分，仍然认为是可运行）。

### 2. RUNNABLE <--> WAITING
1. 调用 [[3-计算机科学/6-应用开发/0-软件语言/Java/2-并发编程/wait&notify|wait&notify]] 在RUNNABLE 和 AWITING间转换，t 线程用 [[3-计算机科学/6-应用开发/0-软件语言/Java/2-并发编程/synchronized|synchronized]](obj) 获取了对象锁后：
	- 调用 obj.wait() 方法时，t 线程从 RUNNABLE --> WAITING
	- 调用 obj.notify() ， obj.notifyAll() ， t.interrupt() 时
		- 竞争锁成功，t 线程从 WAITING --> RUNNABLE 
		- 竞争锁失败，t 线程从 WAITING --> BLOCKED 
- BLOCKED ， WAITING ， TIMED_WAITING 都是 Java API 层面对【阻塞状态】的细分。
- TERMINATED 当线程代码运行结束。

### 3. RUNNABLE <--> WAITING

- 当前线程调用 t.[[3-计算机科学/6-应用开发/0-软件语言/Java/2-并发编程/join|join]]() 方法时，当前线程从 RUNNABLE --> WAITING
	- 注意是**当前线程**在**t 线程对象**的[[3-计算机科学/6-应用开发/0-软件语言/Java/2-并发编程/monitor|Monitor]]上等待
- t 线程运行结束，或调用了当前线程的 [[3-计算机科学/6-应用开发/0-软件语言/Java/2-并发编程/interrupt|interrupt]]() 时，当前线程从 WAITING --> RUNNABLE

### 4. RUNNABLE <--> WAITING

- 当前线程调用 LockSupport.[[3-计算机科学/6-应用开发/0-软件语言/Java/2-并发编程/park&unpark|park]]() 方法会让当前线程从 RUNNABLE --> WAITING
- 调用 LockSupport.[[3-计算机科学/6-应用开发/0-软件语言/Java/2-并发编程/park&unpark|unpark]](目标线程) 或调用了线程 的 interrupt() ，会让目标线程从WAITING --> RUNNABLE

### 5. RUNNABLE <--> TIMED_WAITING

t 线程用 synchronized(obj) 获取了对象锁后：
	- 调用 obj.wait(long n) 方法时，t 线程从 RUNNABLE --> TIMED_WAITING
	- t 线程等待时间超过了 n 毫秒，或调用 obj.notify() ， obj.notifyAll() ， t.[[3-计算机科学/6-应用开发/0-软件语言/Java/2-并发编程/interrupt|interrupt]]() 时
		- 竞争锁成功，t 线程从 TIMED_WAITING --> RUNNABLE 
		- 竞争锁失败，t 线程从 TIMED_WAITING --> BLOCKED 

### 6. RUNNABLE <--> TIMED_WAITING

- 当前线程调用 t.join(long n) 方法时，当前线程从 RUNNABLE --> TIMED_WAITING
	- 注意是当前线程在t 线程对象的监视器上等待
- 当前线程等待时间超过了 n 毫秒，或t 线程运行结束，或调用了当前线程的 interrupt() 时，当前线程从TIMED_WAITING --> RUNNABLE

### 7. RUNNABLE <--> TIMED_WAITING

- 当前线程调用 Thread.sleep(long n) ，当前线程从 RUNNABLE --> TIMED_WAITING 
- 当前线程等待时间超过了 n 毫秒，当前线程从 TIMED_WAITING --> RUNNABLE 

### 8. RUNNABLE <--> TIMED_WAITING

- 当前线程调用 LockSupport.parkNanos(long nanos) 或 LockSupport.parkUntil(long millis) 时，当前线程从 RUNNABLE --> TIMED_WAITING
- 调用 LockSupport.unpark(目标线程) 或调用了线程 的 interrupt() ，或是等待超时，会让目标线程从 TIMED_WAITING--> RUNNABLE

### 9. RUNNABLE <--> BLOCKED

- t 线程用 synchronized(obj) 获取了对象锁时如果竞争失败，从 RUNNABLE --> BLOCKED 
- 持 obj 锁线程的同步代码块执行完毕，会唤醒该对象上所有 BLOCKED 的线程重新竞争，如果其中 t 线程竞争成功，从 BLOCKED --> RUNNABLE ，其它失败的线程仍然 BLOCKED 

### 10. RUNNABLE --> TERMINATED

- 当前线程所有代码运行完毕，进入 TERMINATED


## blocked和waiting区别

线程可以通过wait,join,LockSupport.park方式进入wating状态，进入wating状态的线程等待唤醒(notify或notifyAll)才有机会获取cpu的时间片段来继续执行。
线程的 blocked状态往往是无法进入同步方法/代码块来完成的。这是因为无法获取到与同步方法/代码块相关联的锁。

与wating状态相关联的是等待队列，与blocked状态相关的是同步队列，一个线程由等待队列迁移到同步队列时，线程状态将会由wating转化为blocked。可以这样说，blocked状态是处于wating状态的线程重新焕发生命力的必由之路。

 ## 总结

java把线程交给操作系统后就任由操作系统去调度了，所以操作系统层面的可运行/运行/阻塞对于java程序来说是一样的，jvm不会去细分这几种状态，同一就是RUNNABLE。
