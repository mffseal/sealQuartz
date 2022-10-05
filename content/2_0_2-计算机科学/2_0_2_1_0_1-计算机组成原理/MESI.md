---
title: MESI
created: 2022-05-30 20:25:31
updated: 2022-05-30 20:30:26
tags: 
- atom
---
# MESI

**M：代表已修改（Modified）**：Cache Block 里面的内容我们已经更新过了，但是还没有写回到主内存里面；  
**E：代表独占（Exclusive）**：Cache Block 里面的数据和主内存里面的数据是一致的；  
**S：代表共享（Shared）**：Cache Block 里面的数据和主内存里面的数据是一致的；  
**I：代表已失效（Invalidated）**：Cache Block 里面的数据已经失效了，不可以相信这个 Cache Block 里面的数据；

![[z-oblib/z2-attachments/24483793-3cef70653d60cdf9.webp]]

## 问题
CPU操作分为两种：load（读）、store（写），加入缓存的目的是提前缓存内存的数据，提高load的效率，但是store的速度降低了，因为CPU将数据store到内存多了写缓存的步骤，并且需要同步所有CPU的私有缓存。这样store操作会严重阻塞后续的load操作，这样加缓存的意义完全就没有了，不仅没能提高load的效率，反而阻塞了load。为了解决load被阻塞的问题，在CPU中加入了新的组件store buffer（写队列）；

![[z-oblib/z2-attachments/24483793-80300b10191392a0.webp]]
每个CPU都有一个store buffer，当CPU需要执行store操作时，会将store操作先放入store buffer中，不会立即执行store操作，等待`合适的时机`再执行（store buffer满了等等情况会真正执行store操作），在store后面的load操作不用再等store真正执行完毕才能执行，只要store放入了store buffer中，load就可以执行了。

## 总结

MESI协议的引入会导致缓存的写入效率降低，所以引入了store buffer等部件，store buffer将store操作缓存起来，不会立即写入缓存，**导致多CPU内的值同步会有一定延迟**，间接导致cpu的操作[[2_0_2-计算机科学/2_0_2_1_2_3-软件系统/2_0_2_1_2_3_1-操作系统/指令重排序|重排序]]，多cpu的共享变量的操作会发生混乱，所以JMM中可以使用[[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/Java/1-高级特性/volatile|volatile]]强制刷新store buffer，让多CPU中的值[[2_0_2-计算机科学/2_0_2_1_2_3-软件系统/2_0_2_1_2_3_1-操作系统/同步|同步]]没有延迟，保证多CPU共享变量不会发生混乱。
