---
title: 解决Ubuntu2204虚拟机滚轮在鼠标移动时失效问题
created: 2023-01-28 03:27:39
updated: 2023-01-28 03:31:00
tags: 
- article
---

# 解决Ubuntu2204虚拟机滚轮在鼠标移动时失效问题

安装 imwheel

```sh
sudo apt install imwheel
```

配置 imwheel

```sh
sudo vim ~/.imwheelrc
```

内容：

```
"^.*$"
    None, Up, Button4, 2
    None, Down, Button5, 2
    Shift_L,   Up,   Shift_L|Button4, 2
    Shift_L,   Down, Shift_L|Button5, 2
    Control_L, Up,   Control_L|Button4
    Control_L, Down, Control_L|Button5
```

运行：

```sh
/usr/bin/imwheel
```

添加自启动：

ubuntu搜索 startup applications：
![[3-计算机科学/3-操作系统/Linux/使用/z-attachments/Pasted image 20230128033032.png]]

添加：

![[3-计算机科学/3-操作系统/Linux/使用/z-attachments/Pasted image 20230128033055.png]]
