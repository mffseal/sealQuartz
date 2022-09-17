---
title: CAS与volatile
created: 2022-05-31 23:01:30
updated: 2022-06-01 17:49:08
tags: 
- atom
---
# CAS与volatile


## 用例

AtomicInteger 的解决方法，内部并没有用锁来保护共享[[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/Java/2-并发编程/变量的线程安全|变量的线程安全]]。那么它是如何实现的呢？

```java
public void withdraw(Integer amount) {
    while(true) {
        // 需要不断尝试，直到成功为止
        while (true) {
            // 比如拿到了旧值 1000
            int prev = balance.get();
            // 在这个基础上 1000-10 = 990
            int next = prev - amount;
            /*
        compareAndSet 正是做这个检查，在 set 前，先比较 prev 与当前值
        - 不一致了，next 作废，返回 false 表示失败
           比如，别的线程已经做了减法，当前值已经被减成了 990
           那么本[[2_0_2-计算机科学/2_0_2_1_2_3-软件系统/2_0_2_1_2_3_1-操作系统/线程|线程]]的这次 990 就作废了，进入 while 下次循环重试
        - 一致，以 next 设置为新值，返回 true 表示成功

        */
        if (balance.compareAndSet(prev, next)) {
                break;
            }
        }
    }
}
```

其中的关键是 compareAndSet，它的简称就是 [[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/Java/2-并发编程/CAS|CAS]] （也有 Compare And Swap 的说法），它必须是原子操作。
![[z-oblib/z2-attachments/Pasted image 20220531231303.png]]


### 慢动作分析

```java
@Slf4j
public class SlowMotion {
 
    public static void main(String[] args) {
        AtomicInteger balance = new AtomicInteger(10000);
        int mainPrev = balance.get();
        log.debug("try get {}", mainPrev);
 
        new Thread(() -> {
            sleep(1000);
            int prev = balance.get();
            balance.compareAndSet(prev, 9000);
            log.debug(balance.toString());
        }, "t1").start();
 
 
        sleep(2000);
        log.debug("try set 8000...");
        boolean isSuccess = balance.compareAndSet(mainPrev, 8000);
        log.debug("is success ? {}", isSuccess);
        if(!isSuccess){
            mainPrev = balance.get();
            log.debug("try set 8000...");
            isSuccess = balance.compareAndSet(mainPrev, 8000);
            log.debug("is success ? {}", isSuccess);
        }
 
    }
 
 
    private static void sleep(int millis) {
        try {
            Thread.sleep(millis);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
```

## volatile

获取共享变量时，为了保证该变量的[[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/Java/2-并发编程/可见性|可见性]]，需要使用 [[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/Java/1-高级特性/volatile|volatile]] 修饰。
它可以用来修饰成员变量和静态成员变量，他可以避免线程从自己的工作缓存中查找变量的值，必须到主存中获取它的值，线程操作 volatile 变量都是直接操作主存。即一个线程对 volatile 变量的修改，对另一个线程可见。
>注意：
>volatile 仅仅保证了共享变量的[[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/Java/2-并发编程/可见性|可见性]]，让其它线程能够看到最新值，但不能解决指令交错问题（不能保证原子性）。
[[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/Java/2-并发编程/CAS|CAS]] 必须借助 volatile 才能读取到共享变量的最新值来实现【比较并交换】的效果。

## 为什么无锁效率更高

- 无锁情况下，即使重试失败，线程始终在高速运行，没有停歇，而 [[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/Java/2-并发编程/synchronized|synchronized]] 会让线程在没有获得锁的时候，发生上下文切换，进入阻塞。打个比喻
- 线程就好像高速跑道上的赛车，高速运行时，速度超快，一旦发生[[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/Java/2-并发编程/上下文切换|上下文切换]]，就好比赛车要减速、熄火，等被唤醒又得重新打火、启动、加速... 恢复到高速运行，代价比较大
- 但无锁情况下，因为线程要保持运行，需要额外 CPU 的支持，CPU 在这里就好比高速跑道，没有额外的跑道，线程想高速运行也无从谈起，虽然不会进入阻塞，但由于没有分到时间片，仍然会进入可运行状态，还是会导致上下文切换。