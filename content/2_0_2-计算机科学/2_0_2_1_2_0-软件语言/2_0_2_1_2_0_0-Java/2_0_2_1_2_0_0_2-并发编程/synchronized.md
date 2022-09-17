---
title: synchronized
created: 2022-05-03 16:33:52
updated: 2022-05-31 15:43:07
tags: 
- atom
---
# synchronized

## 简介

俗称**对象锁**，采用互斥的方式让同一时刻只有一个[[2_0_2-计算机科学/2_0_2_1_2_3-软件系统/2_0_2_1_2_3_1-操作系统/线程|线程]]能持有对象锁。其它线程再想获取这个对象锁时就会**阻塞**住。这样就能保证拥有锁的线程可以安全的执行[[2_0_2-计算机科学/2_0_2_1_2_3-软件系统/2_0_2_1_2_3_1-操作系统/临界区|临界区]]内的代码，不用担心线程[[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/2_0_2_1_2_0_0-Java/2_0_2_1_2_0_0_2-并发编程/上下文切换|上下文切换]]。

## 特点
- synchronized**不可中断**（不可放弃争抢锁）：
	- 不可中断的意思是等待获取锁的时候不可中断，拿到锁之后可中断，没获取到锁的情况下，中断操作一直不会生效。
- synchronized规定：线程在加锁时， 先清空工作内存→在主内存中拷贝最新变量的副本到工作内存 →执行完代码→将更改后的共享变量的值刷新到主内存中→释放互斥锁。保证了[[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/2_0_2_1_2_0_0-Java/2_0_2_1_2_0_0_2-并发编程/可见性|内存可见性]]。
- synchronized代码块中的代码越多，上锁时间越长，尽量减少锁的粒度。
- synchronized可以保证原子性、可见性，并且对外部展现有序性，即内部的重排序不会影响外部（而不是不会发生重排序）（因为同一时刻进入synchronized代码块的只有一个线程，单线程下重排序无影响）。
	- 要想保证有序性，就要把东西全部交给synchronized管理，而不能暴露一部分在外面，这也是[[2_0_2-计算机科学/2_0_2_1_2_1-软件方法学/设计模式/单例模式#双重校验锁|双重检查锁]]实现时要加[[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/2_0_2_1_2_0_0-Java/2_0_2_1_2_0_0_1-高级特性/volatile|volatile]]。

## 语法

```java
synchronized(对象)
{
	// 临界区
}
```

## 流程

### 比喻

![[z-oblib/z2-attachments/Pasted image 20220526224204.png]]

1. `synchronized(对象)`中的对象，可以想象为一个房间（room），有唯一入口（门）房间只能一次进入一人进行计算，线程 t1，t2 想象成两个人。
2. 当线程 t1 执行到 `synchronized(room)`时就好比 t1 进入了这个房间，并锁住了门拿走了钥匙，在门内执行 `count++` 代码。
3. 这时候如果 t2 也运行到了 `synchronized(room)` 时，它发现门被锁住了，只能在门外等待，发生了上下文切换，阻塞住了。
4. 这中间即使 t1 的 cpu 时间片不幸用完，被踢出了门外（不要错误理解为锁住了对象就能一直执行下去哦），这时门还是锁住的，**t1 仍拿着钥匙**，t2 线程还在阻塞状态进不来，只有下次轮到 t1 自己再次获得时间片时才能开门进入。
5. 当 t1 执行完 `synchronized{}` 块内的代码，这时候才会从 obj 房间出来并解开门上的锁，唤醒 t2 线程把钥匙给他。t2 线程这时才可以进入 obj 房间，锁住了门拿上钥匙，执行它的 `count--` 代码。

![[z-oblib/z2-attachments/Pasted image 20220527095647.png]]

### 总结

synchronized 实际是用对象锁保证了临界区内代码的原子性，临界区内的代码对外是不可分割的，不会被线程切换所打断。

## 使用场景

`synchronized`关键字可以用到4个种场景:
1. Instance methods
2. Static methods
3. Code blocks inside instance methods
4. Code blocks inside static methods

### 成员方法

```java
public synchronized void add(int value){
      this.count += value;
}
```

等价于锁在所属对象上：

```java
class Test{
    public void test() {
        synchronized(this) {
        
        }
    }
}
```

### 静态方法

- 同步静态方法属于类对象。在VM中只有一个类对象，因此不管有几个对象，只能有一个线程执行静态同步方法。

```java
public static synchronized void add(int value){
      count += value;
}
```

等价于锁在类对象上：

```java
class Test{
    public static void test() {
        synchronized(Test.class) {
            
        }
    }
}
```

### 实例方法代码块

- 不需要同步整个方法，只需要同步方法里面的一部分，可以借助同步块来完成工作。
- 括号中的对象是同步代码调用的实例，本例中是`this`。这个对象称为监视对象。
- 在该对象上本方法被声明为同步的。

**代码块必须要传递一个对象作为锁的载体，可以是独立创建的对象或者是代码块所在实例本身（this指针）。**

```java
public void add(int value){
	synchronized(this){
	   this.count += value;   
	}
}
```

下面两个方法的代码，效果是一样的：
- 只能有一个线程执行(针对同一个对象) 
- 第二个方法是不同的线程执行的时候会在同步块里面发生等待(针对同一对象)

```java
public class MyClass {
    public synchronized void log1(String msg1, String msg2){
        log.writeln(msg1);
        log.writeln(msg2);
    }
    
    public void log2(String msg1, String msg2){
        synchronized(this){
            log.writeln(msg1);
            log.writeln(msg2);
        }
    }
}
```

### 静态方法代码块

下面两个静态方法是在类对象上的:
- 一个线程只能在同一时间执行上面的任何一个方法。
- 对于第二个方法：只能有一个线程在代码块里面执行。

```java
  public class MyClass {

    public static synchronized void log1(String msg1, String msg2){
       log.writeln(msg1);
       log.writeln(msg2);
    }

  
    public static void log2(String msg1, String msg2){
       synchronized(MyClass.class){
          log.writeln(msg1);
          log.writeln(msg2);  
       }
    }
  }
```

## 底层实现

> https://github.com/farmerjohngit/myblog/issues/12

### 代码块级

同步代码块的加锁、解锁是通过 Javac 编译器实现的，底层是借助`monitorenter`和`monitorerexit`。

```java
static final Object lock = new Object();
static int counter = 0;
 
public static void main(String[] args) {
    synchronized (lock) {
        counter++;
    }
}
```

```java
public static void main(java.lang.String[]);
    descriptor: ([Ljava/lang/String;)V
    flags: ACC_PUBLIC, ACC_STATIC
	Code:
      stack=2, locals=3, args_size=1
         0: getstatic     #2                  // <- lock引用 （synchronized开始）
         3: dup
         4: astore_1                          // lock引用 -> slot 1
         5: monitorenter                      // 将 lock对象 MarkWord 置为 Monitor 指针
         6: getstatic     #3                  // <- i
         9: iconst_1                          // 准备常数 1
        10: iadd                              // +1
        11: putstatic     #3                  // -> i
        14: aload_1                           // <- lock引用
        15: monitorexit                       // 将 lock对象 MarkWord 重置, 唤醒 EntryList
        16: goto          24
        19: astore_2                          // e -> slot 2 
        20: aload_1                           // <- lock引用
        21: monitorexit                       // 将 lock对象 MarkWord 重置, 唤醒 EntryList
        22: aload_2                           // <- slot 2 (e)
        23: athrow                            // throw e
        24: return
      Exception table:
         from    to  target type
             6    16    19   any
            19    22    19   any
      LineNumberTable:
        line 8: 0
        line 9: 6
        line 10: 14
        line 11: 24
      LocalVariableTable:
        Start  Length  Slot  Name   Signature
            0      25     0  args   [Ljava/lang/String;
      StackMapTable: number_of_entries = 2
        frame_type = 255 /* full_frame */
          offset_delta = 19
          locals = [ class "[Ljava/lang/String;", class java/lang/Object ]
          stack = [ class java/lang/Throwable ]
        frame_type = 250 /* chop */
          offset_delta = 4
```

从字节码中可知同步语句块的实现使用的是`monitorenter`和`monitorexit`指令，其中`monitorenter`指令指向同步代码块的开始位置，`monitorexit`指令则指明同步代码块的结束位置，当执行`monitorenter`指令时，当前线程将试图获取[[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/2_0_2_1_2_0_0-Java/2_0_2_1_2_0_0_1-高级特性/Mark Word|mark word]]里面存储的[[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/2_0_2_1_2_0_0-Java/2_0_2_1_2_0_0_2-并发编程/monitor|monitor]]，当 `monitor`的进入计数器为 0，那线程可以成功取得`monitor`，并将计数器值设置为1，取锁成功。

`monitorenter`指令会将Mark Word置为Monitor指针，再之前会保存对象的hash code等信息。

如果当前线程已经拥有 `monitor` 的持有权，那它可以重入这个 `monitor` ，重入时计数器的值也会加 1。倘若其他线程已经拥有`monitor`的所有权，那当前线程将被阻塞，直到正在执行线程执行完毕，即`monitorexit`指令被执行，执行线程将释放 `monitor`并设置计数器值为0 ，其他线程将有机会持有 `monitor` 。

`monitorexit`指令会从复制的备份中恢复对象的hash code等信息。

值得注意的是编译器将会确保无论方法通过何种方式完成，方法中调用过的每条 `monitorenter` 指令都有执行其对应 `monitorexit` 指令，而无论这个方法是正常结束还是异常结束。为了保证在方法异常完成时 `monitorenter` 和 `monitorexit` 指令依然可以正确配对执行，编译器会自动产生一个异常处理器，这个异常处理器声明可处理所有的异常，它的目的就是用来执行 `monitorexit` 指令。从上面的字节码中也可以看出有两个`monitorexit`指令，它就是异常结束时被执行的释放`monitor` 的指令。

异常处理会根据Exception table：
在6-16行/19-22行发生异常，都会跳转到19行，19行就是释放锁的地方。
```java
Exception table:
 from    to  target type
	 6    16    19   any
	19    22    19   any
```

### 方法级

同步方法的加锁、解锁是通过 Javac 编译器实现的，底层是借助`ACC_SYNCHRONIZED`访问标识符来实现的，代码如下所示：

```java
public class Hello {
    public synchronized void test() {
        System.out.println("test");
    }
}
```

**方法级的同步是隐式**，即无需通过字节码指令来控制的，它实现在方法调用和返回操作之中。JVM可以从方法常量池中的方法表结构(method_info Structure) 中的 `ACC_SYNCHRONIZED` 访问标志区分一个方法是否同步方法。当方法调用时，调用指令将会检查方法的 `ACC_SYNCHRONIZED`访问标志是否被设置，如果设置了，执行线程将先持有`monitor`，然后再执行方法，最后在方法完成(无论是正常完成还是非正常完成)时释放`monitor`。在方法执行期间，执行线程持有了`monitor`，其他任何线程都无法再获得同一个`monitor`。如果一个同步方法执行期间抛出了异常，并且在方法内部无法处理此异常，那这个同步方法所持有的`monitor`将在异常抛到同步方法之外时自动释放。

下面我们看看字节码层面如何实现：

```java
public class Hello {
  public Hello();
    Code:
       0: aload_0
       1: invokespecial #1                  // Method java/lang/Object."<init>":()V
       4: return
  public synchronized void test();
    Code:
       0: getstatic     #2                  // Field java/lang/System.out:Ljava/io/PrintStream;
       3: ldc           #3                  // String test
       5: invokevirtual #4                  // Method java/io/PrintStream.println:(Ljava/lang/String;)V
       8: return
}
```

## synchronized的不足之处

synchronized是用操作系统提供的monitor实现的，所以开销比较大，也不是很灵活：
- 如果临界区是只读操作，其实可以多线程一起执行，但使用synchronized的话，**同一时间只能有一个线程执行**。
- synchronized无法知道线程有没有成功获取到锁。
- 使用synchronized，如果临界区因为IO或者[[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/2_0_2_1_2_0_0-Java/2_0_2_1_2_0_0_2-并发编程/sleep|sleep]]方法等原因阻塞了，而当前线程又没有释放锁，就会导致**所有线程等待**。

> 针对性能问题，java6开始有了[[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/2_0_2_1_2_0_0-Java/2_0_2_1_2_0_0_2-并发编程/轻量级锁|轻量级锁]]和[[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/2_0_2_1_2_0_0-Java/2_0_2_1_2_0_0_2-并发编程/偏向锁|偏向锁]]。
> 针对功能性问题，在locks包下的锁解决了。
