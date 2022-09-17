---
title: stream
created: 2022-08-30 23:23:01
updated: 2022-08-30 23:23:53
tags: 
- atom
---
# stream

## OJ中的应用

将内容读取成string，再按照空格分割出字符串数组，再通过stream将字符串数组转成int数组。

```java
public class P5788 {  
    public static void main(String[] args) throws IOException {  
        BufferedReader buf = new BufferedReader(new InputStreamReader(System.in));  
  
        int n = Integer.parseInt(buf.readLine());  
        int[] array;  
  
        String str = buf.readLine();  
        array = Arrays.stream(str.split(" ")).mapToInt(Integer::parseInt).toArray();  
  
        int[]res = new int[n];  
  
        Stack<Integer> stack = new Stack<>();  
        for (int i=0; i<array.length; i++) {  
            while (!stack.isEmpty() && array[stack.peek()] < array[i]) {  
                int cur = stack.pop();  
                res[cur] = i+1;  
            }  
            stack.push(i);  
        }  
  
        for (int re : res) System.out.print(re + " ");  
    }  
}
```