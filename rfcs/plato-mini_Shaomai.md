# Jina X Plato

## 简介

使用 Jina 框架实现基于 plato-mini 模型的对话机器人

flows 涵盖的协议与端口号：

| 协议名称  | 端口号 |
| --------- | ------ |
| http      | 12345  |
| websocket | 12346  |
| grpc      | 12347  |

## Demo

### 配置环境

```
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
```

### 开启对话后端服务

```
jina flow --uses flow.yml
```

### 开启客户端

Start another terminal with activated virtual environment. Then run:

```
python client.py
```

## 测试

```
pytest .\test\test_protocols.py
```
