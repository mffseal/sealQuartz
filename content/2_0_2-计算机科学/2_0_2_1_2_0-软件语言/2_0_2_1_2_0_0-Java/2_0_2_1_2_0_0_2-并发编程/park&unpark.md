---
title: park&unpark
created: 2022-05-29 17:20:40
updated: 2022-05-29 20:59:21
tags: 
- atom
---
# park&unpark

## 特点

### 与 wait&notify相比

- wait，notify 和 notifyAll 必须配合 Object Monitor 一起使用，而 park，unpark 不必
- park & unpark 是以线程为单位来阻塞/唤醒线程，而 notify 只能随机唤醒一个等待线程，notifyAll 是唤醒所有等待线程，就不那么精准。
- park & unpark 可以先 unpark，而 wait & notify 不能先 notify。

## 原理

**每个线程都有自己的一个 Parker 对象**，由三部分组成 _counter ， _cond 和 _mutex 打个比喻：
- 线程就像一个旅人，Parker 就像他随身携带的背包：
	- 条件变量就好比背包中的帐篷
	- `_counter` 就好比背包中的备用干粮（0 为耗尽，1 为充足）
- 调用 park 就是要看需不需要停下来歇息
	- 如果备用干粮耗尽，那么钻进帐篷歇息
	- 如果备用干粮充足，那么不需停留，继续前进
- 调用 unpark，就好比令干粮充足
	- 如果这时线程还在帐篷，就唤醒让他继续前进
	- 如果这时线程还在运行，那么下次他调用 park 时，仅是消耗掉备用干粮，不需停留继续前进
		- 因为背包空间有限，多次调用 unpark 仅会补充一份备用干粮

1. 当前线程调用 Unsafe.park() 方法
2. 检查 `_counter` ，本情况为 0，这时，获得 `_mutex` 互斥锁
3. 线程进入 `_cond` 条件变量阻塞
4. 设置 `_counter` = 0
![[z-oblib/z2-attachments/Pasted image 20220529205721.png]]
5. 调用 Unsafe.unpark(Thread_0) 方法，设置 `_counter` 为 1
6. 唤醒 `_cond` 条件变量中的 Thread_0
7. Thread_0 恢复运行
8. 设置 `_counter` 为 0
![[z-oblib/z2-attachments/Pasted image 20220529205853.png]]
9. 调用 Unsafe.unpark(Thread_0) 方法，设置 `_counter` 为 1
10. 唤醒 `_cond` 条件变量中的 Thread_0
11. Thread_0 恢复运行
12. 设置 `_counter` 为 0