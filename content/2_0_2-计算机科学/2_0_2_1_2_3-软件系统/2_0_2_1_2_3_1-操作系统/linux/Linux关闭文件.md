---
title: Linux关闭文件
created: 2022-10-03 23:12:03
updated: 2022-10-03 23:13:37
tags: 
- atom
---

# Linux关闭文件

![[2_0_2-计算机科学/2_0_2_1_2_3-软件系统/2_0_2_1_2_3_1-操作系统/linux/z-attachments/Pasted image 20221003231213.png]]

通过引用计数来确定有几个[[2_0_2-计算机科学/2_0_2_1_2_3-软件系统/2_0_2_1_2_3_1-操作系统/linux/文件描述符|文件描述符]]表引用了该文件描述，如果本次关闭后对应文件的底层文件描述引用计数位0，则内核释放该文件资源。
