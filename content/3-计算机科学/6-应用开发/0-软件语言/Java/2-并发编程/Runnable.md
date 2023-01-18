---
title: Runnable
created: 2022-05-25 22:30:42
updated: 2022-05-26 09:31:02
tags: 
- atom
---
# Runnable

用来承载供Thread对象执行的任务，将任务从Thread中抽出来可以更加灵活。

```java
Runnable runnable = () -> log.debug("runnable");  // lambda
Thread t2 = new Thread(runnable);
```

因为Runnable是一个@FunctionalInterface接口，所以可以通过[[3-计算机科学/6-应用开发/0-软件语言/Java/1-高级特性/lambda|lambda]]的形式实现。
通过把方法包装成Runnable更加灵活，并且Runnable对[[3-计算机科学/6-应用开发/0-软件语言/Java/2-并发编程/线程池|线程池]]等高级API更加友好。这种思想也就是[[3-计算机科学/6-应用开发/0-软件语言/Java/1-高级特性/组合优于继承|组合优于继承]]。