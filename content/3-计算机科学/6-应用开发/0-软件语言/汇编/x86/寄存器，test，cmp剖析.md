---
title: 寄存器，test，cmp剖析
created: 2022-09-17 16:11:42
updated: 2022-09-17 16:12:26
tags: 
- article
---
# 寄存器，test，cmp剖析

## 状态寄存器

> 首先复习一下状态寄存器.

PSW(Program Status Word)程序状态字(即标志)寄存器,是一个16位寄存器,由条件码标志(flag)和控制标志构成,如下所示：  

![[3-计算机科学/6-应用开发/0-软件语言/汇编/z-attachments/Pasted image 20220917161214.png]]

条件码：  
- OF(Overflow Flag)溢出标志
    - 溢出时为1，否则置0
    - 标明一个溢出了的计算
- SF(Sign Flag)符号标志
    - 结果为负时置1，否则置0
- ZF(Zero Flag)零标志,
    - 运算结果为0时置1，否则置0
- CF(Carry Flag)进位标志
- 进位时置1，否则置0
- 注意:Carry标志中存放计算后最右的位
- AF(Auxiliary carry Flag)辅助进位标志
    - 记录运算时第3位(半个字节)产生的进位置
    有进位时1,否则置0。
- PF(Parity Flag)奇偶标志
    - 结果操作数中1的个数为偶数时置1，否则置0  
    - 
控制标志位：  
- DF(Direction Flag)方向标志
    - 在串处理指令中控制信息的方向
- IF(Interrupt Flag)中断标志
- TF(Trap Flag)陷井标志  

> test和cmp指令运行后都会设置标志位.

## test

> test 是逻辑运算符

- 执行BIT与BIT之间的逻辑运算
- 两操作数作与运算,仅修改标志位，不回送结果
- `test r/m, r/m/data`
- 影响标志位 C,O,P,Z,S(其中C与O两个标志会被设为0)
- test 的一个非常普遍的用法是用来测试一方寄存器是否为空
    - test ecx, ecx
    - jz somewhere
    - 如果ecx为零，设置ZF零标志为1，Jz跳转

## cmp

> cmp 属于算术运算指令

- 比较两个值(寄存器,内存,直接数值)
- 两操作数作减法,仅修改标志位,不回送结果
- `CMP r/m,r/m/data`
- 影响标志位 C,P,A,Z,O

## 总结

- test 逻辑与运算结果为零,就把ZF(零标志)置1
- cmp 算术减法运算结果为零,就把ZF(零标志)置1