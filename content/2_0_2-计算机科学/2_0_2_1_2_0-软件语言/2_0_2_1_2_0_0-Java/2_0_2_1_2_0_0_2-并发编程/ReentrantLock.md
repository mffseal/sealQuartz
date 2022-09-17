---
title: ReentrantLock
created: 2022-05-29 22:49:47
updated: 2022-06-10 21:21:06
tags: 
- atom
---
# ReentrantLock

> 相当于是一个java层面实现的[[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/2_0_2_1_2_0_0-Java/2_0_2_1_2_0_0_2-并发编程/monitor|monitor]]。

## 特点

相对于 [[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/2_0_2_1_2_0_0-Java/2_0_2_1_2_0_0_2-并发编程/synchronized|synchronized]] 它具备如下特点：
- 可中断（放弃争抢锁）
- 可以设置超时时间
- 可以设置为公平锁
	- 先到先得，而不是随机争抢
	- 解决线程[[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/2_0_2_1_2_0_0-Java/2_0_2_1_2_0_0_2-并发编程/饥饿|饥饿]]问题
- 支持多个条件变量
	- 条件变量相当于synchronized中的[[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/2_0_2_1_2_0_0-Java/2_0_2_1_2_0_0_2-并发编程/wait&notify|waitSet]]，不满足条件的可以在wait_set等待
	- 支持多个条件变量意味着有多个waitSet，可以根据不同条件进入不同set等待
- 与 synchronized 一样，都支持可重入

> state标识资源是否为锁定状态。

## 语法

```java
// 获取锁
reentrantLock.lock();
try {
    // 临界区
} finally {
    // 释放锁
    reentrantLock.unlock();
}
```

> 阿里手册：reentrantLock.lock()放在try外。

要保证：
- lock/unlock成对出现
- unlock在finally中执行

## 特性

### 可重入

synchronized(对象)中对象的作用实际上是一个指针，关连（指向）了底层的monitor对象，而reentrantLock的对象本身就是类似一个Monitor的存在。

```java
static ReentrantLock lock = new ReentrantLock();
 
public static void main(String[] args) {
    method1();
}
 
public static void method1() {
    lock.lock();
    try {
        log.debug("execute method1");
        method2();
    } finally {
        lock.unlock();
    }
}
 
public static void method2() {
    lock.lock();
    try {
        log.debug("execute method2");
        method3();
    } finally {
        lock.unlock();
    }
}
 
public static void method3() {
    lock.lock();
    try {
        log.debug("execute method3");
    } finally {
        lock.unlock();
    }
}
```

- 当lock.lock()成功，则当前线程成为lock的owner
- 当lock.lock()失败，当前线程会被加入到lock的等待队列中

### 可打断

> 被动避免死等

等待锁的过程中，其它[[2_0_2-计算机科学/2_0_2_1_2_3-软件系统/2_0_2_1_2_3_1-操作系统/线程|线程]]可以用interrupt()终止我的等待。

```java
ReentrantLock lock = new ReentrantLock();
 
Thread t1 = new Thread(() -> {
log.debug("启动...");
    try {
        lock.lockInterruptibly();
    } catch (InterruptedException e) {
        e.printStackTrace();
        log.debug("等锁的过程中被打断");
        return;
    }
    try {
        log.debug("获得了锁");
    } finally {
        lock.unlock();
    }
}, "t1");
 
 
lock.lock();
log.debug("Main获得了锁");
t1.start();
try {
    sleep(1);
    t1.interrupt();
    log.debug("执行打断");
} finally {
    lock.unlock();
}
```

### 锁超时

>主动避免死等

```java
ReentrantLock lock = new ReentrantLock();
Thread t1 = new Thread(() -> {
    log.debug("启动...");
    if (!lock.tryLock()) {
        log.debug("获取立刻失败，返回");
        return;
    }
    try {
        log.debug("获得了锁");
    } finally {
        lock.unlock();
    }
}, "t1");
 
lock.lock();
log.debug("获得了锁");
t1.start();
try {
    sleep(2);
} finally {
    lock.unlock();
}
```

### 公平锁

>不公平：新线程会无视队列尝试获取一次锁，失败则进入等待队列。等待队列中的线程还是有序唤醒的。
>公平锁一般没有必要，会降低[[2_0_2-计算机科学/2_0_2_1_2_3-软件系统/2_0_2_1_2_3_1-操作系统/并发|并发]]性能。

### 条件变量

- synchronized 中也有条件变量，就是我们讲原理时那个 waitSet 休息室，当条件不满足时进入 waitSet 等待
- ReentrantLock 的条件变量比 synchronized 强大之处在于，它是支持多个条件变量的，这就好比
	- synchronized 是那些不满足条件的线程都在一间休息室等消息
	- 而 ReentrantLock 支持多间休息室，有专门等烟的休息室、专门等早餐的休息室、唤醒时也是按休息室来唤醒

使用要点：
- await 前需要获得锁
- await 执行后，会释放锁，进入 conditionObject 等待
- await 的线程被唤醒（或打断、或超时）取重新竞争 lock 锁
- 竞争 lock 锁成功后，从 await 后继续执行

```java
static ReentrantLock lock = new ReentrantLock();
static Condition waitCigaretteQueue = lock.newCondition();
static Condition waitbreakfastQueue = lock.newCondition();
static volatile boolean hasCigrette = false;
static volatile boolean hasBreakfast = false;
 
public static void main(String[] args) {
    new Thread(() -> {
        try {
            lock.lock();
            while (!hasCigrette) {
            try {
                    waitCigaretteQueue.await();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
            log.debug("等到了它的烟");
        } finally {
            lock.unlock();
        }
    }).start();
 
    new Thread(() -> {
        try {
            lock.lock();
            while (!hasBreakfast) {
                try {
                    waitbreakfastQueue.await();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
            log.debug("等到了它的早餐");
        } finally {
            lock.unlock();
        }
    }).start();
 
    sleep(1);
    sendBreakfast();
    sleep(1);
    sendCigarette();
}
 
private static void sendCigarette() {
    lock.lock();
    try {
        log.debug("送烟来了");
        hasCigrette = true;
        waitCigaretteQueue.signal();
    } finally {
        lock.unlock();
    }
}
 
private static void sendBreakfast() {
    lock.lock();
    try {
        log.debug("送早餐来了");
        hasBreakfast = true;
        waitbreakfastQueue.signal();
    } finally {

        lock.unlock();
        }
}
```

## 原理

> 头节点必定是一个线程为null的哨兵节点，防止等待队列被删到空。

### 非公平

![[z-oblib/z2-attachments/Pasted image 20220609203458.png]]

#### 加解锁流程

从构造器开始看，默认为非公平锁实现：

```java
public ReentrantLock() {
    sync = new NonfairSync();
}
```

> NonfairSync 继承自 AQS。

无竞争时：

![[z-oblib/z2-attachments/Pasted image 20220609210612.png]]

出现第一个竞争：

![[z-oblib/z2-attachments/Pasted image 20220609210641.png]]

Thread-1 执行了：
1. CAS 尝试将 state 由 0 改为 1，结果失败
2. 进入 tryAcquire 逻辑，这时 state 已经是1，结果仍然失败
3. 接下来进入 addWaiter 逻辑，构造 Node 队列
	- 图中黄色三角表示该 Node 的 waitStatus 状态，其中 0 为默认正常状态
	- Node 的创建是懒惰的
	- 其中第**一**个 Node 称为 Dummy（哑元）或哨兵，用来占位，并不关联线程

> 哨兵节点当作是一个一直存在的等待队列头节点。作用是防止等待队列被删到空。
> 因为出队和入队可能同时发生，如果队列长度是1，此时把头节点直接删掉，可能导致新加到队尾的节点链到了错误的前驱节点，造成空指针异常。
> 所以将废弃的节点值置为null，当作新的头节点（哨兵节点），而不是直接删除。

![[z-oblib/z2-attachments/Pasted image 20220609211231.png]]

当前线程进入 **acquireQueued** 逻辑：
1. acquireQueued 会在一个死循环中不断尝试获得锁，失败后进入 park 阻塞
2. 如果自己是紧邻着 head（排第**二**位），那么再次 tryAcquire 尝试获取锁，当然这时 state 仍为 1，失败
3. 进入 shouldParkAfterFailedAcquire 逻辑，将前驱 node，即 head 的 waitStatus 改为 -1，这次返回 false
![[z-oblib/z2-attachments/Pasted image 20220609211430.png]]
4. shouldParkAfterFailedAcquire 执行完毕回到 acquireQueued ，再次 tryAcquire 尝试获取锁，当然这时 state 仍为 1，失败
5. 当再次进入 shouldParkAfterFailedAcquire 时，这时因为其前驱 node 的 waitStatus 已经是 -1，这次返回 true
6. 进入 parkAndCheckInterrupt， Thread-1 park（灰色表示）

![[z-oblib/z2-attachments/Pasted image 20220609211502.png]]
再次有多个线程经历上述过程竞争失败，变成这个样子
![[z-oblib/z2-attachments/Pasted image 20220609211515.png]]
Thread-0 释放锁，进入 tryRelease 流程，如果成功
- 设置 exclusiveOwnerThread 为 null
- state = 0

![[z-oblib/z2-attachments/Pasted image 20220609211528.png]]
当前队列不为 null，并且 head 的 waitStatus = -1，进入 unparkSuccessor 流程
找到队列中离 head 最近的一个 Node（没取消的），unpark 恢复其运行，本例中即为 Thread-1
回到 Thread-1 的 acquireQueued 流程

![[z-oblib/z2-attachments/Pasted image 20220609211542.png]]
如果加锁成功（没有竞争），会设置
- exclusiveOwnerThread 为 Thread-1，state = 1
- head 指向刚刚 Thread-1 所在的 Node，该 Node 清空 Thread
> 清空后，Thread-1节点被当作新的哨兵节点
- 原本的 head 因为从链表断开，而可被垃圾回收
如果这时候有其它线程来竞争（非公平的体现），例如这时有 Thread-4 来了

![[z-oblib/z2-attachments/Pasted image 20220609211557.png]]
如果不巧又被 Thread-4 占了先
- Thread-4 被设置为 exclusiveOwnerThread，state = 1
- Thread-1 再次进入 acquireQueued 流程，获取锁失败，重新进入 park 阻塞

#### 加锁源码

```java
// Sync 继承自 AQS
static final class NonfairSync extends Sync {
    private static final long serialVersionUID = 7316153563782823691L;
    
    // 加锁实现
    final void lock() {
        // 首先用 cas 尝试（仅尝试一次）将 state 从 0 改为 1, 如果成功表示获得了独占锁
        if (compareAndSetState(0, 1))
            setExclusiveOwnerThread(Thread.currentThread());
        else
            // 如果尝试失败，进入 ㈠
            acquire(1);
    }
    
    // ㈠ AQS 继承过来的方法, 方便阅读, 放在此处
    public final void acquire(int arg) {
        // ㈡ tryAcquire        
        if (
            !tryAcquire(arg) && 
            // 当 tryAcquire 返回为 false 时, 先调用 addWaiter ㈣, 接着 acquireQueued ㈤
            acquireQueued(addWaiter(Node.EXCLUSIVE), arg)
        ) {
            selfInterrupt();
        }
    }
    
    // ㈡ 进入 ㈢
    protected final boolean tryAcquire(int acquires) {
        return nonfairTryAcquire(acquires);
    }
    
    // ㈢ Sync 继承过来的方法, 方便阅读, 放在此处
    final boolean nonfairTryAcquire(int acquires) {
        final Thread current = Thread.currentThread();
        int c = getState();
        // 如果还没有获得锁
        if (c == 0) {
            // 尝试用 cas 获得, 这里体现了非公平性: 不去检查 AQS 队列
            if (compareAndSetState(0, acquires)) {
                setExclusiveOwnerThread(current);
                return true;
            }
        }
        // 如果已经获得了锁, 线程还是当前线程, 表示发生了锁重入
        else if (current == getExclusiveOwnerThread()) {
            // state++
            int nextc = c + acquires;
            if (nextc < 0) // overflow
                throw new Error("Maximum lock count exceeded");
            setState(nextc);
            return true;
        }
        // 获取失败, 回到调用处
        return false;
    }
    
    // ㈣ AQS 继承过来的方法, 方便阅读, 放在此处

    private Node addWaiter(Node mode) {
    // 将当前线程关联到一个 Node 对象上, 模式为独占模式
        Node node = new Node(Thread.currentThread(), mode);
        // 如果 tail 不为 null, cas 尝试将 Node 对象加入 AQS 队列尾部
        Node pred = tail;
        if (pred != null) {
            node.prev = pred;
            if (compareAndSetTail(pred, node)) {
                // 双向链表
                pred.next = node;
                return node;
            }
        }
        // 尝试将 Node 加入 AQS, 进入 ㈥
        enq(node);
        return node;
    }
    
    // ㈥ AQS 继承过来的方法, 方便阅读, 放在此处
    private Node enq(final Node node) {
        for (;;) {
            Node t = tail;
            if (t == null) {
                // 还没有, 设置 head 为哨兵节点（不对应线程，状态为 0）
                if (compareAndSetHead(new Node())) {
                    tail = head;
                }
            } else {
                // cas 尝试将 Node 对象加入 AQS 队列尾部
                node.prev = t;
                if (compareAndSetTail(t, node)) {
                    t.next = node;
                    return t;
                }
            }
        }
    }
    
    // ㈤ AQS 继承过来的方法, 方便阅读, 放在此处
    final boolean acquireQueued(final Node node, int arg) {
        boolean failed = true;
        try {
            boolean interrupted = false;
            for (;;) {
                final Node p = node.predecessor();
                // 上一个节点是 head, 表示轮到自己（当前线程对应的 node）了, 尝试获取
                if (p == head && tryAcquire(arg)) {
                    // 获取成功, 设置自己（当前线程对应的 node）为 head
                    setHead(node);
                    // 上一个节点 help GC
                    p.next = null;
                    failed = false;
                    // 返回中断标记 false

                    return interrupted;
                    }
                if (
                    // 判断是否应当 park, 进入 ㈦
                    shouldParkAfterFailedAcquire(p, node) &&
                    // park 等待, 此时 Node 的状态被置为 Node.SIGNAL ㈧
                    parkAndCheckInterrupt()
                ) {
                    interrupted = true;
                }
            }
        } finally {
            if (failed)
                cancelAcquire(node);
        }
    }
    
    // ㈦ AQS 继承过来的方法, 方便阅读, 放在此处
    private static boolean shouldParkAfterFailedAcquire(Node pred, Node node) {
        // 获取上一个节点的状态
        int ws = pred.waitStatus;
        if (ws == Node.SIGNAL) {
            // 上一个节点都在阻塞, 那么自己也阻塞好了
            return true;
        }
        // > 0 表示取消状态
        if (ws > 0) {
            // 上一个节点取消, 那么重构删除前面所有取消的节点, 返回到外层循环重试
            do {
                node.prev = pred = pred.prev;
            } while (pred.waitStatus > 0);
            pred.next = node;
        } else {
            // 这次还没有阻塞
            // 但下次如果重试不成功, 则需要阻塞，这时需要设置上一个节点状态为 Node.SIGNAL
            compareAndSetWaitStatus(pred, ws, Node.SIGNAL);
        }
        return false;
    }
    
    // ㈧ 阻塞当前线程
    private final boolean parkAndCheckInterrupt() {
        LockSupport.park(this);
        return Thread.interrupted();
    }
}
```

>是否需要 unpark 是由当前节点的**前驱**节点的 waitStatus == Node.SIGNAL 来决定，而不是本节点的  waitStatus 决定

#### 解锁源码

```java
// Sync 继承自 AQS
static final class NonfairSync extends Sync {
    // 解锁实现
    public void unlock() {
        sync.release(1);
    }
    
    // AQS 继承过来的方法, 方便阅读, 放在此处
    public final boolean release(int arg) {
        // 尝试释放锁, 进入 ㈠
        if (tryRelease(arg)) {
            // 队列头节点 unpark
            Node h = head;            
            if (
                // 队列不为 null
                h != null && 
                // waitStatus == Node.SIGNAL 才需要 unpark
                h.waitStatus != 0
            ) {
                // unpark AQS 中等待的线程, 进入 ㈡
                unparkSuccessor(h);
            }
            return true;
        }
        return false;
    }
    
    // ㈠ Sync 继承过来的方法, 方便阅读, 放在此处
    protected final boolean tryRelease(int releases) {
        // state--
        int c = getState() - releases;
        if (Thread.currentThread() != getExclusiveOwnerThread())
            throw new IllegalMonitorStateException();
        boolean free = false;
        // 支持锁重入, 只有 state 减为 0, 才释放成功
        if (c == 0) {
            free = true;
            setExclusiveOwnerThread(null);
        }
        setState(c);
        return free;
    }
    
    // ㈡ AQS 继承过来的方法, 方便阅读, 放在此处
    private void unparkSuccessor(Node node) {
        // 如果状态为 Node.SIGNAL 尝试重置状态为 0
        // 不成功也可以
        int ws = node.waitStatus;
        if (ws < 0) {
            compareAndSetWaitStatus(node, ws, 0);
        }
 
        // 找到需要 unpark 的节点, 但本节点从 AQS 队列中脱离, 是由唤醒节点完成的
        Node s = node.next;
        // 不考虑已取消的节点, 从 AQS 队列从后至前找到队列最前面需要 unpark 的节点
        if (s == null || s.waitStatus > 0) {
            s = null;
            for (Node t = tail; t != null && t != node; t = t.prev)
                if (t.waitStatus <= 0)
                    s = t;
        }
        if (s != null)
            LockSupport.unpark(s.thread);
    }
}
```

### 可重入

```java
static final class NonfairSync extends Sync {
    // ...
    
    // Sync 继承过来的方法, 方便阅读, 放在此处
    final boolean nonfairTryAcquire(int acquires) {
        final Thread current = Thread.currentThread();
        int c = getState();
        if (c == 0) {
            if (compareAndSetState(0, acquires)) {
                setExclusiveOwnerThread(current);
                return true;
            }
        }
        // 如果已经获得了锁, 线程还是当前线程, 表示发生了锁重入
        else if (current == getExclusiveOwnerThread()) {
            // state++
            int nextc = c + acquires;
            if (nextc < 0) // overflow
                throw new Error("Maximum lock count exceeded");
            setState(nextc);
            return true;
        }
        return false;
    }
    
    // Sync 继承过来的方法, 方便阅读, 放在此处
    protected final boolean tryRelease(int releases) {
        // state--(releases==1) 
        int c = getState() - releases;
        if (Thread.currentThread() != getExclusiveOwnerThread())
            throw new IllegalMonitorStateException();
        boolean free = false;  // 只减计数，未释放锁
        // 支持锁重入, 只有 state 减为 0, 才释放成功
        if (c == 0) {
            free = true;
            setExclusiveOwnerThread(null);
        }
        setState(c);
        return free;
    }
}
```

### 不可打断

> 默认的模式。

在此模式下，即使它被打断，仍会驻留在 AQS 队列中，一直要等到获得锁后方能得知自己被打断了：

```java
// Sync 继承自 AQS
static final class NonfairSync extends Sync {
    // ...
    
    private final boolean parkAndCheckInterrupt() {
        // 如果打断标记已经是 true, 则 park 会失效
        LockSupport.park(this);
        // 返回是否被打断过，interrupted 会清除打断标记（为了二次park不受标记影响）
        return Thread.interrupted();
    }
	// 线程没法立刻获得锁时，会进入该方法
    final boolean acquireQueued(final Node node, int arg) {
        boolean failed = true;
        try {
            boolean interrupted = false;
            for (;;) {
                final Node p = node.predecessor();
                if (p == head && tryAcquire(arg)) {
                    setHead(node);
                    p.next = null;
                    failed = false;
                    // 还是需要获得锁后, 才能返回打断状态（返回到acquire里）
                    return interrupted;
                }
                if (
                    shouldParkAfterFailedAcquire(p, node) &&
                    parkAndCheckInterrupt()
                ) {
                    // 如果是因为 interrupt 被唤醒, 返回打断状态为 true
                    interrupted = true;
                    // 但是没有做其它处理，还是会进入循环
                    // 循环中还是会去尝试获取锁，进入park阻塞
                }
            }
        } finally {
            if (failed)
                cancelAcquire(node);
        }
    }
    

    public final void acquire(int arg) {
    if (
            !tryAcquire(arg) && 
            // 前面函数被打断后返回到这里
            acquireQueued(addWaiter(Node.EXCLUSIVE), arg)
        ) {
            // 如果打断状态为 true，会执行下属方法
            // 重新产生一次中断
            selfInterrupt();
        }
    }
    
    static void selfInterrupt() {
        // 重新产生一次中断
        Thread.currentThread().interrupt();
    }
}
```

### 可打断

```java
static final class NonfairSync extends Sync {
    public final void acquireInterruptibly(int arg) throws InterruptedException {
        if (Thread.interrupted())
            throw new InterruptedException();
        // 如果没有获得到锁, 进入 ㈠
        if (!tryAcquire(arg))
            doAcquireInterruptibly(arg);
    }
    
    // ㈠ 可打断的获取锁流程
    private void doAcquireInterruptibly(int arg) throws InterruptedException {
        final Node node = addWaiter(Node.EXCLUSIVE);
        boolean failed = true;
        try {
            for (;;) {
                final Node p = node.predecessor();
                if (p == head && tryAcquire(arg)) {
                    setHead(node);
                    p.next = null; // help GC
                    failed = false;
                    return;
                }
                if (shouldParkAfterFailedAcquire(p, node) &&
                    parkAndCheckInterrupt()) {
                    // 在 park 过程中如果被 interrupt 会进入此
                    // 这时候抛出异常, 而不会再次进入 for (;;)
                    throw new InterruptedException();
                    // 不会再进入for循环等待
                }
            }
        } finally {
            if (failed)
                cancelAcquire(node);
        }
    }
}
```

### 非公平锁



### 公平锁

> 先检查等待队列是否为空，而不是上来就CAS抢占锁。

```java
static final class FairSync extends Sync {
    private static final long serialVersionUID = -3000897897090466540L;
 
    final void lock() {
        acquire(1);
    }
    
    // AQS 继承过来的方法, 方便阅读, 放在此处
    public final void acquire(int arg) {
        if (
            !tryAcquire(arg) && 
            acquireQueued(addWaiter(Node.EXCLUSIVE), arg)
        ) {
            selfInterrupt();
        }
    }
 
    // 与非公平锁主要区别在于 tryAcquire 方法的实现
    protected final boolean tryAcquire(int acquires) {
        final Thread current = Thread.currentThread();
        int c = getState();
        if (c == 0) {
            // 先检查 AQS 队列中是否有前驱节点, 没有才去竞争
            // 而不是上来就尝试CAS
            if (!hasQueuedPredecessors() &&
                compareAndSetState(0, acquires)) {
                setExclusiveOwnerThread(current);
                return true;
            }
        }
        else if (current == getExclusiveOwnerThread()) {
            int nextc = c + acquires;
            if (nextc < 0)
                throw new Error("Maximum lock count exceeded");
            setState(nextc);
            return true;
        }
        return false;
    }
    
    // ㈠ AQS 继承过来的方法, 方便阅读, 放在此处
    public final boolean hasQueuedPredecessors() {
        Node t = tail;
        Node h = head;
        Node s;
        // h != t 时表示队列中有 Node
        return h != t &&
            (
	            // 老大是占位用的节点
                // (s = h.next) == null 表示队列中还有没有老二
                (s = h.next) == null || 
                // 或者队列中老二线程不是此线程
                s.thread != Thread.currentThread()
            );
    }
}
```

### 条件变量

每个条件变量其实就对应着一个等待队列，其实现类是 ConditionObject:

#### await流程

开始 Thread-0 持有锁，调用 await，进入 ConditionObject 的 addConditionWaiter 流程。
创建新的 Node 状态为 -2（Node.CONDITION），关联 Thread-0，加入等待队列尾部。

![[z-oblib/z2-attachments/Pasted image 20220609233958.png]]

接下来进入 AQS 的 fullyRelease 流程，释放同步器上的锁：
>fullyRelease是释放掉重入的锁。

![[z-oblib/z2-attachments/Pasted image 20220609234005.png]]

当前线程释放锁，unpark AQS 队列中的下一个节点，竞争锁，假设没有其他竞争线程，那么 Thread-1 竞争成功：

![[z-oblib/z2-attachments/Pasted image 20220609234027.png]]

park 阻塞 Thread-0：

![[z-oblib/z2-attachments/Pasted image 20220609234041.png]]

```java
public final void await() throws InterruptedException {  
    if (Thread.interrupted())  
        throw new InterruptedException();  
    Node node = addConditionWaiter();  
    // fullyRelease作用是可以释放掉重入的锁
    int savedState = fullyRelease(node);  
    int interruptMode = 0;  
    while (!isOnSyncQueue(node)) {  
	    // 阻塞自己， 等待被唤醒
        LockSupport.park(this);  
        if ((interruptMode = checkInterruptWhileWaiting(node)) != 0)  
            break;  
    }  
    if (acquireQueued(node, savedState) && interruptMode != THROW_IE)  
        interruptMode = REINTERRUPT;  
    if (node.nextWaiter != null) // clean up if cancelled  
        unlinkCancelledWaiters();  
    if (interruptMode != 0)  
        reportInterruptAfterWait(interruptMode);  
}
```