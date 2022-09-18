---
title: Timer
created: 2022-06-08 17:05:32
updated: 2022-06-08 17:06:49
tags: 
- atom
---
# Timer

在[[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/Java/2-并发编程/任务调度线程池|任务调度线程池]]功能加入之前，可以使用 java.util.Timer 来实现定时功能，Timer 的优点在于简单易用，但 由于所有任务都是由**同一个**线程来调度，因此所有任务都是**串行**执行的，同一时间只能有一个任务在执行，前一个 任务的延迟或异常都将会影响到之后的任务。

```java
public static void main(String[] args) {
    Timer timer = new Timer();
    TimerTask task1 = new TimerTask() {
        @Override
        public void run() {
            log.debug("task 1");

            sleep(2);
            }
    };
    TimerTask task2 = new TimerTask() {
        @Override
        public void run() {
            log.debug("task 2");
        }
    };
    // 使用 timer 添加两个任务，希望它们都在 1s 后执行
    // 但由于 timer 内只有一个线程来顺序执行队列中的任务，因此『任务1』的延时，影响了『任务2』的执行
    timer.schedule(task1, 1000);
    timer.schedule(task2, 1000);
}
```

## 缺点

后一个线程的执行会受到前一个线程的影响：
- 开始时间会受制于前一个线程的执行时间。
- 前一个线程异常会影响后面的线程。