---
title: VFS文件系统
created: 2022-10-05 01:03:55
updated: 2022-10-05 01:16:34
tags: 
- atom
---

# VFS文件系统

![[3-计算机科学/3-操作系统/Linux/z-attachments/Pasted image 20221005010403.png]]

task_stuct就是进程的PCB。
f_entry是文件的路径，一般会先指向一个缓冲，图中便于理解直接指向了dentry（directory entry）。
