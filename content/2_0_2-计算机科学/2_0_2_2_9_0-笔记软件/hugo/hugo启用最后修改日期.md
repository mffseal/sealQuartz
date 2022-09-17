---
title: hugo启用最后修改日期
created: 2022-05-12 20:54:46
updated: 2022-05-12 21:38:36
tags: 
- article
---
# hugo启用最后修改日期

## 读取笔记yaml信息

修改模板：
```yaml
updated: 填入日期
```

设置配置文件：
如果是yaml文件：
```yaml
frontmatter:
  lastmod: [":lastmod", "updated"]
```
如果是toml文件：
```toml
[frontmatter]
  lastmod = [":lastmod", "updated"]
```

配置文件中第二个字段与yaml中定义的字段一致即可。

## 读取笔记文件修改信息

设置配置文件：
如果是yaml文件：
```yaml
frontmatter:
  lastmod: [":fileModTime", "lastmod"]
```
如果是toml文件：
```toml
[frontmatter]
  lastmod = [":fileModTime", "lastmod"]
```