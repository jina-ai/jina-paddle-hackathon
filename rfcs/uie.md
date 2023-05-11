# Jina X UIE

实现一个 requests 以 schema 为参数，对输入的 DocArray 进行信息抽取

flows 中定义服务如下：

| 协议名称  | 端口号 |
| --------- | ------ |
| grpc      | 12344  |
| http      | 12345  |
| websocket | 12346  |

## 测试

1. 运行服务端

```
pdm start
```

2. 运行客户端

```
pdm test
```
