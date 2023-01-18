---
title: Linux_TCP编程
created: 2022-10-06 19:31:15
updated: 2022-10-06 21:42:08
tags: 
- atom
---

# Linux_TCP编程

## 编程模型

![[3-计算机科学/3-操作系统/Linux/z-attachments/Pasted image 20221006193131.png]]

![[3-计算机科学/3-操作系统/Linux/z-attachments/Pasted image 20221006193853.png]]

![[3-计算机科学/3-操作系统/Linux/z-attachments/Pasted image 20221006193901.png]]

## 主要接口

### socket

![[3-计算机科学/3-操作系统/Linux/z-attachments/Pasted image 20221006193943.png]]

### bind

![[3-计算机科学/3-操作系统/Linux/z-attachments/Pasted image 20221006194037.png]]

### listen

![[3-计算机科学/3-操作系统/Linux/z-attachments/Pasted image 20221006194147.png]]

客户端连接到来后会把连接放入未决连接队列中。

### accept

![[3-计算机科学/3-操作系统/Linux/z-attachments/Pasted image 20221006194258.png]]

### connect

![[3-计算机科学/3-操作系统/Linux/z-attachments/Pasted image 20221006195543.png]]

### 通用地址家族

```c
struct sockaddr{
  sa_family_t sa_family;
  char sa_data[14];
};
```

### ipv4地址家族

```c
     struct sockaddr_in {

       sa_family_t  sin_family; /* address family: AF_INET */

       in_port_t    sin_port; /* port in network byte order */

       struct in_addr sin_addr;   /* internet address */

};

/* Internet address. */

struct in_addr {

     uint32_t   s_addr;     /* address in network byte order */

};
```

### ipv6地址家族

```c
    struct sockaddr_in6 {

       sa_family_t     sin6_family;   /* AF_INET6 */

       in_port_t       sin6_port;     /* port number */

       uint32_t    sin6_flowinfo; /* IPv6 flow information */

       struct in6_addr sin6_addr;     /* IPv6 address */

       uint32_t    sin6_scope_id; /* Scope ID (new in 2.4) */

};

struct in6_addr {

       unsigned char   s6_addr[16];   /* IPv6 address */

};
```

### 字节序转换

![[3-计算机科学/3-操作系统/Linux/z-attachments/Pasted image 20221006195021.png]]

### 地址转换

![[3-计算机科学/3-操作系统/Linux/z-attachments/Pasted image 20221006195141.png]]

![[3-计算机科学/3-操作系统/Linux/z-attachments/Pasted image 20221006214207.png]]

## 案例

![[3-计算机科学/3-操作系统/Linux/z-attachments/Pasted image 20221006195719.png]]

![[3-计算机科学/3-操作系统/Linux/z-attachments/Pasted image 20221006195805.png]]
