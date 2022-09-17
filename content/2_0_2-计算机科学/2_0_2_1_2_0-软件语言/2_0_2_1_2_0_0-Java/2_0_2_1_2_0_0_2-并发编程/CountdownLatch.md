---
title: CountdownLatch
created: 2022-06-10 23:21:15
updated: 2022-06-22 20:51:07
tags: 
- #atom
---
# CountdownLatch

用来进行[[2_0_2-计算机科学/2_0_2_1_2_3-软件系统/2_0_2_1_2_3_1-操作系统/线程|线程]][[2_0_2-计算机科学/2_0_2_1_2_3-软件系统/2_0_2_1_2_3_1-操作系统/同步|同步]]协作，等待所有线程完成倒计时。
其中构造参数用来初始化等待计数值，await() 用来等待计数归零，countDown() 用来让计数减一

## 使用

### 基本流程

```java
public static void main(String[] args) throws InterruptedException {
    CountDownLatch latch = new CountDownLatch(3);
 
    new Thread(() -> {
        log.debug("begin...");
        sleep(1);
        latch.countDown();
        log.debug("end...{}", latch.getCount());
    }).start();
 
    new Thread(() -> {
        log.debug("begin...");
        sleep(2);
        latch.countDown();
        log.debug("end...{}", latch.getCount());
    }).start();
 
    new Thread(() -> {
        log.debug("begin...");
        sleep(1.5);
        latch.countDown();
        log.debug("end...{}", latch.getCount());
    }).start();
 
    log.debug("waiting...");
    latch.await();
    log.debug("wait end...");
}
```

>当然可以用[[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/2_0_2_1_2_0_0-Java/2_0_2_1_2_0_0_2-并发编程/join|join]]实现类似功能，但join是更底层的接口，使用起来比较繁琐。

### 配合线程池

[[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/2_0_2_1_2_0_0-Java/2_0_2_1_2_0_0_2-并发编程/线程池|线程池]]

```java
public static void main(String[] args) throws InterruptedException {
    CountDownLatch latch = new CountDownLatch(3);
    ExecutorService service = Executors.newFixedThreadPool(4);
    service.submit(() -> {
        log.debug("begin...");
        sleep(1);
        latch.countDown();
        log.debug("end...{}", latch.getCount());
    });
    service.submit(() -> {
        log.debug("begin...");
        sleep(1.5);
        latch.countDown();
        log.debug("end...{}", latch.getCount());
    });
    service.submit(() -> {
        log.debug("begin...");
        sleep(2);
        latch.countDown();
        log.debug("end...{}", latch.getCount());
    });
    service.submit(()->{
        try {
            log.debug("waiting...");
            latch.await();
            log.debug("wait end...");
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    });
}
```

## 原理

**CountDownLatch**是一种同步辅助，让我们多个线程执行任务时，需要等待线程执行完成后，才能执行下面的语句，之前线程操作时是使用`Thread.join`方法进行等待，**CountDownLatch**内部使用了[[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/2_0_2_1_2_0_0-Java/2_0_2_1_2_0_0_2-并发编程/AQS|AQS]]锁，其实内部有一个**state**字段，通过该字段来控制锁的操作。

**CountDownLatch**内部是将**state**作为计数器来使用，比如我们初始化时，**state**计数器为3，同时开启三个线程当有一个线程执行成功，每当有一个线程执行完成后就将**state**值减少1，直到减少到为0时，说明所有线程已经执行完毕。