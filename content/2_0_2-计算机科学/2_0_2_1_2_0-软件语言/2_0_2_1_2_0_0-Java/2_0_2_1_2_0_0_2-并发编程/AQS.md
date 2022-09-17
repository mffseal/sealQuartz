---
title: AQS
created: 2022-05-04 22:29:23
updated: 2022-06-09 21:50:26
tags: 
- atom
---
# AQS


全称是 AbstractQueuedSynchronizer，是**阻塞**式锁（类似[[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/2_0_2_1_2_0_0-Java/2_0_2_1_2_0_0_2-并发编程/synchronized|synchronized]]）和相关的同步器工具的框架。

## 特点

- 用 **state** 属性来表示资源的状态（分独占模式和共享模式），子类需要定义如何维护这个状态，控制如何获取锁和释放锁
	- getState - 获取 state 状态
	- setState - 设置 state 状态
	- compareAndSetState - cas 机制设置 state 状态
	- 独占模式是只有一个线程能够访问资源，而共享模式可以允许多个线程访问资源
- 提供了基于 FIFO 的等待队列，类似于 Monitor 的 EntryList
- 条件变量来实现等待、唤醒机制，支持多个条件变量，类似于 Monitor 的 WaitSet

子类主要实现这样一些方法（默认抛出 UnsupportedOperationException）
- tryAcquire
- tryRelease
- tryAcquireShared
- tryReleaseShared
- isHeldExclusively

> 这里不使用抽象方法的目的是：避免强迫子类中把所有的抽象方法都实现一遍，减少无用功，这样子类只需要实现自己关心的抽象方法即可，比如 Semaphore 只需要实现 tryAcquire 方法而不用实现其余不需要用到的模版方法。


### 获取锁

```java
// 如果获取锁失败
if (!tryAcquire(arg)) {
    // 入队, 可以选择阻塞当前线程  park unpark
}
```

> AQS使用park&unpark来阻塞和恢复线程

### 释放锁

```java
// 如果释放锁成功
if (tryRelease(arg)) {
    // 让阻塞线程恢复运行
}
```


## 自己实现不可重入锁

实现Lock+AQS：

```java
package test;  
  
import lombok.extern.slf4j.Slf4j;  
  
import java.util.concurrent.TimeUnit;  
import java.util.concurrent.locks.AbstractQueuedSynchronizer;  
import java.util.concurrent.locks.Condition;  
import java.util.concurrent.locks.Lock;  
  
@Slf4j  
public class Test23Aqs {  
    public static void main(String[] args) {  
        MyLock lock = new MyLock();  
        new Thread(()->{  
            log.debug("尝试加锁");  
            lock.lock();  
            log.debug("加锁成功");  
            try {  
                log.debug("加锁");  
                try {  
                    Thread.sleep(3000);  
                } catch (InterruptedException e) {  
                    e.printStackTrace();  
                }  
            } finally {  
                log.debug("解锁");  
                lock.unlock();  
            }  
        }).start();  
  
        new Thread(()->{  
            log.debug("尝试加锁");  
            lock.lock();  
            log.debug("加锁成功");  
            try {  
                log.debug("加锁");  
            } finally {  
                log.debug("解锁");  
                lock.unlock();  
            }  
        }).start();  
    }  
}  
  
  
// 不可重入锁：  
// 仿ReentrantLock实现  
// 1. 实现Lock接口  
// 2. 使用AQS同步器类  
class MyLock implements Lock {  
  
    // 同步器类  
    // 锁的大部分功能是由该同步器类完成的  
    // 实现一个独占锁：  
    class MySync extends AbstractQueuedSynchronizer {  
        // 尝试获取锁  
        @Override  
        protected boolean tryAcquire(int arg) {  
            // 可能有其它线程同时尝试加锁，所以要用cas  
            if (compareAndSetState(0, 1)) {  
                // 加上锁了，设置owner为当前线程  
                setExclusiveOwnerThread(Thread.currentThread());  
                return true;            }  
            return false;  
        }  
  
        // 尝试释放锁  
        @Override  
        protected boolean tryRelease(int arg) {  
            // 获取了锁，不用再和其它线程竞争  
            setExclusiveOwnerThread(null);  
            // state是volatile的，所以这里放在最后，让写屏障能影响前面所有操作，保证之前的设置对所有线程可见  
            setState(0);  
            return true;        }  
  
        // 是否持有独占锁  
        @Override  
        protected boolean isHeldExclusively() {  
            return getState() == 1;  
        }  
  
        // 返回一个条件变量  
        public Condition newCondition() {  
            // AQS提供的一个内部类，可以直接使用  
            return new ConditionObject();  
        }  
    }  
  
    private MySync sync = new MySync();  
  
    // 下面的抽象方法自己实现比较繁琐  
    // 就可以利用同步器类，AQS实现了大部分方法  
  
    // 加锁（尝试加锁，失败会进入队列等待）  
    @Override  
    public void lock() {  
        sync.acquire(1);  
    }  
  
    // 可打断加锁（加锁过程可打断）  
    @Override  
    public void lockInterruptibly() throws InterruptedException {  
        sync.acquireInterruptibly(1);  
    }  
  
    // 尝试加锁（尝试一次，失败直接返回false）  
    @Override  
    public boolean tryLock() {  
        return sync.tryAcquire(1);  
    }  
  
    // 带超时加锁  
    @Override  
    public boolean tryLock(long time, TimeUnit unit) throws InterruptedException {  
        return sync.tryAcquireNanos(1, unit.toNanos(time));  
    }  
  
    // 解锁  
    @Override  
    public void unlock() {  
        // 调用了tryRelease并唤醒正在阻塞的线程  
        sync.release(1);  
    }  
  
    // 创建条件变量  
    @Override  
    public Condition newCondition() {  
        return sync.newCondition();  
    }  
}
```











## 简介

AQS就是一个支持多个[[2_0_2-计算机科学/2_0_2_1_2_3-软件系统/2_0_2_1_2_3_1-操作系统/线程|线程]]进来排队的先进先出（FIFO）的双端队列，通过自身设计来实现多个线程到达总能按一定顺序进入队列，不会因为同时入队抢占发生问题。同时在头部保证有序的向目标资源进行访问（线程获取资源权限）。                    

**AQS**是`AbstractQueuedSynchronizer`的简称，即`抽象队列同步器`，从字面意思上理解:

- 抽象：抽象类，只实现一些主要逻辑，有些方法由子类实现；
- 队列：使用先进先出（FIFO）队列存储数据；
- 同步：实现了同步的功能。

AQS是一个用来构建锁和同步器的框架，使用AQS能简单且高效地构造出应用广泛的同步器，比如我们提到的ReentrantLock，Semaphore，ReentrantReadWriteLock，SynchronousQueue，FutureTask等等皆是基于AQS的。

当然，我们自己也能利用AQS非常轻松容易地构造出符合我们自己需求的同步器，只要子类实现它的几个`protected`方法就可以。

## AQS的数据结构

AQS内部使用了一个[[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/2_0_2_1_2_0_0-Java/2_0_2_1_2_0_0_1-高级特性/volatile|volatile]]的变量state来作为资源的标识。同时定义了几个获取和改变state的protected方法，子类可以覆盖这些方法来实现自己的逻辑：

```java
getState()
setState()
compareAndSetState()
```

这三种操作均是原子操作，其中compareAndSetState的实现依赖于Unsafe的compareAndSwapInt()方法。

而AQS类本身实现的是**一些排队和阻塞的机制**，比如具体线程等待队列的维护（如获取资源失败入队/唤醒出队等）。

1. 内部可以是一个先进先出（FIFO）的双端队列（CLH队列，（Craig, Landin, and Hagersten 队列）），并使用了两个指针head和tail用于标识队列的头部和尾部。其数据结构如图：
![[z-oblib/z2-attachments/AQS数据结构.png]]
但它并不是直接储存线程，而是**储存拥有线程的Node节点**，因为是一个双向链表的结构，所以最小单元是Node，Node会包含前后节点的地址，还包括一个线程。

2. 也可以是一个借助nextWaiter（见后续章节）实现的单向队列。

### 资源共享模式

> 一堆线程在排队等待资源，但资源可以同时只给一个线程用，或者支持多个线程同时用。

资源有两种共享模式，或者说两种同步方式：

- 独占模式（Exclusive）：资源是独占的，一次只能一个线程获取。如ReentrantLock。
- 共享模式（Share）：同时可以被多个线程获取，具体的资源个数可以通过参数指定。如Semaphore/CountDownLatch。

一般情况下，子类只需要根据需求实现其中一种模式，当然也有同时实现两种模式的同步类，如`ReadWriteLock`。

### Node结构

AQS中关于这两种资源共享模式的定义源码（均在内部类Node中）。我们来看看**Node的结构**：

```java
static final class Node {
    // 标记一个结点（对应的线程）在共享模式下等待
    static final Node SHARED = new Node();
    // 标记一个结点（对应的线程）在独占模式下等待
    static final Node EXCLUSIVE = null; 

    // waitStatus的值，表示该结点（对应的线程）已被取消
    static final int CANCELLED = 1; 
    // waitStatus的值，表示后继结点（对应的线程）需要被唤醒
    static final int SIGNAL = -1;
    // waitStatus的值，表示该结点（对应的线程）在等待某一条件
    static final int CONDITION = -2;
    /*waitStatus的值，表示有资源可用，新head结点需要继续唤醒后继结点（共享模式下，多线程并发释放资源，而head唤醒其后继结点后，需要把多出来的资源留给后面的结点；设置新的head结点时，会继续唤醒其后继结点）*/
    static final int PROPAGATE = -3;

    // 等待状态，取值范围，-3，-2，-1，0，1
    volatile int waitStatus;
    volatile Node prev; // 前驱结点
    volatile Node next; // 后继结点
    volatile Thread thread; // 结点对应的线程
    Node nextWaiter; // 在CLH队列时，表示共享式或独占式标记，在条件队列时，表示下一个Node节点


    // 判断共享模式的方法
    final boolean isShared() {
        return nextWaiter == SHARED;
    }

    Node(Thread thread, Node mode) {     // Used by addWaiter
        this.nextWaiter = mode;
        this.thread = thread;
    }

    // 其它方法忽略，可以参考具体的源码
}

// AQS里面的addWaiter私有方法
private Node addWaiter(Node mode) {
    // 使用了Node的这个构造函数
    Node node = new Node(Thread.currentThread(), mode);
    // 其它代码省略
}
```

注意：通过Node我们可以实现两个队列，一是通过prev和next实现CLH队列(线程同步队列,双向队列)，二是nextWaiter实现Condition条件上的等待线程队列(单向队列)，这个Condition主要用在ReentrantLock类中。

waitStatus等待状态如下：
![[z-oblib/z2-attachments/103e67d0d59543c4acfd4d0345dabfec.png]]

 **nextWaiter特殊标记**：
- Node在CLH队列时，nextWaiter表示共享式或独占式标记；
- Node在条件队列时，nextWaiter表示下个Node节点指针；

## AQS的主要方法源码解析

AQS的设计是基于[[2_0_2-计算机科学/2_0_2_1_2_1-软件方法学/设计模式/模板模式|模板模式]]的，它有一些方法必须要子类去实现的，它们主要有：

- isHeldExclusively()：该线程是否正在独占资源。只有用到condition才需要去实现它。
- tryAcquire(int)：独占方式。尝试获取资源，成功则返回true，失败则返回false。
- tryRelease(int)：独占方式。尝试释放资源，成功则返回true，失败则返回false。
- tryAcquireShared(int)：共享方式。尝试获取资源。负数表示失败；0表示成功，但没有剩余可用资源；正数表示成功，且有剩余资源。
- tryReleaseShared(int)：共享方式。尝试释放资源，如果释放后允许唤醒后续等待结点返回true，否则返回false。

> 子类需要实现在独占/共享模式下对资源的获取和释放的有针对性地逻辑部分。

这些方法虽然都是[[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/2_0_2_1_2_0_0-Java/2_0_2_1_2_0_0_0-语法基础/访问控制符#protected|protected]]方法，但是它们并没有在AQS具体实现，而是直接抛出异常（这里不使用抽象方法的目的是：避免强迫子类中把所有的抽象方法都实现一遍，减少无用功，这样子类只需要实现自己关心的抽象方法即可，比如 Semaphore 只需要实现 tryAcquire 方法而不用实现其余不需要用到的模版方法）：

> 而AQS实现了一系列（包括资源/释放）主要的逻辑。

### 线程排队

获取资源的入口是acquire(int arg)方法。arg是要获取的资源的个数，在独占模式下始终为1。我们先来看看这个方法的逻辑：

```java
public final void acquire(int arg) {
    if (!tryAcquire(arg) &&
        acquireQueued(addWaiter(Node.EXCLUSIVE), arg))
        selfInterrupt();
}
```

首先调用tryAcquire(arg)尝试去获取资源。前面提到了这个方法是在子类具体实现的。

如果获取资源失败，就通过addWaiter(Node.EXCLUSIVE)方法把这个线程插入到等待队列中。其中传入的参数代表要插入的Node是独占式的。这个方法的具体实现：

```java
private Node addWaiter(Node mode) {
    // 生成该线程对应的Node节点
    Node node = new Node(Thread.currentThread(), mode);
    // 获取尾节点
    Node pred = tail;
    // 如果前面还有其它节点
    if (pred != null) {
	    // 将当前节点地前驱节点设置为队尾节点
        node.prev = pred;
        // 使用CAS尝试将后继节点信息写入队尾节点，如果成功就返回
        // 使用CAS是为了处理多个线程同时想排队的情况
        if (compareAndSetTail(pred, node)) {
            pred.next = node;
            return node;
        }
    }
    // 如果等待队列为空或者上述CAS失败，再自旋CAS插入
    enq(node);
    return node;
}

// 自旋CAS插入等待队列
private Node enq(final Node node) {
    for (;;) {
        Node t = tail;
        // 如果等待队列为空
        if (t == null) { // Must initialize
	        // 创建一个空节点作为头节点（哨兵节点）
            if (compareAndSetHead(new Node()))
	            // 并把队尾指向队首，及队伍中现在只有一个空节点，队首队尾都指向这个节点
                tail = head;
        // 等待队列不为空
        } else {
	        // 使用CAS尝试将后继节点信息写入队尾节点，和之前函数一样，不过这里是在循环里一直去尝试
            node.prev = t;
            if (compareAndSetTail(t, node)) {
                t.next = node;
                return t;
            }
        }
    }
}
```

>上面的两个函数比较好理解，就是在队列的尾部插入新的Node节点，但是需要注意的是由于AQS中会存在多个线程同时争夺资源的情况，因此肯定会出现多个线程同时插入节点的操作，在这里是通过CAS自旋的方式保证了操作的线程安全性。

### 获取资源

OK，现在回到最开始的aquire(int arg)方法。现在通过addWaiter方法，已经把一个Node放到等待队列尾部了。而等待队列的头节点获取资源，而队列中节点会依次成为头节点。具体的实现我们来看看acquireQueued方法：

```java
final boolean acquireQueued(final Node node, int arg) {
    boolean failed = true;
    try {
	    // 设置中断状态为非中断
        boolean interrupted = false;
        // 自旋
        for (;;) {
            final Node p = node.predecessor();
            // 队首节点是当前已经获取到资源的结点或null，那么排在第二个位置的节点会循环尝试获取资源
            // 如果node的前驱结点p是head，表示node是第二个结点，就可以尝试去获取资源了
            if (p == head && tryAcquire(arg)) {
                // 拿到资源后，说明之前的头节点释放资源了，将head指向当前节点，把前任队首踢出队伍。
                setHead(node); 
                p.next = null; // 清空上一任头节点的后继节点信息，帮助JVM回收垃圾
                failed = false;
                return interrupted;
            }
            // 多次没获取到锁，可以休息了，就进入waiting状态，直到被unpark()
            if (shouldParkAfterFailedAcquire(p, node) &&
                parkAndCheckInterrupt())
                interrupted = true;
        }
    } finally {
        if (failed)
            cancelAcquire(node);
    }
}
```

> 这里parkAndCheckInterrupt方法内部使用到了LockSupport.park(this)，顺便简单介绍一下park。
> 
> LockSupport类是Java 6 引入的一个类，提供了基本的线程同步原语。LockSupport实际上是调用了Unsafe类里的函数，归结到Unsafe里，只有两个函数：
> 
> -   park(boolean isAbsolute, long time)：阻塞当前线程
> -   unpark(Thread jthread)：使给定的线程停止阻塞

所以**结点进入等待队列后，是调用park使它进入阻塞状态的。只有头结点的线程是处于活跃状态的**。

当然，获取资源的方法除了acquire外，还有以下三个：
- acquireInterruptibly：申请可中断的资源（独占模式）
- acquireShared：申请共享模式的资源
- acquireSharedInterruptibly：申请可中断的资源（共享模式）

> 可中断的意思是，在线程中断时可能会抛出`InterruptedException`。

![[z-oblib/z2-attachments/acquire流程.png]]

###  释放资源

```java
public final boolean release(int arg) {
    if (tryRelease(arg)) {
        Node h = head;
        if (h != null && h.waitStatus != 0)
            unparkSuccessor(h);
        return true;
    }
    return false;
}

// 传入的参数是头节点
private void unparkSuccessor(Node node) {
    // 如果状态是负数，尝试把它设置为0
    int ws = node.waitStatus;
    if (ws < 0)
        compareAndSetWaitStatus(node, ws, 0);
    // 得到头结点的后继结点head.next
    Node s = node.next;
    // 如果这个后继结点为空或者状态大于0
    // 通过前面的定义我们知道，大于0只有一种可能，就是这个结点已被取消
    if (s == null || s.waitStatus > 0) {
        s = null;  // 节点被取消则把节点删掉
        // 等待队列中所有还有用的结点，都向前移动
        // 从队尾向前遍历，取最靠近队首的未取消节点
        for (Node t = tail; t != null && t != node; t = t.prev)
            if (t.waitStatus <= 0)
                s = t;
    }
    // 如果后继结点不为空，
    if (s != null)
        LockSupport.unpark(s.thread);
}
```

