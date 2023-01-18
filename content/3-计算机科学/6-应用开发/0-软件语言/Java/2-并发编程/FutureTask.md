---
title: FutureTask
created: 2022-05-26 09:55:56
updated: 2022-05-26 10:08:30
tags: 
- atom
---
# FutureTask

FutureTask 能够接收 [[3-计算机科学/6-应用开发/0-软件语言/Java/2-并发编程/Callable|Callable]] 类型的参数，用来处理有返回结果的情况。

```java
FutureTask<V> implements RunnableFuture<V>
interface RunnableFuture<V> extends Runnable, Future<V>  // Future.get()用来返回任务的返回值

```