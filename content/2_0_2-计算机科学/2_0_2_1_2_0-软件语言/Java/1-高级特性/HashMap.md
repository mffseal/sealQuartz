---
title: HashMap
created: 2022-06-13 15:31:55
updated: 2022-07-20 16:52:28
tags: 
- atom
---

# HashMap

## 并发问题

### JDK7并发死链

```java
public static void main(String[] args) {
    // 测试 java 7 中哪些数字的 hash 结果相等
    System.out.println("长度为16时，桶下标为1的key");
    for (int i = 0; i < 64; i++) {
        if (hash(i) % 16 == 1) {
            System.out.println(i);
        }
    }
    System.out.println("长度为32时，桶下标为1的key");
    for (int i = 0; i < 64; i++) {
        if (hash(i) % 32 == 1) {
            System.out.println(i);
        }
    }
    // 1, 35, 16, 50 当大小为16时，它们在一个桶内
    final HashMap<Integer, Integer> map = new HashMap<Integer, Integer>();
    // 放 12 个元素
    map.put(2, null);
    map.put(3, null);
    map.put(4, null);
    map.put(5, null);
    map.put(6, null);
    map.put(7, null);
    map.put(8, null);
    map.put(9, null);
    map.put(10, null);
    // 下面三个会放在一个桶中
    map.put(16, null);
    map.put(35, null);
    map.put(1, null);
 
    System.out.println("扩容前大小[main]:"+map.size());
    new Thread() {
        @Override
        public void run() {
            // 放第 13 个元素, 发生扩容
            map.put(50, null);
            System.out.println("扩容后大小[Thread-0]:"+map.size());
        }
    }.start();
    new Thread() {
        @Override
        public void run() {
            // 放第 13 个元素, 发生扩容
            map.put(50, null);
            System.out.println("扩容后大小[Thread-1]:"+map.size());
        }
    }.start();
}
 
final static int hash(Object k) {
    int h = 0;
    if (0 != h && k instanceof String) {
        return sun.misc.Hashing.stringHash32((String) k);
    }
    h ^= k.hashCode();
    h ^= (h >>> 20) ^ (h >>> 12);
    return h ^ (h >>> 7) ^ (h >>> 4);
}
```

#### 死链复现

调试工具使用 idea
在 HashMap 源码 590 行加断点
```java
int newCapacity = newTable.length;
```
断点的条件如下，目的是让 HashMap 在扩容为 32 时，并且线程为 Thread-0 或 Thread-1 时停下来：
```java
newTable.length==32 && 
    (
        Thread.currentThread().getName().equals("Thread-0")||
        Thread.currentThread().getName().equals("Thread-1")
    )
```
断点暂停方式选择 Thread，否则在调试 Thread-0 时，Thread-1 无法恢复运行
运行代码，程序在预料的断点位置停了下来，输出：
```
长度为16时，桶下标为1的key 
1 
16 
35 
50 
长度为32时，桶下标为1的key 
1 
35 
扩容前大小[main]:12 
```
接下来进入扩容流程调试
在 HashMap 源码 594 行加断点
```java
Entry<K,V> next = e.next; // 593
if (rehash)              // 594
// ...
```
这是为了观察 e 节点和 next 节点的状态，Thread-0 单步执行到 594 行，再 594 处再添加一个断点（条件Thread.currentThread().getName().equals("Thread-0")）
这时可以在 Variables 面板观察到 e 和 next 变量，使用 view as -> Object 查看节点状态
```
e (1)->(35)->(16)->null 
next (35)->(16)->null 
```
在 Threads 面板选中 Thread-1 恢复运行，可以看到控制台输出新的内容如下，Thread-1 扩容已完成
```
newTable[1]  (35)->(1)->null
扩容后大小:13
```
这时 Thread-0 还停在 594 处， Variables 面板变量的状态已经变化为
```
e (1)->null 
next (35)->(1)->null 
```
为什么呢，因为 Thread-1 扩容时链表也是后加入的元素放入链表头，因此链表就倒过来了，但 Thread-1 虽然结果正确，但它结束后 Thread-0 还要继续运行
接下来就可以单步调试（F8）观察死链的产生了
下一轮循环到 594，将 e 搬迁到 newTable 链表头
```
newTable[1]     (1)->null 
e (35)->(1)->null 
next (1)->null 
```
下一轮循环到 594，将 e 搬迁到 newTable 链表头
```
newTable[1] (35)->(1)->null 
e (1)->null 
next null 
```
再看看源码
```java
e.next = newTable[1];
// 这时 e  (1,35)
// 而 newTable[1] (35,1)->(1,35) 因为是同一个对象
 
newTable[1] = e;  
// 再尝试将 e 作为链表头, 死链已成
 
e = next;
// 虽然 next 是 null, 会进入下一个链表的复制, 但死链已经形成了
```

#### 源码分析

```java
// 将 table 迁移至 newTable
void transfer(Entry[] newTable, boolean rehash) {    
    int newCapacity = newTable.length;
    for (Entry<K,V> e : table) {
        while(null != e) {
            Entry<K,V> next = e.next;
            // 1 处
            if (rehash) {
                e.hash = null == e.key ? 0 : hash(e.key);
            }
            int i = indexFor(e.hash, newCapacity);
            // 2 处
            // 将新元素加入 newTable[i], 原 newTable[i] 作为新元素的 next
            e.next = newTable[i];
            newTable[i] = e;
            e = next;
        }
    }
}
```

```
原始链表，格式：[下标] (key,next)
[1] (1,35)->(35,16)->(16,null)
 
线程 a 执行到 1 处 ，此时局部变量 e 为 (1,35)，而局部变量 next 为 (35,16) 线程 a 挂起
 
线程 b 开始执行（构建扩容后的新链表）
第一次循环
[1] (1,null)
 
第二次循环
[1] (35,1)->(1,null)
 
第三次循环
[1] (35,1)->(1,null)
[17] (16,null)
 
切换回线程 a，此时局部变量 e 和 next 被恢复，引用没变但内容变了：e 的内容被改为 (1,null)，而 next 的内
容被改为 (35,1) 并链向 (1,null)
第一次循环
[1] (1,null)
 
第二次循环，注意这时 e 是  (35,1) 并链向 (1,null) 所以 next 又是 (1,null)
[1] (35,1)->(1,null)
 
第三次循环，e 是 (1,null)，而 next 是 null，但 e 被放入链表头，这样 e.next 变成了 35 （2 处）
[1] (1,35)->(35,1)->(1,35)
链表出现循环
已经是死链了
```

### 总结

1. JDK7的HashMap桶链表采用头插法，新节点会成为链表的头节点。
2. 在扩容过程中，遍历旧链表构造新链表的时候采用头插法，会导致链表倒序排列，顺序与原链表不一致。（头插法有逆序操作，会修改节点的next指针，两个线程同时扩容就会读取到异常的next值造成环的出现）。
3. 两个线程同时触发扩容且一个线程先完成扩容遍历，第二个线程只获取到了头节点和头节点.next两个节点。
4. 第二个线程继续执行时，手上的两个节点已经被第一个线程改掉，先后关系反了，但第二个线程不知道还以为是原来的顺序。
5. 第二个线程继续按原顺序对链表扩容，遍历构造新链表时出现了环。

- 究其原因，是因为在多线程环境下使用了非线程安全的 map 集合
- JDK 8 虽然将扩容算法做了调整，不再将元素加入链表头（而是保持与扩容前一样的顺序），但仍不意味着能够在多线程环境下能够安全扩容，还会出现其它问题（如扩容丢数据）。