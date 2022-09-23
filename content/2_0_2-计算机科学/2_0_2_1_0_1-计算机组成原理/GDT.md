---
title: GDT
created: 2022-09-23 20:55:06
updated: 2022-09-23 20:58:39
tags: 
- atom
---

# GDT

GDT段描述符类似一个可以理解为一个List，这个List保存的是Long值（64位），可假设为`List<Long> list = new ArrayList<Long>();`

这个List刚开始的时候由操作系统创建，放在内存的某个位置，位置地址会保存到GDTR寄存器中，结构如下：

![[2_0_2-计算机科学/2_0_2_1_0_1-计算机组成原理/z-attachments/Pasted image 20220923205651.png]]
![[2_0_2-计算机科学/2_0_2_1_0_1-计算机组成原理/z-attachments/Pasted image 20220923205738.png]]
这里段基地址和段属性拆分是为了兼容16位程序，一开始只有右半段，后来加了左边的。

## 参考

[「Coding Master」第28话 从实模式到保护模式的切换代码_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1a54y1G7Re/?spm_id_from=333.337.search-card.all.click&vd_source=dc239faaaafac9ea3e7880710bece137)
[GDT、GDTR和段寄存器的关系 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/512150749)
