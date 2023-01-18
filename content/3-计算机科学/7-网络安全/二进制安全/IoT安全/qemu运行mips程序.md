---
title: qemu运行mips程序
created: 2022-09-19 23:22:29
updated: 2022-09-19 23:31:05
tags: 
- article
---

# qemu运行mips程序

1. [[3-计算机科学/7-网络安全/二进制安全/IoT安全/安装qemu|安装qemu]]
2. 拷贝[[3-计算机科学/7-网络安全/二进制安全/IoT安全/qemu-user-static|qemu-user-static]]到目标目录下：`cp /usr/bin/qemu-mips-static ./`。
3. 运行mips程序(其中./bin/busybox为要执行的busybox)：`sudo chroot . ./qemu-mips-static ./bin/busybox`。
