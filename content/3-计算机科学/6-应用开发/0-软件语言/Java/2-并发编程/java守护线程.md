---
title: java守护线程
created: 2022-05-26 17:35:48
updated: 2022-05-26 17:37:06
tags: 
- atom
---
# java守护线程

主线程结束时不管守护线程还有没有其它任务，都会强制结束守护线程。

主要用在：
- 垃圾回收器线程。
- Tomcat中的Accetor和Poller线程。（结束tomcat后不会等待当前请求处理完成而是会直接结束运行）。