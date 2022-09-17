---
title: ThreadPoolExecutor
created: 2022-06-07 22:55:23
updated: 2022-06-08 17:55:12
tags: 
- atom
---
# ThreadPoolExecutor

![[z-oblib/z2-attachments/Pasted image 20220607225611.png]]

## 线程池状态

ThreadPoolExecutor 使用 int 的高 3 位来表示[[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/Java/2-并发编程/线程池|线程池]]状态，低 29 位表示[[2_0_2-计算机科学/2_0_2_1_2_3-软件系统/2_0_2_1_2_3_1-操作系统/线程|线程]]数量：

| 状态名     | 高3位 | 接收新任务 | 处理阻塞队列任务 | 说明                                       |
| ---------- | ----- | ---------- | ---------------- | ------------------------------------------ |
| RUNNING    | 111   | Y          | Y                |                                            |
| SHUTDOWN   | 000   | N          | Y                | 不会接收新任务，但会处理阻塞队列剩余任务   |
| STOP       | 001   | N          | N                | 会中断正在执行的任务，并抛弃阻塞队列任务   |
| TIDYING    | 010   |            |                  | 任务全执行完毕，活动线程为 0 即将进入 终结 |
| TERMINATED | 011   |            |                  | 终结状态                                           |

从数字上比较，TERMINATED > TIDYING > STOP > SHUTDOWN > RUNNING。
> 有符号位，111为负数，所以RUNNING最小。

目的不主要是节约空间：这些信息存储在一个原子变量 ctl 中，目的是将线程池状态与线程个数合二为一，这样就可以用一次 [[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/Java/2-并发编程/CAS|cas]] 原子操作进行赋值。

```java
// c 为旧值， ctlOf 返回结果为新值
ctl.compareAndSet(c, ctlOf(targetState, workerCountOf(c))));
 
// rs 为高 3 位代表线程池状态， wc 为低 29 位代表线程个数，ctl 是合并它们
private static int ctlOf(int rs, int wc) { return rs | wc; }
```

## 构造方法

> 构造方法的参数决定了线程池的大多数行为。

```java
public ThreadPoolExecutor(int corePoolSize,
                          int maximumPoolSize,
                          long keepAliveTime,
                          TimeUnit unit,
                          BlockingQueue<Runnable> workQueue,
                          ThreadFactory threadFactory,
                          RejectedExecutionHandler handler)
```

- corePoolSize 核心线程数目 (最多保留的线程数)
- maximumPoolSize 最大线程数目
- keepAliveTime 生存时间 - 针对救急线程
- unit 时间单位 - 针对救急线程
- workQueue [[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/Java/2-并发编程/阻塞队列|阻塞队列]]
- threadFactory 线程工厂 - 可以为线程创建时起个好名字
- handler 拒绝策略
> 可以类比[[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/Java/2-并发编程/自定义线程池|自定义线程池]]中的相关设计思路。

### 线程工作方式

在核心线程都被占用的情况下，救急线程会出来执行任务，任务执行完后会销毁。
而核心线程在无任务的情况下不会销毁。

![[z-oblib/z2-attachments/Pasted image 20220607231221.png]]
![[z-oblib/z2-attachments/Pasted image 20220607231227.png]]

- 线程池中刚开始没有线程，当一个任务提交给线程池后，线程池会创建一个新线程来执行任务。
- 当线程数达到 corePoolSize 并没有线程空闲，这时再加入任务，新加的任务会被加入workQueue 队列排队，直到有空闲的线程。
- 如果队列选择了**有界队列**，那么任务超过了队列大小时，会创建 `maximumPoolSize - corePoolSize`数目的线程来**救急**。
	> 救急线程配合有界队列使用。
- 如果线程到达 `maximumPoolSize` 仍然有新任务这时会执行拒绝策略。
- JDK提供了4种拒绝策略：
	1. AbortPolicy 让调用者抛出RejectedExecutionException 异常，这是默认策略
	2. CallerRunsPolicy 让调用者运行任务
	3. DiscardPolicy 放弃本次任务
	4. DiscardOldestPolicy 放弃队列中最早的任务，本任务取而代之
- 其它著名框架也提供了拒绝策略实现：
	- Dubbo 的实现，在抛出 RejectedExecutionException 异常之前会记录日志，并 dump 线程栈信息，方便定位问题
	- Netty 的实现，是创建一个新线程来执行任务
	- ActiveMQ 的实现，带超时等待（60s）尝试放入队列，类似我们之前自定义的拒绝策略
	- PinPoint 的实现，它使用了一个拒绝策略链，会逐一尝试策略链中每种拒绝策略
- 当高峰过去后，超过corePoolSize 的救急线程如果一段时间没有任务做，需要结束节省资源，这个时间由keepAliveTime 和 unit 来控制。

![[z-oblib/z2-attachments/Pasted image 20220607231450.png]]

## 工厂方法

> 构造方法的参数太多，用起来可能比较麻烦，JDK又提供了工具类提供很多工厂方法，创建不同线程池，内部就是调用上述构造方法并传递不同参数。

根据这个构造方法，JDK Executors 类中提供了众多工厂方法来创建各种用途的线程池。

### newFixedThreadPool

```java
public static ExecutorService newFixedThreadPool(int nThreads) {
    return new ThreadPoolExecutor(nThreads, nThreads,
                                  0L, TimeUnit.MILLISECONDS,
                                  new LinkedBlockingQueue<Runnable>());
}
```

#### 特点

- 核心线程数 == 最大线程数（没有救急线程被创建），因此也无需超时时间
- 阻塞队列是无界的，可以放任意数量的任务

#### 使用场景

适用于任务量已知，相对耗时的任务。

### newCachedThreadPool

> 全员都是外包@华为

```java
public static ExecutorService newCachedThreadPool() {
    return new ThreadPoolExecutor(0, Integer.MAX_VALUE,
                                  60L, TimeUnit.SECONDS,
                                  new SynchronousQueue<Runnable>());
}
```

#### 特点

- 核心线程数是 0， 最大线程数是 Integer.MAX_VALUE，救急线程的空闲生存时间是 60s，意味着：
	- 全部都是救急线程（60s 后可以回收）
	- 救急线程可以无限创建
- 队列采用了 SynchronousQueue 实现特点是，它**没有容量**，没有线程来取是放不进去的（一手交钱、一手交货）
- 整个线程池表现为线程数会根据任务量不断增长，没有上限，当任务执行完毕，空闲 1分钟后释放线程。 

#### 使用场景

适合任务数比较**密集**，但每个任务**执行时间**较**短**的情况。

### newSingleThreadExecutor

```java
public static ExecutorService newSingleThreadExecutor() {
	// 没有直接返回线程池对象
	// 用装饰器模式进行了包装
	// 限制了返回对象能调用的方法
    return new FinalizableDelegatedExecutorService
        (new ThreadPoolExecutor(1, 1,
                                0L, TimeUnit.MILLISECONDS,
                                new LinkedBlockingQueue<Runnable>()));
}
```

#### 特点

- 健壮性：
	- 自己创建一个单线程串行执行任务，如果任务执行失败而终止那么没有任何补救措施，后续要创建的线程也无法执行。
	- 而线程池还会新建一个线程，保证池的正常工作，一个线程失败不影响后续线程执行。
- Executors.newSingleThreadExecutor() 线程个数始终为1
	- 线程数不能修改。
	- FinalizableDelegatedExecutorService 应用的是[[装饰器模式]]，只对外暴露了ExecutorService 接口，因此不能调用 ThreadPoolExecutor 中特有的方法，防止设置被修改。
- Executors.newFixedThreadPool(1) 初始时为1时和SingleThreadExecutor一样：
	- 线程数后续还可以修改。
	- 对外暴露的是 ThreadPoolExecutor 对象，可以强转后调用 setCorePoolSize 等方法进行修改核心线程数。

#### 使用场景

希望多个任务排队执行：线程数固定为 **1**，任务数多于 1 时，会放入**无界**队列排队。任务执行完毕，这唯一的线程也**不会**被释放。

## 提交任务

```java
// 执行任务
void execute(Runnable command);
 
// 提交任务 task，用返回值 Future 获得任务执行结果
// 保护性暂停模式
// 用来在主线程种接收线程池种线程返回的结果
<T> Future<T> submit(Callable<T> task);
 
// 提交 tasks 中所有任务
<T> List<Future<T>> invokeAll(Collection<? extends Callable<T>> tasks)
        throws InterruptedException;
 
// 提交 tasks 中所有任务，带超时时间
<T> List<Future<T>> invokeAll(Collection<? extends Callable<T>> tasks,
                                  long timeout, TimeUnit unit)
        throws InterruptedException;
 
// 提交 tasks 中所有任务，哪个任务先成功执行完毕，返回此任务执行结果，其它任务取消
<T> T invokeAny(Collection<? extends Callable<T>> tasks)

        throws InterruptedException, ExecutionException;
        // 提交 tasks 中所有任务，哪个任务先成功执行完毕，返回此任务执行结果，其它任务取消，带超时时间
<T> T invokeAny(Collection<? extends Callable<T>> tasks,
                    long timeout, TimeUnit unit)
        throws InterruptedException, ExecutionException, TimeoutException;
```

- submit的返回值靠[[2_0_2-计算机科学/2_0_2_1_2_1-软件方法学/设计模式/保护性暂停|保护性暂停]]实现，Future类似GuardedObject。

## 关闭线程池

### shutdown

```java
/*
线程池状态变为 SHUTDOWN
 - 不会接收新任务
 - 但已提交任务会执行完
 - 此方法不会阻塞调用线程的执行
*/
void shutdown();
```

```java
public void shutdown() {
    final ReentrantLock mainLock = this.mainLock;
    mainLock.lock();
    try {
        checkShutdownAccess();
        // 修改线程池状态
        advanceRunState(SHUTDOWN);
        // 仅会打断空闲线程
        interruptIdleWorkers();
        onShutdown(); // 扩展点 ScheduledThreadPoolExecutor
    } finally {
        mainLock.unlock();
    }
    // 尝试终结(没有运行的线程可以立刻终结，如果还有运行的线程也不会等)
    // 让那些还未结束的线程自灭，我不管了
    tryTerminate();
}
```

### shutdownNow

```java
/*
线程池状态变为 STOP
 - 不会接收新任务
 - 会将队列中的任务返回
 - 并用 interrupt 的方式中断正在执行的任务
*/
List<Runnable> shutdownNow();
```

```java
public List<Runnable> shutdownNow() {
List<Runnable> tasks;
    final ReentrantLock mainLock = this.mainLock;
    mainLock.lock();
    try {
        checkShutdownAccess();
        // 修改线程池状态
        advanceRunState(STOP);
        // 打断所有线程
        interruptWorkers();
        // 获取队列中剩余任务
        tasks = drainQueue();
    } finally {
        mainLock.unlock();
    }
    // 尝试终结
    tryTerminate();
    return tasks;
}
```

## 其它方法

```java
// 不在 RUNNING 状态的线程池，此方法就返回 true
boolean isShutdown();
 
// 线程池状态是否是 TERMINATED
boolean isTerminated();
 
// 调用 shutdown 后，由于调用线程并不会等待所有任务运行结束，因此如果它想在线程池 TERMINATED 后做些事情，可以利用此方法等待
// 等待线程全部结束或等待超时
boolean awaitTermination(long timeout, TimeUnit unit) throws InterruptedException;
```

## 任务异常处理

 ### 主动捕捉

```java
ExecutorService pool = Executors.newFixedThreadPool(1);
pool.submit(() -> {
    try {
        log.debug("task1");
        int i = 1 / 0;
    } catch (Exception e) {
        log.error("error:", e);
    }
});
```

### 使用Future

```java
ExecutorService pool = Executors.newFixedThreadPool(1);
Future<Boolean> f = pool.submit(() -> {
    log.debug("task1");
    int i = 1 / 0;
    return true;
});
log.debug("result:{}", f.get());
```

