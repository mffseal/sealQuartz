---
title: Linux文件锁
created: 2022-10-05 00:42:28
updated: 2022-10-05 00:46:27
tags: 
- atom
---

# Linux文件锁

多进程异步访问文件需要使用文件锁实现同步。

## 过程

进程打开文件时，内核会产生一个对应的struct file变量，硬链接到对应inode。

![[2_0_2-计算机科学/2_0_2_1_2_3-软件系统/2_0_2_1_2_3_1-操作系统/linux/z-attachments/Pasted image 20221005004428.png]]

![[2_0_2-计算机科学/2_0_2_1_2_3-软件系统/2_0_2_1_2_3_1-操作系统/linux/z-attachments/Pasted image 20221005004553.png]]

## fcntl使用

![[2_0_2-计算机科学/2_0_2_1_2_3-软件系统/2_0_2_1_2_3_1-操作系统/linux/z-attachments/Pasted image 20221005004626.png]]

![[2_0_2-计算机科学/2_0_2_1_2_3-软件系统/2_0_2_1_2_3_1-操作系统/linux/z-attachments/Pasted image 20221005005033.png]]

	
