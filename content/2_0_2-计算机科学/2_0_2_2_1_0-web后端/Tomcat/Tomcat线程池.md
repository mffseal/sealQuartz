---
title: Tomcat线程池
created: 2022-06-08 18:28:37
updated: 2022-06-08 21:00:59
tags: 
- #atom
---
# Tomcat线程池
> 合理的分工是实现高[[2_0_2-计算机科学/2_0_2_1_2_3-软件系统/2_0_2_1_2_3_1-操作系统/并发|并发]]的保障。

![[z-oblib/z2-attachments/Pasted image 20220608183846.png]]

> 分工的原因就是为了防止[[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/2_0_2_1_2_0_0-Java/2_0_2_1_2_0_0_2-并发编程/饥饿|饥饿]]，把

- LimitLatch 用来限流，可以控制最大连接个数，类似 J.U.C 中的  Semaphore 后面再讲
- Acceptor 只负责【接收新的 socket 连接】
- Poller 只负责监听 socket channel 是否有【可读的 I/O 事件】
- 一旦可读，封装一个任务对象（socketProcessor），提交给 Executor [[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/2_0_2_1_2_0_0-Java/2_0_2_1_2_0_0_2-并发编程/线程池|线程池]]处理
- Executor 线程池中的[[2_0_2-计算机科学/2_0_2_1_2_1-软件方法学/设计模式/工作线程|工作线程]]最终负责【处理请求】。

## 与JDK线程池差别

Tomcat 线程池扩展了 ThreadPoolExecutor，行为稍有不同：

- 如果总线程数达到 maximumPoolSize
	- 这时不会立刻抛 RejectedExecutionException 异常
	- 而是再次尝试将任务放入队列，如果还失败，才抛出 RejectedExecutionException 异常

```java
public void execute(Runnable command, long timeout, TimeUnit unit) {
    submittedCount.incrementAndGet();
    try {
	    // 先执行原生的execute
        super.execute(command);
    // 第一次失败不直接抛异常
    } catch (RejectedExecutionException rx) {
	    // 拿到任务队列
	    // TaskQueue是tomcat做过扩展的任务队列
        if (super.getQueue() instanceof TaskQueue) {
            final TaskQueue queue = (TaskQueue)super.getQueue();
            try {
                if (!queue.force(command, timeout, unit)) {
                    submittedCount.decrementAndGet();
                    throw new RejectedExecutionException("Queue capacity is full.");
                }
            } catch (InterruptedException x) {
                submittedCount.decrementAndGet();
                Thread.interrupted();
                throw new RejectedExecutionException(x);
            }
            } else {
            submittedCount.decrementAndGet();
            throw rx;
        }
 
    }
}
```

Connector 配置：
```java
public boolean force(Runnable o, long timeout, TimeUnit unit) throws InterruptedException {
    if ( parent.isShutdown() ) 
        throw new RejectedExecutionException(
            "Executor not running, can't force a command into the queue"
        );
    // 还是调用的offer
    return super.offer(o,timeout,unit); //forces the item onto the queue, to be used if the task 
is rejected
}
```

