---
title: 逆向wp-Easy-Re
created: 2022-09-17 21:43:19
updated: 2022-09-17 22:06:08
tags: 
- article
---
# 逆向wp-Easy-Re

bugku 逆向第二题.

## 定位关键函数

通过 ida 反编译, 很容易定位关键函数, 本题结构十分简单:

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int v3; // eax
  __int128 v5; // [esp+0h] [ebp-44h]
  __int64 v6; // [esp+10h] [ebp-34h]
  int v7; // [esp+18h] [ebp-2Ch]
  __int16 v8; // [esp+1Ch] [ebp-28h]
  char v9; // [esp+20h] [ebp-24h]

  _mm_storeu_si128((__m128i *)&v5, _mm_loadu_si128((const __m128i *)&xmmword_413E34));  // &xmmword_413E34 即被比较数据 flag
  v7 = 0;
  v6 = qword_413E44;
  v8 = 0;
  printf("欢迎来到DUTCTF呦\n");
  printf("这是一道很可爱很简单的逆向题呦\n");
  printf("输入flag吧:");
  scanf("%s", &v9);
  v3 = strcmp((const char *)&v5, &v9);  // 将输入与已有数据进行比较, 
  if ( v3 )
    v3 = -(v3 < 0) | 1;
  if ( v3 )
    printf(aFlag_0);
  else
    printf((const char *)&unk_413E90);
  system("pause");
  return 0;
}
```

## 解析字符串

对 `&xmmword_413E34` 位置的数据进行分析, 发现此处就是 flag 的逆序存储, 直接右键显示为 字符, 然后手工反向输入即可.

![[2_0_2-计算机科学/2_0_2_1_3_0-网络安全/二进制安全/逆向/writeup/z-attachments/Pasted image 20220917214345.png]]

## 借助 python 解码

> python 3

将数据复制出来, 放到python 3 里解码:

```py
import binascii

a = '7D465443545544'    ## 逆序所以后一段在前
b = binascii.a2b_hex(a)    ## 16 进制转为字符串
c = '3074656D30633165577B465443545544'
b += binascii.a2b_hex(c)    ## 16 进制转为字符串
str_list = list(b)    ## 将字符串转为数组
str_list.reverse()    ## 对数组逆序

for i in str_list:     ## 遍历输出数组, 以 chr 格式
    print(chr(i), end="")
```