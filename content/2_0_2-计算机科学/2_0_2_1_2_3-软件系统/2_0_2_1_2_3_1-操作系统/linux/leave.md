---
title: leave
created: 2022-09-12 22:18:31
updated: 2022-09-12 23:25:01
tags: 
- atom
---
# leave

- `mov esp, ebp` 清空当前函数栈以还原栈空间（直接移动栈顶指针 **esp** 到当前函数的栈底 **ebp** ）；
- `pop ebp` 还原栈底（将此时 **esp** 所指的上层函数栈底 old ebp 弹入 **ebp** 寄存器内）；