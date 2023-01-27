---
title: Linux文件元数据
created: 2022-10-04 22:28:50
updated: 2022-10-04 23:03:59
tags: 
- atom
---

# Linux文件元数据

![[3-计算机科学/3-操作系统/Linux/z-attachments/Pasted image 20221004222858.png]]

![[3-计算机科学/3-操作系统/Linux/z-attachments/Pasted image 20221004225821.png]]

数据块表是一个长度为15的整型数组，每个单元存放一个数据块编号。其中前11个直接存放数据块，后4个是块链的形式，其中每个块（4K情况）可以存放1024个整数代表其它块的编号。

1K * 1K * 4K = 4G
