---
title: 逆向wp-Reverse-100
created: 2022-09-17 21:52:26
updated: 2022-09-17 21:52:57
tags: 
- article
---
# 逆向wp-Reverse-100

[杭电 CTF 平台逆向第四题.](http://sec.hdu.edu.cn/question/reverse/5789?sort=default)

题目在网络对应目录中: http://gokoucat.ys168.com/

## 定位关键函数

老套路, string 查找, 不多 BB.

## 解析函数

这个函数比较简单, key 和 判断流程在一个简单的函数中直接展示:

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  signed int i; // edi
  char s_input; // [esp+10h] [ebp-104h]
  char Dst; // [esp+11h] [ebp-103h]

  s_input = 0;
  memset(&Dst, 0, 0xFFu);
  printf("please input ns-ctf password: ");
  scanf_s("%s", &s_input);
  for ( i = 1; strncmp("nsF0cuS!x01", &s_input, 0xBu); ++i )
  {
    printf("try again!\n");
    memset(&s_input, 0, 0x100u);
    printf("please input ns-ctf password: ");
    scanf_s("%s", &s_input);
  }
  dword_403368 = 1;
  if ( &s_input + strlen(&s_input) + 1 != &Dst )
  {
    if ( i > 3 )
    {
      sub_401000();
      return 0;
    }
    printf("flag:{NSCTF_md5065ca>01??ab7e0f4>>a701c>cd17340}");
  }
  return 0;
}
```

- 函数利用 for 里的语句循环读入字符串
- 字符串与 `nsF0cuS!x01` 比较, 相同则通过
- 如果 `i <= 3`, 返回的 flag 是未经处理的错误答案

## 作答

对策十分简单, 故意错误输入3次, 第四次输入 `nsF0cuS!x01` 即可

![[3-计算机科学/7-网络安全/二进制安全/逆向/writeup/z-attachments/Pasted image 20220917215255.png]]

