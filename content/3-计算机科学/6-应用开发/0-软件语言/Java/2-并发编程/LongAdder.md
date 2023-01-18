---
title: LongAdder
created: 2022-06-02 14:22:48
updated: 2022-06-06 22:43:29
tags: 
- atom
---
# LongAdder

## 原理

LongAdder 类有几个关键域：
```java
// 累加单元数组, 懒惰初始化
transient volatile Cell[] cells;
 
// 基础值, 如果没有竞争, 则用 cas 累加这个域
transient volatile long base;
 
// 在 cells 创建或扩容时, 置为 1, 表示加锁
transient volatile int cellsBusy;
```

cellsBusy用到了[[3-计算机科学/6-应用开发/0-软件语言/Java/2-并发编程/CAS锁|CAS锁]]的方法。

### Cell

Cell为累加单元：

```java
// 防止缓存行伪共享
@sun.misc.Contended 
static final class Cell {
    volatile long value;
    Cell(long x) { value = x; }
    
    // 最重要的方法, 用来 cas 方式进行累加, prev 表示旧值, next 表示新值
    final boolean cas(long prev, long next) {
        return UNSAFE.compareAndSwapLong(this, valueOffset, prev, next);
    }
    // 省略不重要代码
}
```

[[3-计算机科学/6-应用开发/0-软件语言/Java/2-并发编程/伪共享|伪共享]]