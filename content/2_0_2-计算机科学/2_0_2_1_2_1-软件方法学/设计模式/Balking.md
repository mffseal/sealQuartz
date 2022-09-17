---
title: Balking
created: 2022-05-30 22:40:25
updated: 2022-05-30 22:57:00
tags: 
- #atom
---
# Balking

Balking （犹豫）模式用在一个线程发现另一个线程或本线程已经做了某一件相同的事，那么本线程就无需再做了，直接结束返回。

## 实现

### 单线程情况

通过变量记录某个方法是否已经执行过，保证方法只能执行一次。
例如监控器前程只需要一个，不需要重复start()新的线程。

```java
class SystemMonitor {
	private boolean starting = false;
	public void start() {
		// 防止重复启动
		if(starting) {
			return;
		}
		starting = true;
		monitorThread = new Thread(()->{...;});
		monitorThread.start();
	}
}
```

### 多线程情况

starting的判断和赋值分成了两步，所以没有保证原子性，多线程访问会出问题，需要加锁：

```java
class SystemMonitor {
	private boolean starting = false;
	public void start() {
		// 加锁防止多线程破坏原子性
		synchronized(this) {
			if(starting) {
				return;
			}
		starting = true;
		}
		monitorThread = new Thread(()->{...;});
		monitorThread.start();
	}
}
```

## 应用

