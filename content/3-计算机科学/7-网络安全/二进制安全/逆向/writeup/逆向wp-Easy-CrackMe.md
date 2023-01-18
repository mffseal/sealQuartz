---
title: 逆向wp-Easy-CrackMe
created: 2022-09-17 21:39:29
updated: 2022-09-17 21:50:17
tags: 
- article
---
# 逆向wp-Easy-CrackMe

题目在网络对应目录中: http://gokoucat.ys168.com/

## 黑盒测试

- windows 窗体程序
- 没什么输入限制
- 错误返回字符串 `Incorrect Password`

![[3-计算机科学/7-网络安全/二进制安全/逆向/writeup/z-attachments/Pasted image 20220917214007.png]]

## 反编译

程序是 32 位的.

### 定位关键函数

通过字符串 `Incorrect Password` 定位关键函数, F5 分析 C 代码.

### 关键函数分析

> 变量名根据用途重命名过.

```c
int __cdecl sub_401080(HWND hDlg)
{
  int result; // eax@5
  CHAR c1; // [sp+4h] [bp-64h]@1
  char c2; // [sp+5h] [bp-63h]@1
  char c3; // [sp+6h] [bp-62h]@2
  char c4; // [sp+8h] [bp-60h]@3
  __int16 v6; // [sp+65h] [bp-3h]@1
  char v7; // [sp+67h] [bp-1h]@1

  c1 = 0;
  memset(&c2, 0, 0x60u);
  v6 = 0;
  v7 = 0;
  GetDlgItemTextA(hDlg, 1000, &c1, 100);
  if ( c2 == 'a' && !strncmp(&c3, a5y, 2u) && !strcmp(&c4, aR3versing) && c1 == 'E' )
  {
    MessageBoxA(hDlg, str_success, str_title1, 0x40u);
    result = EndDialog(hDlg, 0);
  }
  else
  {
    result = MessageBoxA(hDlg, aIncorrectPassw, str_title1, 0x10u);
  }
  return result;
}
```

发现 `if ( c2 == 'a' && !strncmp(&c3, a5y, 2u) && !strcmp(&c4, aR3versing) && c1 == 'E' )` 是关键.  

条件真则密码通过, 密码为 `'E' + 'a' + "5y" + "R3versing"`

![[3-计算机科学/7-网络安全/二进制安全/逆向/writeup/z-attachments/Pasted image 20220917214032.png]]