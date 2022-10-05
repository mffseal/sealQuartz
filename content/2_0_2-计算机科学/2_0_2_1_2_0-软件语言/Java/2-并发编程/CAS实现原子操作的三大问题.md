---
title: CAS实现原子操作的三大问题
created: 2022-05-03 20:36:17
updated: 2022-09-19 01:14:22
tags: 
- article
- featured
---

# CAS实现原子操作的三大问题

## ABA问题

所谓ABA问题，就是一个值原来是A，变成了B，又变回了A。这个时候使用[[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/Java/2-并发编程/CAS|CAS]]是检查不出变化的，但实际上却被更新了两次。

ABA问题的解决思路是在变量前面追加上**版本号或者时间戳**。从JDK 1.5开始，JDK的atomic包里提供了一个类`AtomicStampedReference`类来解决ABA问题。

这个类的`compareAndSet`方法的作用是首先检查当前引用是否等于预期引用，并且检查当前标志是否等于预期标志，如果二者都相等，才使用CAS设置为新的值和标志。

```java
public boolean compareAndSet(V   expectedReference,
                             V   newReference,
                             int expectedStamp,
                             int newStamp) {
    Pair<V> current = pair;
    return
        expectedReference == current.reference &&
        expectedStamp == current.stamp &&
        ((newReference == current.reference &&
          newStamp == current.stamp) ||
         casPair(current, Pair.of(newReference, newStamp)));
}
```

## 循环时间长开销大

CAS多与自旋结合。如果[[2_0_2-计算机科学/2_0_2_1_2_3-软件系统/2_0_2_1_2_3_1-操作系统/自旋|自旋]]CAS长时间不成功，会占用大量的CPU资源。

解决思路是让JVM支持处理器提供的**pause指令**。

pause指令能让自旋失败时cpu睡眠一小段时间再继续自旋，从而使得读操作的频率低很多,为解决内存顺序冲突而导致的CPU流水线重排的代价也会小很多。

## 只能保证一个共享变量的原子操作

有两种解决方案：

1. 使用JDK 1.5开始就提供的`AtomicReference`类保证对象之间的[[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/Java/2-并发编程/原子性|原子性]]，把多个变量放到一个对象里面进行CAS操作；
2. 使用[[2_0_2-计算机科学/2_0_2_1_2_3-软件系统/2_0_2_1_2_3_1-操作系统/linux/锁|锁]]。锁内的[[2_0_2-计算机科学/2_0_2_1_2_3-软件系统/2_0_2_1_2_3_1-操作系统/临界区|临界区]]代码可以保证只有当前[[2_0_2-计算机科学/2_0_2_1_2_3-软件系统/2_0_2_1_2_3_1-操作系统/线程|线程]]能操作。
