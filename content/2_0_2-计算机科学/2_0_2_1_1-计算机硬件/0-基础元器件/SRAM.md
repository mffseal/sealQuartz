---
title: SRAM
created: 2022-09-04 15:02:29
updated: 2022-09-04 15:08:10
tags: 
- atom
---
# SRAM

静态随机存取存储器（Static Random-Access Memory，SRAM）是随机存取存储器的一种。所谓的“静态”，是指这种存储器只要保持通电，里面储存的数据就可以恒常保持。相对之下，动态随机存取存储器（DRAM）里面所储存的数据就需要周期性地更新。然而，当电力供应停止时，SRAM储存的数据还是会消失（被称为volatile memory），这与在断电后还能储存资料的ROM或闪存是不同的。


## 存储结构

![[z-oblib/z2-attachments/Pasted image 20220904150755.png]]

6T:指的是由六个晶体管组成，如图中的M1、M2、 M3、M4、M5、M6. SRAM中的每一bit存储在由4个场效应管(M1, M2, M3, M4)构成两个交叉耦合的反相器中。另外两个场效应管(M5, M6)是存储基本单元到用于读写的位线(BitLine)的控制开关。

6T电路等价于SR锁存器：

![[z-oblib/z2-attachments/Pasted image 20220904150813.png]]

