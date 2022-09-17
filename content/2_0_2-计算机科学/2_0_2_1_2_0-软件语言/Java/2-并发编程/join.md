---
title: join
created: 2022-04-28 16:37:26
updated: 2022-06-10 23:33:41
tags: 
- atom
---
# join

join()方法是Thread类的一个实例方法。让**当前**线程陷入等待，等待某个其它[[2_0_2-计算机科学/2_0_2_1_2_3-软件系统/2_0_2_1_2_3_1-操作系统/线程|线程]]运行结束，**谁调用就等待谁**，join起到了[[2_0_2-计算机科学/2_0_2_1_2_3-软件系统/2_0_2_1_2_3_1-操作系统/同步|同步]]的作用。

join()底层就是wait()。

有时候，主线程创建并启动了子线程，如果子线程中需要进行大量的耗时运算，主线程往往将早于子线程结束之前结束。

如果主线程想等待子线程执行完毕后，获得子线程中的处理完的某个数据，就要用到join方法了。

示例代码：

```java
public class Join {
    static class ThreadA implements Runnable {

        @Override
        public void run() {
            try {
                System.out.println("我是子线程，我先睡一秒");
                Thread.sleep(1000);
                System.out.println("我是子线程，我睡完了一秒");
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {
        Thread thread = new Thread(new ThreadA());
        thread.start();
        thread.join();
        System.out.println("如果不加join方法，我会先被打出来，加了就不一样了");
    }
}
```

> 注意join()方法有两个重载方法，一个是join(long)， 一个是join(long, int)。
> 
> 实际上，通过源码你会发现，join()方法及其重载方法底层都是利用了wait(long)这个方法。
> 
> 对于join(long, int)，通过查看源码(JDK 1.8)发现，底层并没有精确到纳秒，而是对第二个参数做了简单的判断和处理。

## 原理

底层设计模式是[[2_0_2-计算机科学/2_0_2_1_2_1-软件方法学/设计模式/保护性暂停|保护性暂停]]。

一个线程等待另一个线程的结束。

```java
public final synchronized void join(long millis)  
throws InterruptedException {  
    long base = System.currentTimeMillis();  // 获取当前时间
    long now = 0;  
	// 参数合法性判断
    if (millis < 0) {  
        throw new IllegalArgumentException("timeout value is negative");  
    }  
    
    if (millis == 0) {  
        while (isAlive()) {  
            wait(0);  
        }  
    } else {  
	    // 判断虚假唤醒
        while (isAlive()) {  
            long delay = millis - now;  // 更新还要等多久
            // 超时了就不再等了
            if (delay <= 0) {  
                break;  
            }  
            wait(delay);  // 如果被虚假唤醒，就重新进入wait并等待剩余时间
            now = System.currentTimeMillis() - base;  // 更新已经过了多久
        }  
    }  
}
```

isAlive()是本地方法，由子线程（被等待的线程）调用，判断子线程是否还活着。

在主线程中调用t1.join()[[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/Java/2-并发编程/synchronized#成员方法|同步方法]]，会**把t1当作锁对象**，而成功调用t1.join()代表主线程获取到了当前的t1锁对象，因此wait是针对主线程生效的。