---
title: Thread
created: 2022-05-25 23:12:47
updated: 2022-05-26 09:31:13
tags: 
- atom
---
# Thread

Thread是一个实现了[[3-计算机科学/6-应用开发/0-软件语言/Java/2-并发编程/Runnable|Runnable]]接口的类，创建一个包含自定义任务的Thread对象有两种方式：
1. 通过继承Thread类并重写run()方法来实现。
2. 通过实例化Thread类时传入Runnable对象来实现。

可以用两种方式来实现因为Thread中默认的run()方法采用了代理的思想：

```java
@Override  
public void run() {  
    if (target != null) {  
        target.run();  
    }  
}
```

上述代码target就是传入的Runnable对象，如果没有传入，则需要继承Thread并重写该方法。这样的方式就能实现有两种方式来创建自己的Thread类。而通过把方法包装成Runnable对象再传递给Thread更加灵活，并且Runnable对[[3-计算机科学/6-应用开发/0-软件语言/Java/2-并发编程/线程池|线程池]]等高级API更加友好。这种思想也就是[[3-计算机科学/6-应用开发/0-软件语言/Java/1-高级特性/组合优于继承|组合优于继承]]。