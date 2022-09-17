---
title: epoll
created: 2022-06-19 17:01:50
updated: 2022-06-19 19:24:54
tags: 
- #atom
---
# epoll

## 特性

### 触发模式

#### 水平触发

水平触发为Level Triggered，简称LT。  
水平触发关心的是缓冲区的状态，当缓冲区可读的时候，就会发出通知，也就是当缓冲区中只要有数据就会发出通知。

#### 边缘触发

边缘触发为Edge Triggered，简称ET。  
边缘触发关心的是缓冲区状态的变化，当缓冲区状态发生变化的时候才会发出通知，比如缓冲区中来了新的数据。

#### 区别

设想这样一个场景，当一次read()读取没有读取完缓冲区中的数据时，LT和ET的区别：  
1、LT，此时缓冲区中还有数据，会继续发通知

2、ET，此时缓冲区状态并没有发生变化，并没有来新的数据，就不会发通知，在新数据到来之前，之前剩余的数据就无法取出。

所以在ET模式下，当读取数据的时候，一定要循环读取数据，直到缓冲区中的数据**全部读取**完成，一次性将数据取出。


## 原理流程

> 类似java [[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/Java/2-并发编程/ReentrantLock|ReentrantLock]] 的实现，或者像[[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/Java/2-并发编程/monitor|Monitor]]管程的设计。线程访问资源就到等待室中等待；准备好了的资源会放入红黑树便于检索；有资源好了操作系统就会唤醒等待室中的线程。

### 1、创建epoll对象

如下图所示，当某个进程调用epoll_create方法时，内核会创建一个eventpoll对象（也就是程序中epfd所代表的对象）。eventpoll对象也是文件系统中的一员，和socket一样，它也会有等待队列。

内核创建eventpoll对象：
![[z-oblib/z2-attachments/v2-e3467895734a9d97f0af3c7bf875aaeb_720w.jpg]]

创建一个代表该epoll的eventpoll对象是必须的，因为内核要维护“就绪列表”等数据，“就绪列表”可以作为eventpoll的成员。

### 2、维护监视列表

创建epoll对象后，可以用epoll_ctl添加或删除所要监听的socket。以添加socket为例，如下图，如果通过epoll_ctl添加sock1、sock2和sock3的监视，内核会将eventpoll添加到这三个socket的等待队列中。

添加所要监听的socket：

![[z-oblib/z2-attachments/v2-b49bb08a6a1b7159073b71c4d6591185_720w 1.jpg]]

当socket收到数据后，中断程序会操作eventpoll对象，而不是直接操作进程。

### 3、接收数据

当socket收到数据后，中断程序会给eventpoll的“就绪列表”添加socket引用。如下图展示的是sock2和sock3收到数据后，中断程序让rdlist引用这两个socket。

给就绪列表添加引用：
![[z-oblib/z2-attachments/v2-18b89b221d5db3b5456ab6a0f6dc5784_720w.jpg]]

eventpoll对象相当于是socket和进程之间的中介，socket的数据接收并**不直接影响进程**，而是通过改变eventpoll的就绪列表来改变进程状态。

当程序执行到epoll_wait时，如果rdlist已经引用了socket，那么epoll_wait直接返回，如果rdlist为空，**阻塞**进程。

### 4、阻塞和唤醒进程

假设计算机中正在运行进程A和进程B，在某时刻进程A运行到了epoll_wait语句。如下图所示，内核会将进程A放入eventpoll的**等待队列**中，阻塞进程。

epoll_wait阻塞进程：
![[z-oblib/z2-attachments/v2-90632d0dc3ded7f91379b848ab53974c_720w.jpg]]

当socket接收到数据，中断程序一方面修改rdlist，另一方面唤醒eventpoll等待队列中的进程，进程A再次进入运行状态（如下图）。也因为rdlist的存在，进程A可以**知道哪些socket发生了变化**。

epoll唤醒进程：
![[z-oblib/z2-attachments/v2-40bd5825e27cf49b7fd9a59dfcbe4d6f_720w.jpg]]

## 实现细节

eventpoll的数据结构是什么样子？
就绪队列应该应使用什么数据结构？
eventpoll应使用什么数据结构来管理通过epoll_ctl添加或删除的socket？

如下图所示，eventpoll包含了lock、mtx、wq（等待队列）、rdlist等成员。rdlist和rbr是我们所关心的。

epoll原理示意图：
![[z-oblib/z2-attachments/v2-e63254878f67751dcc07a25b93f974bb_720w.jpg]]
图片来源：《深入理解Nginx：模块开发与架构解析(第二版)》，陶辉

### 就绪列表的数据结构

> 就绪队列 --> 双向链表

就绪列表引用着就绪的socket，所以它应能够快速的**插入**数据。

程序可能随时调用epoll_ctl添加监视socket，也可能随时删除。当删除时，若该socket已经存放在就绪列表中，它也应该被移除。

所以就绪列表应是一种能够快速插入和删除的数据结构。双向链表就是这样一种数据结构，epoll使用**双向链表**来实现就绪队列（对应上图的rdllist）。

### 索引结构

> 索引结构 --> 红黑树

既然epoll将“维护监视队列”和“进程阻塞”分离，也意味着需要有个数据结构来保存监视的socket。至少要方便的添加和移除，还要**便于搜索**，以避免重复添加。红黑树是一种自平衡二叉查找树，搜索、插入和删除时间复杂度都是O(log(N))，效率较好。epoll使用了红黑树作为索引结构（对应上图的rbr）。

> ps：因为操作系统要兼顾多种功能，以及由更多需要保存的数据，rdlist并非直接引用socket，而是通过epitem间接引用，红黑树的节点也是epitem对象。同样，文件系统也并非直接引用着socket。为方便理解，本文中省略了一些间接结构。

## 结论

epoll在select和poll（poll和select基本一样，有少量改进）的基础引入了eventpoll作为中间层，使用了先进的数据结构，是一种高效的多路复用技术。

