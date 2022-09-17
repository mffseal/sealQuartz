---
title: interrupt
created: 2022-05-26 15:42:49
updated: 2022-05-26 17:12:27
tags: 
- atom
---
# interrupt

## 打断 sleep, wait, join 的线程

interrupt强行打断线程：

线程会记录本身是否被打断过，但是sleep, wait, join 以异常的方式响应interrupt后会清除异常标记，isInterrupted() == false。

```java
public static void main(String[] args) throws InterruptedException {  
    Thread t1 = new Thread(()->{  
        log.debug("sleep...");  
        try {  
            Thread.sleep(5000);  
        } catch (InterruptedException e) {  
            throw new RuntimeException(e);  
        }  
    });  
    t1.start();  
    Thread.sleep(500);  // 主线程等t1先睡着  
    t1.interrupt();  
    log.debug("打断标记：{}", t1.isInterrupted());  
}
```

## 打断正常运行的线程

interrupt让你自行了断：

对于正常运行的线程，interrupt主要是设置打断标记，由线程代码根据打断标记来抉择当前线程是要继续运行还是就此终止。

```java
public static void main(String[] args) throws InterruptedException {  
    Thread t1 = new Thread(()->{  
        while (true){  
            boolean interrupted = Thread.currentThread().isInterrupted();  
            if(interrupted) {  
                log.debug("我被打断了");  
                break;            }
        }  
    });  
    t1.start();  
    Thread.sleep(500);  
    log.debug("interrupt");  
    t1.interrupt();  
}
```

### 为什么会不一样

因为线程睡着的时候没法也不知道别人有没有打断他，线程没有在执行，所以由其他人强行把他杀了。

而线程没有睡着的时候，能感知到是否有别的线程在打断他，这样就能让线程自己自行了断，方便做一些善后处理。

## 打断park的线程

```java
private static void test3() throws InterruptedException {
    Thread t1 = new Thread(() -> {
        log.debug("park...");
        LockSupport.park();
        log.debug("unpark...");
        log.debug("打断状态：{}", Thread.currentThread().isInterrupted());
        LockSupport.park();  // 这里park不起效
    }, "t1");
    t1.start();

 
    sleep(0.5);
    t1.interrupt();
}
```

park只能在打断标记是false的时候起效果，isInterrupted不会重置打断标记，所以第二个park不起效。可以用interrupted重置打断标记。