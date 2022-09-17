---
title: Obsidian配置webdav远程同步服务器
created: 2022-05-10 16:56:02
updated: 2022-05-10 19:32:33
tags: 
- article
---
# Obsidian配置webdav远程同步服务器

## 准备

1. obsidian软件
2. obsidian remotely save插件
3. vps服务器 （ubuntu2004）

## 安装并配置nginx服务器

### 安装nginx及webdav插件
```shell
sudo apt
sudo apt -y install nginx nginx-extras libnginx-mod-http-dav-ext libnginx-mod-http-auth-pam
```

### 创建nginx配置文件
```shell
vim /etc/nginx/conf.d/webdav.conf
```

文件内容：
```nginx
server {
    listen 设置一个端口;
    listen [::]:设置一个端口;
    server_name 如果有域名就配在这里;
    # 设置使用utf-8编码,防止中文文件名乱码
    charset utf-8;
    # 默认存放文件的路径
    root /webdav;
    auth_basic              realm_name;
    # 用户密码文件存放位置
    auth_basic_user_file    /etc/nginx/.passwords.list;
    # dav 允许的操作
    dav_methods     PUT DELETE MKCOL COPY MOVE;
    dav_ext_methods PROPFIND OPTIONS;
    # 创建文件的默认权限
    dav_access      user:rw group:rw all:r;
    # 临时文件位置
    client_body_temp_path   /tmp;
    # 最大上传文件限制, 0表示无限制
    client_max_body_size    0;
    # 允许自动创建文件夹(如果有需要的话)
    create_full_put_path    on;
    autoindex on;
    autoindex_exact_size on;
	# 注意这里必须要用location块包起来，否则add_header会报错
    location / {
        if ($request_method = OPTIONS ) {
            add_header Content-Length 0;
            add_header Content-Type text/plain;
            add_header DAV 1,2;
            add_header Allow 'OPTIONS,HEAD,GET,PROPFIND,DELETE,COPY,MOVE,PROPPATCH,LOCK,UNLOCK';
            add_header Access-Control-Allow-Origin '$http_origin' always;
            add_header Access-Control-Allow-Credentials 'true' always;
            add_header Access-Control-Allow-Methods 'OPTIONS,HEAD,GET,POST,PUT,PROPFIND,DELETE,COPY,MOVE,PROPPATCH,LOCK,UNLOCK' always;
            add_header Access-Control-Allow-Headers '*' always;
            return 200;
        }

        add_header Access-Control-Allow-Origin '$http_origin' always;
        add_header Access-Control-Allow-Credentials 'true' always;
        add_header Access-Control-Allow-Methods 'OPTIONS,HEAD,GET,POST,PUT,PROPFIND,DELETE,COPY,MOVE,PROPPATCH,LOCK,UNLOCK' always;
        add_header Access-Control-Allow-Headers 'Origin,X-Requested-With,Content-Type,Accept,Authorization,Depth' always;
    }
}
```

测试连通性：
直接用浏览器访问地址：端口看是否能映射出目录。

注意：
- 必须要用location块把add_header部分包起来，否则add_header会报错，因为add_header不能用在server块下的if块中。

### 创建文件夹并配置权限
```shell
mkdir /webdav
sudo chown -R www-data:www-data /webdav
sudo chmod 755 /webdav
```

### 创建用户并生成密码
```shell
# 设置用户名
echo -n '设置一个用户名:' | sudo tee /etc/nginx/.passwords.list
# 生成密码并写入密文
openssl passwd -apr1 | sudo tee -a /etc/nginx/.passwords.list
# 确认输入两次密码
```

注意：
- 用户名后面要有冒号
- 文件此时保存的是所设置密码的密文

### 配置防火墙并启动服务

```shell
sudo ufw allow 你设置的端口
sudo systemctl start nginx
sudo systemctl enable nginx
```

## 设置插件

按照插件字段提示设置即可，有几个地方要注意：
- 服务器地址前也要加`http://`。
- 不建议开加密，可能文件名会超过linux255字符的限制导致同步失败。