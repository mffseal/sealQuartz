---
title: cmake骨架
created: 2023-01-17 17:28:19
updated: 2023-01-18 10:36:46
tags: 
- draft
---

# cmake骨架

## 主模块

1. 设定Cmake版本要求
2. 设定项目名称
3. 设定语言标准
4. 打开源码文件，添加可执行文件
5. 设定编译选项
6. 添加子模块目录
7. 设定项目安装目录
8. 设定头文件搜索路径
9. 设定链接器搜索路径
10. 设定安装路径
    1. 设定`CMAKE_INSTALL_PREFIX`环境变量
    2. 二进制文件安装路径
    3. 头文件安装路径

## 子模块

1. 添加库文件
2. 设定对外的头文件导入路径
    1. [[3-计算机科学/6-应用开发/0-软件语言/cmake/项目命令/target_include_directories|target_include_directories]]指定头文件搜索目录
    2. 
