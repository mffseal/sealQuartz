---
title: Linux创建进程
created: 2022-10-05 01:53:23
updated: 2022-10-05 18:14:00
tags: 
- atom
---

# Linux创建进程

## fork

![[3-计算机科学/3-操作系统/Linux/z-attachments/Pasted image 20221005015332.png]]

![[3-计算机科学/3-操作系统/Linux/z-attachments/Pasted image 20221005015435.png]]

![[3-计算机科学/3-操作系统/Linux/z-attachments/Pasted image 20221005020045.png]]

2.4内核下fork时会拷贝进程映像，及代码段、数据段、栈段、堆等。
2.6内核会采用写时复制技术，不全量复制PCB，节省内存空间。
