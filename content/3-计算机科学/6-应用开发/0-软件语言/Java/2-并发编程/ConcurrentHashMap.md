---
title: ConcurrentHashMap
created: 2022-06-12 22:09:17
updated: 2022-06-13 20:31:20
tags: 
- atom
---
# ConcurrentHashMap

## 用例

分布式计算字符串数量：

### 生成测试数据

```java
static final String ALPHA = "abcedfghijklmnopqrstuvwxyz";
 
public static void main(String[] args) {
    int length = ALPHA.length();
    int count = 200;
    List<String> list = new ArrayList<>(length * count);
    for (int i = 0; i < length; i++) {
        char ch = ALPHA.charAt(i);
        for (int j = 0; j < count; j++) {
            list.add(String.valueOf(ch));
        }
    }
    Collections.shuffle(list);
    for (int i = 0; i < 26; i++) {
        try (PrintWriter out = new PrintWriter(
            new OutputStreamWriter(
                new FileOutputStream("tmp/" + (i+1) + ".txt")))) {
            String collect = list.subList(i * count, (i + 1) * count).stream()
                .collect(Collectors.joining("\n"));
            out.print(collect);
        } catch (IOException e) {
        }
    }
}
```

### 模板代码

模版代码中封装了多线程读取文件的代码：

```java
private static <V> void demo(Supplier<Map<String,V>> supplier, 
BiConsumer<Map<String,V>,List<String>> consumer) {
    Map<String, V> counterMap = supplier.get();
    List<Thread> ts = new ArrayList<>();
    for (int i = 1; i <= 26; i++) {
        int idx = i;
        Thread thread = new Thread(() -> {
            List<String> words = readFromFile(idx);
            consumer.accept(counterMap, words);
        });
        ts.add(thread);
    }
 
    ts.forEach(t->t.start());
    ts.forEach(t-> {
        try {
            t.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
            }
    });
 
    System.out.println(counterMap);
}
 
public static List<String> readFromFile(int i) {
    ArrayList<String> words = new ArrayList<>();
    try (BufferedReader in = new BufferedReader(new InputStreamReader(new FileInputStream("tmp/" 
+ i +".txt")))) {
        while(true) {
            String word = in.readLine();
            if(word == null) {
                break;
            }
            words.add(word);
        }
        return words;
    } catch (IOException e) {
        throw new RuntimeException(e);
    }
}
```

### 实现

1. 提供一个 map 集合，用来存放每个单词的计数结果，key 为单词，value 为计数
2. 提供一组操作，保证计数的安全性，会传递 map 集合以及 单词 List

#### LongAdder实现

借助LongAdder实现原子的自增。

```java
demo(
    () -> new ConcurrentHashMap<String, LongAdder>(),
    (map, words) -> {
        for (String word : words) {
            // 注意不能使用 putIfAbsent，此方法返回的是上一次的 value，首次调用返回 null
            map.computeIfAbsent(word, (key) -> new LongAdder()).increment();
        }
    }
);
```

#### 函数式编程

```java
demo(
    () -> new ConcurrentHashMap<String, Integer>(),
    (map, words) -> {
        for (String word : words) {
            // 函数式编程，无需原子变量
            map.merge(word, 1, Integer::sum);
        }
    }
);
```

## 源码分析
> JDK8源码。
> 解决HashMap的[[3-计算机科学/6-应用开发/0-软件语言/Java/1-高级特性/HashMap#JDK7并发死链|并发问题]]。

### 重要属性和内部类

```java
// 默认为 0
// 当初始化时, 为 -1
// 当扩容时, 为 -(1 + 扩容线程数)
// 当初始化或扩容完成后，为 下一次的扩容的阈值大小
private transient volatile int sizeCtl;
 
// 整个 ConcurrentHashMap 就是一个 Node[]
static class Node<K,V> implements Map.Entry<K,V> {}
 
// hash 表
transient volatile Node<K,V>[] table;
 
// 扩容时的 新 hash 表
private transient volatile Node<K,V>[] nextTable;
 
// 扩容时如果某个 bin 迁移完毕, 用 ForwardingNode 作为旧 table bin 的头结点
static final class ForwardingNode<K,V> extends Node<K,V> {}
 
// 用在 compute 以及 computeIfAbsent 时, 用来占位, 计算完成后替换为普通 Node
static final class ReservationNode<K,V> extends Node<K,V> {}
 
// 作为 treebin 的头节点, 存储 root 和 first
static final class TreeBin<K,V> extends Node<K,V> {}
 
// 作为 treebin 的节点, 存储 parent, left, right
static final class TreeNode<K,V> extends Node<K,V> {}
```

### 重要方法

```java
// 获取 Node[] 中第 i 个 Node
static final <K,V> Node<K,V> tabAt(Node<K,V>[] tab, int i)
    
// cas 修改 Node[] 中第 i 个 Node 的值, c 为旧值, v 为新值
static final <K,V> boolean casTabAt(Node<K,V>[] tab, int i, Node<K,V> c, Node<K,V> v)
    
// 直接修改 Node[] 中第 i 个 Node 的值, v 为新值
static final <K,V> void setTabAt(Node<K,V>[] tab, int i, Node<K,V> v)
```

### 构造方法

```java
public ConcurrentHashMap(int initialCapacity, float loadFactor, int concurrencyLevel) {
    if (!(loadFactor > 0.0f) || initialCapacity < 0 || concurrencyLevel <= 0)
        throw new IllegalArgumentException();
    if (initialCapacity < concurrencyLevel)   // Use at least as many bins
        initialCapacity = concurrencyLevel;   // as estimated threads
    long size = (long)(1.0 + (long)initialCapacity / loadFactor);
    // tableSizeFor 仍然是保证计算的大小是 2^n, 即 16,32,64 ... 
    int cap = (size >= (long)MAXIMUM_CAPACITY) ?
	    // tableSizeFor()会将实际大小设置为2^n
        MAXIMUM_CAPACITY : tableSizeFor((int)size);
    this.sizeCtl = cap;
}
```

### get方法

全程未加锁，性能比较高
> HashTable的get全程有synchronized锁。

桶下标计算：(n - 1) & h)，其中n是数组长度，h是hash值，相当于是取模运算，[[3-计算机科学/0-数据结构与算法/快速取模|快速取模]]。

```java
public V get(Object key) {
    Node<K,V>[] tab; Node<K,V> e, p; int n, eh; K ek;
    // spread 方法能确保返回结果是正数
    // 负数在接下来的流程中有额外用途
    int h = spread(key.hashCode());
    // 如果table不为空并且含有元素
    if ((tab = table) != null && (n = tab.length) > 0 &&
	    // 根据桶下标找链表
        (e = tabAt(tab, (n - 1) & h)) != null) {
        // 如果头结点已经是要查找的 key
        if ((eh = e.hash) == h) {
            if ((ek = e.key) == key || (ek != null && key.equals(ek)))
                return e.val;
        }
        // hash 为负数表示该 bin 在扩容中或是 treebin, 这时调用 find 方法来查找
        else if (eh < 0)
            return (p = e.find(h, key)) != null ? p.val : null;
        // 正常遍历链表, 用 equals 比较
        while ((e = e.next) != null) {
            if (e.hash == h &&
                ((ek = e.key) == key || (ek != null && key.equals(ek))))
                return e.val;
        }
    }
    return null;
}
```

### put方法

和普通HashMap不同，这里不允许空的kay和value。
树化阈值是8。

```java
public V put(K key, V value) {
	// 第三个参数表示重复的key输入，是否用新值覆盖旧值，默认false覆盖
    return putVal(key, value, false);
}
 
final V putVal(K key, V value, boolean onlyIfAbsent) {
	普通hashMap允许有空key和value，这里不允许
    if (key == null || value == null) throw new NullPointerException();
    // 其中 spread 方法会综合高位低位, 具有更好的 hash 性
    int hash = spread(key.hashCode());
    int binCount = 0;
    for (Node<K,V>[] tab = table;;) {
        // f 是链表头节点
        // fh 是链表头结点的 hash
        // i 是链表在 table 中的下标
        Node<K,V> f; int n, i, fh;
        // hash表为空或长度为0：要创建 table （和懒加载有关）
        if (tab == null || (n = tab.length) == 0)
            // 初始化 table 使用了 cas, 无需 synchronized 创建成功, 进入下一轮循环
            tab = initTable();
        // 要创建链表头节点
        else if ((f = tabAt(tab, i = (n - 1) & hash)) == null) {
            // 添加链表头使用了 cas, 无需 synchronized
            if (casTabAt(tab, i, null,
                         new Node<K,V>(hash, key, value, null)))
                break;
        }
        // 帮忙扩容
        // 判断头节点是否是forwardingNode
        else if ((fh = f.hash) == MOVED)
	        // 锁住某个待扩容的桶中链表，帮忙扩容
            // 帮忙之后, 进入下一轮循环
            tab = helpTransfer(tab, f);
        // hashTable 即未正在扩容，又已初始化完毕，并产生了冲突
        else {
            V oldVal = null;
            // 锁住链表头节点
            // 桶下标冲突时才会加锁
            // 只对该桶链表头节点加锁
            synchronized (f) {
                // 再次确认链表头节点没有被移动
                if (tabAt(tab, i) == f) {
                    // 链表
                    if (fh >= 0) {
                        binCount = 1;  // 链表长度
                        // key没有要追加，key有了要更新
                        // 遍历链表
                        for (Node<K,V> e = f;; ++binCount) {
                            K ek;
                            // 找到相同的 key
                            // hash码相等、同一对象、key值相等
                            if (e.hash == hash &&
                                ((ek = e.key) == key ||
                                 (ek != null && key.equals(ek)))) {
                                oldVal = e.val;
                                // 更新value
                                if (!onlyIfAbsent)
                                    e.val = value;
                                break;
                            }
                            Node<K,V> pred = e;
                            // 已经是最后的节点了, 新增 Node, 追加至链表尾 

                            if ((e = e.next) == null) {
                            pred.next = new Node<K,V>(hash, key,
                                                          value, null);
                                break;
                            }
                        }
                    }
                    // 红黑树
                    else if (f instanceof TreeBin) {
                        Node<K,V> p;
                        binCount = 2;
                        // putTreeVal 会看 key 是否已经在树中, 是, 则返回对应的 TreeNode
                        if ((p = ((TreeBin<K,V>)f).putTreeVal(hash, key,
                                                              value)) != null) {
                            oldVal = p.val;
                            if (!onlyIfAbsent)
                                p.val = value;
                        }
                    }
                }
            // 释放链表头节点的锁
            }
	        //根据链表长度决定优化策略 转红黑树/扩容
            if (binCount != 0) {                
                if (binCount >= TREEIFY_THRESHOLD)
                    // 如果链表长度 >= 树化阈值(8), 进行链表转为红黑树
                    treeifyBin(tab, i);
                if (oldVal != null)
                    return oldVal;
                break;
            }
        }
    }
    // 增加 size 计数
    // 使用了类似LongAdder的方式
    // 该方法包含了扩容的逻辑
    addCount(1L, binCount);
    return null;
}

// 保证只有一个线程能成功创建hash表
private final Node<K,V>[] initTable() {
    Node<K,V>[] tab; int sc;
    // 若hash表还未被创建
    while ((tab = table) == null || tab.length == 0) {
	    // 有其它线程正在创建hash表了
        if ((sc = sizeCtl) < 0)
            Thread.yield();  // 让出cpu使用权（弱让出）
        // 尝试将 sizeCtl 设置为 -1（-1表示初始化 table）
        else if (U.compareAndSwapInt(this, SIZECTL, sc, -1)) {
            // 获得锁, 创建 table, 这时其它线程会在 while() 循环中 yield 直至 table 创建 
            try {
                if ((tab = table) == null || tab.length == 0) {
	                // 使用预设容量sc进行hash表创建
	                // 默认容量16
                    int n = (sc > 0) ? sc : DEFAULT_CAPACITY;
                    Node<K,V>[] nt = (Node<K,V>[])new Node<?,?>[n];
                    table = tab = nt;
                    // sc转成下次要扩容时的阈值
                    sc = n - (n >>> 2);
                }

            } finally {
            sizeCtl = sc;
            }
            break;
        }
    }
    return tab;
}
 
// check 是之前 binCount 的个数
private final void addCount(long x, int check) {
    CounterCell[] as; long b, s;
    if (
        // 已经有了 counterCells, 向 cell 累加
        (as = counterCells) != null ||
        // 还没有, 向 baseCount 累加
        !U.compareAndSwapLong(this, BASECOUNT, b = baseCount, s = b + x)
    ) {
        CounterCell a; long v; int m;
        boolean uncontended = true;
        if (
            // 还没有 counterCells
            as == null || (m = as.length - 1) < 0 ||
            // 还没有 cell
            (a = as[ThreadLocalRandom.getProbe() & m]) == null ||
            // cell cas 增加计数失败
            !(uncontended = U.compareAndSwapLong(a, CELLVALUE, v = a.value, v + x))
           ) {
            // 创建累加单元数组和cell, 累加重试
            fullAddCount(x, uncontended);
            return;
        }
        if (check <= 1)
            return;
        // 获取元素个数
        s = sumCount();
    }
    if (check >= 0) {
        Node<K,V>[] tab, nt; int n, sc;
        while (s >= (long)(sc = sizeCtl) && (tab = table) != null &&
               (n = tab.length) < MAXIMUM_CAPACITY) {
            int rs = resizeStamp(n);
            if (sc < 0) {
                if ((sc >>> RESIZE_STAMP_SHIFT) != rs || sc == rs + 1 ||
                    sc == rs + MAX_RESIZERS || (nt = nextTable) == null ||
                    transferIndex <= 0)
                    break;
                // newtable 已经创建了，帮忙扩容
                if (U.compareAndSwapInt(this, SIZECTL, sc, sc + 1))
                    transfer(tab, nt);
            }
            // 需要扩容，这时 newtable 未创建
            else if (U.compareAndSwapInt(this, SIZECTL, sc,

                                         (rs << RESIZE_STAMP_SHIFT) + 2))
                                         transfer(tab, null);
            s = sumCount();
        }
    }
}
```

### size方法

size 计算实际发生在 put，remove 改变集合元素的操作之中
- 没有竞争发生，向 baseCount 累加计数
- 有竞争发生，新建 counterCells，向其中的一个 cell 累加计数
	- counterCells 初始有两个 cell
	- 如果计数竞争比较激烈，会创建新的 cell 来累加计数

```java
public int size() {
    long n = sumCount();
    return ((n < 0L) ? 0 :
            (n > (long)Integer.MAX_VALUE) ? Integer.MAX_VALUE :
            (int)n);
}
 
final long sumCount() {
    CounterCell[] as = counterCells; CounterCell a;
    // 将 baseCount 计数与所有 cell 计数累加
    long sum = baseCount;
    if (as != null) {
        for (int i = 0; i < as.length; ++i) {
            if ((a = as[i]) != null)
                sum += a.value;
        }
    }
    return sum;
}
```

## 总结

Java 8 数组（Node） +（ 链表 Node | 红黑树 TreeNode ） 以下数组简称（table），链表简称（bin）

- 初始化，使用 [[3-计算机科学/6-应用开发/0-软件语言/Java/2-并发编程/CAS|cas]] 来保证并发安全，**懒惰**初始化 table
- 树化，当 table.length < **64** 时，先尝试**扩容**，超过 64 时，并且 bin.length > **8** 时，会将链表树化，树化过程会用 [[3-计算机科学/6-应用开发/0-软件语言/Java/2-并发编程/synchronized|synchronized]] 锁住链表头
- put，如果该 bin 尚未创建，只需要使用 cas 创建 bin；如果已经有了，锁住链表头进行后续 put 操作，元素添加至 bin 的**尾部**
- get，**无锁**操作仅需要保证[[3-计算机科学/6-应用开发/0-软件语言/Java/2-并发编程/可见性|可见性]]，扩容过程中 get 操作在旧table拿到的是 ForwardingNode 则说明正在扩容并且当前桶已被搬迁，它会让 get 操作在新 table 进行搜索
- 扩容，扩容时以 bin 为单位进行，需要对 bin 进行 [[3-计算机科学/6-应用开发/0-软件语言/Java/2-并发编程/synchronized|synchronized]]，但这时妙的是其它竞争[[3-计算机科学/2-计算机组成原理/线程|线程]]也不是无事可做，它们会帮助把其它 bin 进行扩容，扩容时平均只有 **1/6** 的节点会被复制到新 table 中
- size，元素个数保存在 baseCount 中，[[3-计算机科学/2-计算机组成原理/并发|并发]]时的个数变动保存在 CounterCell[] 当中（类似[[3-计算机科学/6-应用开发/0-软件语言/Java/2-并发编程/LongAdder|LongAdder]]）。最后统计数量时累加即可