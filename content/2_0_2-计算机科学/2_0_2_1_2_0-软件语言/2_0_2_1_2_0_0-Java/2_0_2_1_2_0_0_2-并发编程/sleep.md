---
title: sleep
created: 2022-04-28 16:38:02
updated: 2022-05-26 14:46:12
tags: 
- atom
---
# sleep

sleep方法是Thread类的一个静态方法。它的作用是让当前线程睡眠一段时间，睡眠是指让线程放弃当前CPU的时间片，但是并不会释放锁，抱着锁睡觉。它有这样两个方法：

- Thread.sleep(long)
- Thread.sleep(long, int)

> 同样，查看源码(JDK 1.8)发现，第二个方法貌似只对第二个参数做了简单的处理，没有精确到纳秒。实际上还是调用的第一个方法。


## 作用

1. 调用 sleep 会让当前线程从 Running  进入 Timed Waiting 状态（阻塞）。
2. 其它线程可以使用 interrupt 方法打断正在睡眠的线程，这时 sleep 方法会抛出InterruptedException。
3. 睡眠结束后的线程未必会立刻得到执行。
4. 建议用 TimeUnit 的 sleep 代替 Thread 的 sleep 来获得更好的可读性。

## 打断睡眠（非唤醒）

sleep()是可以打断的，而打断的方式是通过InterruptedException异常，所以sleep()需要捉起来。

注意打断睡眠不是唤醒，不会继续做睡醒后要做的工作，而是直接通过异常处理跳出了。所以sleep()后的内容（try范围内）不会被执行。

相当于拔掉一个昏迷的人的氧气管，而不是叫醒他。

```java
Thread t4 = new Thread(){  
    @Override  
    public void run() {  
        log.debug("enter sleep...");  
        try {  
            Thread.sleep(2000);  
            log.debug("i'm awake");  // 这里不会执行  
        } catch (InterruptedException e) {  
            log.debug("fvck, who interrupting me");  // 这里会执行
            throw new RuntimeException(e);  
        }  
    }  
};
```