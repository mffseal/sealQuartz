---
title: volatile
created: 2022-04-28 10:37:28
updated: 2022-05-31 15:49:57
tags: 
- atom
---
# volatile

> https://ifeve.com/java-volatile%E5%85%B3%E9%94%AE%E5%AD%97/

## 内存可见性问题

```java
A = 0;
B = 0;
T0 {
	A = 1;
	print(B);
}

T1 {
	B = 1;
	print(A);
}

```
这样一段代码可能会出现下列四种输出：

| 情况1  | 情况2  | 情况3  | 情况4  |
|------|------|------|------|
| 读A   | 读A   | 写A   | 写A   |
| 读B   | 写B   | 写B   | 读B   |
| 写A   | 写A   | 读A   | 读A   |
| 写B   | 读B   | 读B   | 写B   |
| A0B0 | A0B1 | A1B1 | A1B0 |

在读上加入内存屏障即可保证**在一个线程中**写操作发生在读操作之前，但是若线程1先执行完毕线程2才执行，就会导致线程1无法读取到B的值，所以需要让两个线程同步：

1. 用标志位来告知A B变量有没有被写入过
2. 写过后设置标志位
3. 标志位的写前插入屏障     
4. 读之前自旋判断对应标志位


## 作用

保证：
- 内存可见性
	- 读写一定是从主内存中获得，而不是本地内存
- 内存有序性
	- 读写操作按一定的顺序执行，不会因为指令重排而乱序

>无法保证原子性。

## JVM限制重排序的方式

>禁止重排序实际上不是禁止了cpu指令级别的重排序、乱序执行、双射等操作，而是控制内存的访问顺序。编译器指令防止加载/存储操作在源代码中跨行重新排序，但是允许编译器对任意一侧的内存访问或同一侧的其他访问进行重新排序，这可能意味着使用专用指令停止内核的运行，直至确保所有先前的内存访问对系统中的其他代理可见。代理是系统中能够启动总线事务的任何设备——例如处理器或DMA控制器。屏障影响加载-存储（`load-store`）指令顺序的例子：
>![[z-oblib/z2-attachments/Pasted image 20220531012444.png]]

1. volatile变量执行**写**操作，会在写之前插入StoreStore Barriers**写屏障**，在执行volatile变量写之前的所有Store操作都已执行，数据同步到了内存中（将store buffer中的store操作刷新到内存）；在写之后插入StoreLoad Barriers，代表该volatile变量的写操作也会立即刷新到内存中，其他线程会看到最新值；  
2. volatile变量执行**读**操作，会在读之前插入LoadLoad Barriers**读屏障**，代表在执行volatile变量读之前的所有Load从内存中获取最新值；在读之后插入LoadStore Barriers，代表该读取volatile变量获得是内存中最新的值；

### 如何保证可见性

#### 写屏障

写屏障（sfence）保证在该屏障之前的，对共享变量的改动，都同步到主存当中
```java
public void actor2(I_Result r) {
    num = 2;
    ready = true; // ready 是 volatile 赋值带写屏障
    // 写屏障
}
```

#### 读屏障

而读屏障（lfence）保证在该屏障之后，对共享变量的读取，加载的是主存中最新数据
```java
public void actor1(I_Result r) {
    // 读屏障
    // ready 是 volatile 读取值带读屏障
    if(ready) {
        r.r1 = num + num;
    } else {
        r.r1 = 1;
    }
}f
```
![[z-oblib/z2-attachments/Pasted image 20220531142019.png]]


### 如何保证有序性

写屏障会确保指令重排序时，不会将写屏障之前的代码排在写屏障之后
```java
public void actor2(I_Result r) {
    num = 2;
    ready = true; // ready 是 volatile 赋值带写屏障
    // 写屏障
}
```
读屏障会确保指令重排序时，不会将读屏障之后的代码排在读屏障之前
```java
public void actor1(I_Result r) {
    // 读屏障
    // ready 是 volatile 读取值带读屏障
    if(ready) {
        r.r1 = num + num;
    } else {
        r.r1 = 1;
    }
}
```
![[z-oblib/z2-attachments/Pasted image 20220531143810.png]]

## 原理

用[[3-计算机科学/6-应用开发/1-软件方法学/设计模式/单例模式#双重校验锁|单例模式双重校验锁]]的例子展开：

```java
// -------------------------------------> 加入对 INSTANCE 变量的读屏障
0: getstatic     #2                  // Field INSTANCE:Lcn/itcast/n5/Singleton;
3: ifnonnull     37
6: ldc           #3                  // class cn/itcast/n5/Singleton
8: dup
9: astore_0
10: monitorenter -----------------------> 保证原子性、可见性
11: getstatic     #2                  // Field INSTANCE:Lcn/itcast/n5/Singleton;
14: ifnonnull     27
17: new           #3                  // class cn/itcast/n5/Singleton
20: dup
21: invokespecial #4                  // Method "<init>":()V
24: putstatic     #2                  // Field INSTANCE:Lcn/itcast/n5/Singleton;
// -------------------------------------> 加入对 INSTANCE 变量的写屏障
27: aload_0
28: monitorexit ------------------------> 保证原子性、可见性
29: goto          37
32: astore_1
33: aload_0
34: monitorexit
35: aload_1
36: athrow
37: getstatic     #2                  // Field INSTANCE:Lcn/itcast/n5/Singleton;
40: areturn
```

如上面的注释内容所示，读写 volatile 变量时会加入内存屏障（Memory Barrier（Memory Fence）），保证下面两点：
- 可见性
	- 写屏障（sfence）保证在该屏障之前的 t1 对共享变量的改动，都同步到主存当中
	- 而读屏障（lfence）保证在该屏障之后 t2 对共享变量的读取，加载的是主存中最新数据
- 有序性
	- 写屏障会确保指令重排序时，不会将写屏障之前的代码排在写屏障之后
	- 读屏障会确保指令重排序时，不会将读屏障之后的代码排在读屏障之前
- 更底层是读写变量时使用 lock 指令来多核 CPU 之间的可见性与有序性
![[z-oblib/z2-attachments/Pasted image 20220531154956.png]]

## volatile并不总是可行的

**不能解决指令交错**：
- 写屏障仅仅是保证之后的读能够读到最新的结果，但不能保证读跑到它前面去。
- 而有序性的保证也只是保证了本线程内相关代码不被重排序S。
- 
## volatile的用途

从volatile的内存语义上来看，volatile可以保证内存可见性且禁止重排序。

在保证内存可见性这一点上，volatile有着与锁相同的内存语义，所以可以作为一个“轻量级”的锁来使用。但由于volatile仅仅保证对单个volatile变量的读/写具有原子性，而锁可以保证整个**临界区代码**的执行具有原子性。所以**在功能上，锁比volatile更强大；在性能上，volatile更有优势**。

在禁止重排序这一点上，volatile也是非常有用的。比如我们熟悉的[[3-计算机科学/6-应用开发/1-软件方法学/设计模式/单例模式|单例模式]]，其中有一种实现方式是“[[3-计算机科学/6-应用开发/1-软件方法学/设计模式/单例模式#线程安全的实现|双重锁]]检查”，比如这样的代码：

```java
public class Singleton {

    private static Singleton instance; // 不使用volatile关键字

    // 双重锁检验
    public static Singleton getInstance() {
        if (instance == null) { // 第7行
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton(); // 第10行
                }
            }
        }
        return instance;
    }
}
```

如果这里的变量声明不使用volatile关键字，是可能会发生错误的。它可能会被重排序：

```java
instance = new Singleton(); // 第10行

// 可以分解为以下三个步骤
1 memory=allocate();// 分配内存 相当于c的malloc
2 ctorInstanc(memory) //初始化对象
3 s=memory //设置s指向刚分配的地址

// 上述三个步骤可能会被重排序为 1-3-2，也就是：
1 memory=allocate();// 分配内存 相当于c的malloc
3 s=memory //设置s指向刚分配的地址
2 ctorInstanc(memory) //初始化对象
```

而一旦假设发生了这样的重排序，比如线程A在第10行执行了步骤1和步骤3，但是步骤2还没有执行完。这个时候另一个线程B执行到了第7行，它会判定instance不为空，然后直接返回了一个未初始化完成的instance！

所以JSR-133对volatile做了增强后，volatile的禁止重排序功能还是非常有用的。

## 何时使用volatile

正如我前面所说，如果两个线程同时读写一个共享变量，仅仅使用volatile关键字是不够的。你应该使用 [synchronized](http://tutorials.jenkov.com/java-concurrency/synchronized.html) 来保证读写变量是原子的。（一个线程）读写volatile变量时，不会阻塞（其他）线程进行读写。你必须在关键的地方使用synchronized关键字来解决这个问题。

除了synchronized方法，你还可以使用[java.util.concurrent](http://tutorials.jenkov.com/java-util-concurrent/index.html)包提供的许多原子数据类型来解决这个问题。比如，[AtomicLong](http://tutorials.jenkov.com/java-util-concurrent/atomiclong.html)或[AtomicReference](http://tutorials.jenkov.com/java-util-concurrent/atomicreference.html)，或是其他的类。

如果只有一个线程对volatile进行读写，而其他线程只是读取变量，这时，对于只是读取变量的线程来说，volatile就已经可以保证读取到的是变量的最新值。如果没有把变量声明为volatile，这就无法保证。

volatile关键字对32位和64位的变量都有效。

## volatile的性能考量

读写volatile变量会**导致变量从主存读写**。从主存读写比从CPU缓存读写更加“昂贵”。访问一个volatile变量同样会**禁止指令重排**，而指令重排是一种提升性能的技术。因此，你应当只在需要保证变量可见性的情况下，才使用volatile变量。



假设两个全局变量A和B，初始值都是0，线程0对A写入了1，线程1对B写入了1，然后线程0读B，线程1读B，他们分别读到的A和B分别可能是几，列出所有可能的排列组合。

