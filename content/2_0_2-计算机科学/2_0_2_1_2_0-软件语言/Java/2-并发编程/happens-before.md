---
title: happens-before
created: 2022-05-01 14:38:54
updated: 2022-05-31 16:15:40
tags: 
- atom
---
# happens-before

## 什么是happens-before

**如果操作A happens-before操作B，那么操作A在内存上所做的操作对操作B都是可见的，不管它们在不在一个线程。**

一方面，程序员需要JMM提供一个强的内存模型来编写代码；另一方面，编译器和处理器希望JMM对它们的束缚越少越好，这样它们就可以最可能多的做优化来提高性能，希望的是一个弱的内存模型。

JMM考虑了这两种需求，并且找到了平衡点，对编译器和处理器来说，只要不改变程序的执行结果（单线程程序和正确同步了的多线程程序），编译器和处理器怎么优化都行。

而对于程序员，JMM提供了**happens-before规则**（JSR-133规范），满足了程序员的需求——简单易懂，并且提供了足够强的内存可见性保证。换言之，程序员只要遵循happens-before规则，那他写的程序就能保证在JMM中具有强的内存可见性。

JMM使用happens-before的概念来定制两个操作之间的执行顺序。这两个操作可以在一个线程以内，也可以是不同的线程之间。因此，JMM可以通过happens-before关系向程序员提供跨线程的内存可见性保证。

happens-before关系的定义如下：
1. 概念：如果一个操作happens-before另一个操作，那么第一个操作的执行结果将对第二个操作可见，而且第一个操作的执行顺序排在第二个操作之前。
2. 实际是结果为导向：两个操作之间存在happens-before关系，并不意味着Java平台的具体实现必须要按照happens-before关系指定的顺序来执行。**如果重排序之后的执行结果，与按happens-before关系来执行的结果一致，那么JMM也允许这样的重排序**。

>happens-before关系本质上和as-if-serial语义是一回事。
as-if-serial语义保证单线程内重排序后的执行结果和程序代码本身应有的结果是一致的，happens-before关系保证正确同步的多线程程序的执行结果不被重排序改变。

## 满足的几种情况

### synchronized

线程解锁 m 之前对变量的写，对于接下来对 m 加锁的其它线程对该变量的读可见：
```java
static int x;
static Object m = new Object();
 
new Thread(()->{
    synchronized(m) {
        x = 10;
        }
},"t1").start();
 
new Thread(()->{
    synchronized(m) {
        System.out.println(x);
    }
},"t2").start();
```

### volatile

线程对 volatile 变量的写，对**接下来**其它线程对该变量的读可见
```java
volatile static int x;
 
new Thread(()->{
    x = 10;
},"t1").start();
 
new Thread(()->{
    System.out.println(x);
},"t2").start();
```

### 线程启动前

线程 start 前对变量的写，对该线程开始后对该变量的读可见
```java
static int x;
 
x = 10;
 
new Thread(()->{
    System.out.println(x);
},"t2").start();
```

### 线程结束前
线程结束前对变量的写，对其它线程得知它结束后的读可见（比如其它线程调用 t1.isAlive() 或 t1.join()等待 它结束）
```java
static int x;
 
Thread t1 = new Thread(()->{
    x = 10;
},"t1");
t1.start();
 
t1.join();
System.out.println(x);
```

### 线程打断

线程 t1 打断 t2（interrupt）前对变量的写，对于其他线程得知 t2 被打断后对变量的读可见（通过 t2.interrupted 或 t2.isInterrupted）
```java
static int x;
 
public static void main(String[] args) {
    Thread t2 = new Thread(()->{
        while(true) {
            if(Thread.currentThread().isInterrupted()) {
                System.out.println(x);
                break;
            }
        }
    },"t2");
    t2.start();
 
    new Thread(()->{
        sleep(1);
        x = 10;
        t2.interrupt();
    },"t1").start();
 
    while(!t2.isInterrupted()) {
        Thread.yield();
    }
    System.out.println(x);
}
```

### 默认值

对变量默认值（0，false，null）的写，对其它线程对该变量的读可见

### 传递性

volatile的特性：
```java
volatile static int x;
static int y;
 
new Thread(()->{    
    y = 10;
    x = 20;
},"t1").start();
 
new Thread(()->{
    // x=20 对 t2 可见, 同时 y=10 也对 t2 可见
    System.out.println(x); 
},"t2").start();
```