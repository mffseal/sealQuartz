---
title: AbstractDispatcherServletInitializer的实现类为什么可以在初始化Web容器的时候被调用
created: 2022-08-19 23:41:11
updated: 2022-09-18 22:17:24
tags: 
- article
---

# AbstractDispatcherServletInitializer的实现类为什么可以在初始化Web容器的时候被调用

[(33条消息) AbstractDispatcherServletInitializer 的实现类为什么可以在初始化Web容器的时候被调用_Nishkata的博客-CSDN博客](https://blog.csdn.net/Nishkata/article/details/125432352)

[Spring MVC 之 AbstractAnnotationConfigDispatcherServletInitializer剖析_Spring MVC 之 AbstractAnnotationConfigDispatcherServletInitializer剖析|Samuel个人博客 (yangshuaibin.com)](https://www.yangshuaibin.com/detail/392696)

## Servlet 做的事

Servlet3.0 环境中，容器会在类路径中查找实现 ServletContainerInitializer 接口的类，如果发现的话，就用它来配置 Servlet 容器。  

## SpringMvc 做的事

Spring 提供了这个接口的实现类 SpringServletContainerInitializer , 通过 `@HandlesTypes(WebApplicationInitializer.class)` 设置，这个类反过来会查找实现 WebApplicationInitializer 的类，并将配置的任务交给他们来完成。  
AbstractAnnotationConfigDispatcherServletInitializer 类扩展了 WebApplicationInitializer 。这样就可以通过实现 AbstractAnnotationConfigDispatcherServletInitializer 来进行配置 Servlet 的上下文了。

DispatcherServletInitializer 配置类能够被加载的核心是 Java 的 [[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/Java/1-高级特性/SPI|SPI]] 服务发现机制。

1. 服务接口的定义：Servlet 规范定义了服务接口 `javax-servlet-api-xxx.jar/javax.servlet.ServletContainerInitializer`
2. 注册服务接口的实现： Spring MVC 注册服务。在 `spring-web-xxx.jar` 包下 有 `META-INF/services/javax.servlet.ServletContainerInitializer` 文件，内容为 `org.springframework.web.SpringServletContainerInitializer`
3. 服务加载： SpringServletContainerInitializer 中的 onStartup 方法会在 Servlet 容器初始化的时候通过 SPI 机制发现并调用，onStartup 方法里面又会 将所有 WebApplicationInitializer 的实现类的对象的 onStartup 方法全部调用一遍。
4. AbstractDispatcherServletInitializer 也是 WebApplicationInitializer 接口的实现，所以其 onStartup 方法也会在 Servlet 容器初始化的时候被调用。

![[z-oblib/z2-attachments/Pasted image 20220819234813.png]]
