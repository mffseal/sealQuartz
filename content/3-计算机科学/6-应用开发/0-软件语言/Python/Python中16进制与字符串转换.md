---
title: Python中16进制与字符串转换
created: 2022-09-17 16:14:12
updated: 2022-09-17 16:14:41
tags: 
- article
---
# Python中16进制与字符串转换

## python3 中的字符串和编码

- 在最新的 Python 3 版本中，字符串是以 Unicode 编码的
- Python 的字符串类型是str
- 在内存中以Unicode表示，一个字符对应若干个字节
- 如果要在网络上传输，或者保存到磁盘上，就需要把str变为以字节为单位的 bytes

```
注意区分 `'ABC'` 和` b'ABC'` ，前者是`str`，后者虽然内容显示得和前者一样，但`bytes`的每个字符都只占用一个字节。
```

## hex()

- hex() 函数用于将10进制整数转换成16进制，以字符串形式表示

```
注意! hex() 返回的结果不是整数, 而是 16 进制的字符串表示形式!
```

## 0x 表示的 16 进制数

```py
a = 0xA
b = 0x5
c = a * b
print(a)
print(c)
```

输出的结果:

```
10
50
```

```
两个 16 进制数相乘, 结果是以 10 进制保存的!
```

## str.encode()

以 Unicode 表示的 str 通过 encode() 方法可以编码为指定的 bytes

```py
str.encode(encoding='UTF-8',errors='strict')
```

```py
>>> 'ABC'.encode('ascii')
b'ABC'
>>> '中文'.encode('utf-8')
b'\xe4\xb8\xad\xe6\x96\x87'
>>> '中文'.encode('ascii')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-1: ordinal not in range(128)
```

- 纯英文的str可以用 ASCII , UTF-8, 编码为 bytes，内容是一样的
- 含有中文的str可以用 UTF-8 编码为bytes。
- 含有中文的str无法用ASCII编码
    - 因为中文编码的范围超过了ASCII编码的范围

```
该方法返回编码后的字符串，它是一个 bytes 对象。
```

## bytes.decode()

- 如果我们从网络或磁盘上读取了字节流，那么读到的数据就是 bytes
- 要把bytes变为str，就需要用decode()方法

```py
bytes.decode(encoding="utf-8", errors="strict")
```

```py
>>> b'ABC'.decode('ascii')
'ABC'
>>> b'\xe4\xb8\xad\xe6\x96\x87'.decode('utf-8')
'中文'
```

```
该方法返回解码后的字符串!
```

如果bytes中只有一小部分无效的字节，可以传入errors='ignore'忽略错误的字节:

```py
>>> b'\xe4\xb8\xad\xff'.decode('utf-8', errors='ignore')
'中'

```

```
在操作字符串时，我们经常遇到str和bytes的互相转换。为了避免乱码问题，应当始终坚持使用UTF-8编码对str和bytes进行转换.
```

```
字符串在Python内部的表示是unicode编码，因此，在做编码转换时，通常需要以unicode作为中间编码，
即先将其他编码的字符串解码（decode）成unicode，再从unicode编码（encode）成另一种编码。
```

## bytes 与 str 的长度比较

```py
text1 = 'abc'
text2 = b'abc'
text3 = '好'
text4 = text3.encode('utf-8')
print(len(text1))
print(len(text2))
print(len(text3))
print(len(text4))
print('text3:', text3)
print('text4:', text4)
```

输出:

```
3
3
1
3
```

- len() 函数对 str 对象时计算的是字符数
- len() 函数对 bytes 对象时计算的是字节数

## binascii

```
`a2b_ *` 函数接受仅包含 ASCII 字符的 Unicode 字符串。  
其他函数只接受类似字节的对象（如字节，字节数组和其他支持缓冲区协议的对象）。
```

### binascii.b2a_hex(data)

- binascii.b2a_hex(data)
- binascii.hexlify(data)


- 接收 bytes 对象
- 返回输入 bytes 对象的十六进制表示形式
    - 返回的是 bytes 对象
- 输入数据的每个字节都转换为相应的2位十六进制表示
    - 返回的 bytes 对象长度是数据长度的两倍

```
string(bytes对象) --> 字符对应的 hex --> hex 字面转化为 string(bytes对象)
```

### binascii.a2b_hex(hexstr)

- binascii.a2b_hex(hexstr)
- binascii.unhexlify(hexstr)

- 接收仅包含 ASCII 字符的 Unicode 字符串
- 也可以接收 bytes 对象
- 返回十六进制字符串 hexstr 所表示的二进制数据
    - 返回的是 bytes 对象
- 该函数与b2a_hex（）的反函数
- hexstr 必须包含偶数个十六进制数字
    - 可以是大写或小写

```
string --> hex --> bytes 对象
```

