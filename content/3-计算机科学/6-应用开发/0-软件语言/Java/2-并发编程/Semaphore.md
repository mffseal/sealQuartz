---
title: Semaphore
created: 2022-06-10 22:33:55
updated: 2022-06-10 23:12:22
tags: 
- atom
---
# Semaphore

[ˈsɛməˌfɔr] 信号量，用来限制能同时访问共享资源的[[3-计算机科学/2-计算机组成原理/线程|线程]]上限。

## 应用

- 使用 Semaphore 限流，在访问高峰期时，让请求线程阻塞，高峰期过去再释放许可，当然它只适合限制单机线程数量，并且仅是限制线程数，而不是限制资源数（例如连接数，请对比 Tomcat LimitLatch 的实现）
- 用  Semaphore 实现简单连接池，对比『[[3-计算机科学/6-应用开发/1-软件方法学/设计模式/享元模式|享元模式]]』下的实现（用wait notify），性能和可读性显然更好，注意下面的实现中线程数和数据库连接数是相等的

### 简化连接池

一种享元模式应用。

```java
class Pool {
    // 1. 连接池大小
    private final int poolSize;
 
    // 2. 连接对象数组
    private Connection[] connections;
 
    // 3. 连接状态数组 0 表示空闲， 1 表示繁忙
    private AtomicIntegerArray states;
 
    private Semaphore semaphore;
    // 4. 构造方法初始化
    public Pool(int poolSize) {
        this.poolSize = poolSize;
        // 让许可数与资源数一致
        this.semaphore = new Semaphore(poolSize);
        this.connections = new Connection[poolSize];
        this.states = new AtomicIntegerArray(new int[poolSize]);
        for (int i = 0; i < poolSize; i++) {
            connections[i] = new MockConnection("连接" + (i+1));
        }
    }
 
    // 5. 借连接
    public Connection borrow() {// t1, t2, t3
        // 获取许可
        try {
            semaphore.acquire(); // 没有许可的线程，在此等待
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        for (int i = 0; i < poolSize; i++) {
            // 获取空闲连接
            if(states.get(i) == 0) {
                if (states.compareAndSet(i, 0, 1)) {
                    log.debug("borrow {}", connections[i]);
                    return connections[i];
                }
            }
        }
        // 不会执行到这里
        return null;
    }
    // 6. 归还连接
    public void free(Connection conn) {
        for (int i = 0; i < poolSize; i++) {
            if (connections[i] == conn) {
                states.set(i, 0);
                log.debug("free {}", conn);
                semaphore.release();
                break;
            }
        }
    }
}
```

## 原理

### 加解锁流程

Semaphore 有点像一个停车场，permits 就好像停车位数量，当线程获得了 permits 就像是获得了停车位，然后停车场显示空余车位减一。

1. 刚开始，permits（state）为 3，这时 5 个线程来获取资源
![[z-oblib/z2-attachments/Pasted image 20220610231154.png]]
2. 假设其中 Thread-1，Thread-2，Thread-4 cas 竞争成功，而 Thread-0 和 Thread-3 竞争失败，进入 AQS 队列 park 阻塞
![[z-oblib/z2-attachments/Pasted image 20220610231219.png]]
3. 这时 Thread-4 释放了 permits，状态如下
